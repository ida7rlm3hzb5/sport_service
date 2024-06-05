from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from .models import Equipment, Category, EquipmentOrder, OrderedEquipment


class EquipmentListView(ListView):
    model = Equipment
    template_name = 'rentapp/equipment_list.html'
    context_object_name = 'equipment_list'

    def get_queryset(self):
        selected_categories = self.request.GET.getlist('categories')
        if selected_categories:
            return Equipment.objects.filter(category__id__in=selected_categories)
        return Equipment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_date'] = timezone.now().strftime('%Y-%m-%d')  # Форматируем дату
        context['current_time'] = timezone.now().strftime('%H:%M')  # Форматируем время
        return context


class ConfirmOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        order_date = request.POST['order_date']
        order_time = request.POST['order_time']
        equipment_quantities = {k: v for k, v in request.POST.items() if k.startswith('equipment_quantity_')}

        total_price = 0
        order_details = []

        with transaction.atomic():
            order = EquipmentOrder.objects.create(
                user=user,
                order_date=order_date,
                order_time=order_time,
                total_price=0  # will be updated later
            )

            for eq_id, quantity in equipment_quantities.items():
                quantity = int(quantity)
                if quantity > 0:
                    equipment_id = int(eq_id.split('_')[-1])
                    equipment = Equipment.objects.get(id=equipment_id)

                    if equipment.quantity < quantity:
                        # Handle the case where there is not enough inventory
                        transaction.set_rollback(True)
                        return redirect('not_found')  # Redirect to an error page

                    OrderedEquipment.objects.create(
                        equipment=equipment,
                        quantity=quantity,
                        order=order
                    )

                    equipment.decrease_available_quantity(quantity)
                    equipment.save()

                    total_price += equipment.price * quantity
                    order_details.append(f"{equipment.name}: {quantity} шт.")

            order.total_price = total_price
            order.save()

        return redirect('user', user_id=user.id)


class OrderListView(View):
    def get(self, request):
        orders = EquipmentOrder.objects.filter(status__in=['CREATED', 'RENTED', 'OVERDUE']).prefetch_related('ordered_equipment__equipment').order_by('-order_date', '-order_time')
        old_orders = EquipmentOrder.objects.filter(status='RETURNED').order_by('-order_date', '-order_time')

        for order in orders:
            order.total_price = order.ordered_equipment.annotate(
                total_item_price=F('equipment__price') * F('quantity')
            ).aggregate(total_price=Sum('total_item_price'))['total_price'] or 0

        return render(request, 'rentapp/order_list.html', {'orders': orders, 'old_orders': old_orders})


@method_decorator(login_required, name='dispatch')
class OrderIssueView(View):
    def post(self, request, order_id):
        order = EquipmentOrder.objects.get(id=order_id)
        action = request.POST.get('action')

        # Обработка выдачи заказа
        order.status = 'RENTED'
        order.save()
        # Дополнительные действия, если необходимо

        return redirect('order_list')  # Перенаправляем на список заказов после выполнения действия


@method_decorator(login_required, name='dispatch')
class OrderAcceptView(View):
    def post(self, request, order_id):
        order = EquipmentOrder.objects.get(id=order_id)

        with transaction.atomic():
            # Обработка принятия заказа
            for item in order.ordered_equipment.all():
                equipment = item.equipment
                equipment.increase_available_quantity(item.quantity)
            order.status = 'RETURNED'

            order.save()

        # Дополнительные действия, если необходимо
        return redirect('order_list')  # Перенаправляем на список заказов после выполнения действия


class OrderDeleteView(View):
    def post(self, request, order_id):
        order = EquipmentOrder.objects.get(id=order_id)
        action = request.POST.get('action')

        # Обработка удаления заказа
        order.delete()
        # Дополнительные действия, если необходимо

        return redirect('order_list')  # Перенаправляем на список заказов после выполнения действия
