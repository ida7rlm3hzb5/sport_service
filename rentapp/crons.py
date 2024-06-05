from django_cron import CronJobBase, Schedule
from django.utils import timezone
from .models import EquipmentOrder


class MarkOverdueOrdersCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # 24 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'rentapp.mark_overdue_orders_cron_job'  # a unique code

    def do(self):
        overdue_time = timezone.now() - timezone.timedelta(days=1)
        overdue_orders = EquipmentOrder.objects.filter(
            order_date__lte=overdue_time.date(),
            status__in=['CREATED', 'RENTED']
        )
        overdue_orders.update(status='OVERDUE')
