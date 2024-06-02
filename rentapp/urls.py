from django.urls import path
from .views import EquipmentListView, ConfirmOrderView, OrderListView, OrderIssueView, OrderAcceptView, OrderDeleteView

urlpatterns = [
    path('equipment/', EquipmentListView.as_view(), name='equipment_list'),
    # path('book/', EquipmentBookingView.as_view(), name='book_equipment'),
    path('confirm/', ConfirmOrderView.as_view(), name='confirm_order'),
    path('order_list/', OrderListView.as_view(), name='order_list'),
    path('order/issue_order/<int:order_id>/', OrderIssueView.as_view(), name='issue_order'),
    path('order/accept_order/<int:order_id>/', OrderAcceptView.as_view(), name='accept_order'),
    path('order/delete_order/<int:order_id>/', OrderDeleteView.as_view(), name='delete_order'),
]
