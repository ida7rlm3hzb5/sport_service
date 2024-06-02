from django.contrib import admin
from .models import Equipment, EquipmentOrder, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity')
    search_fields = ('name', 'description')
    list_filter = ('quantity',)


class EquipmentOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'order_time')
    search_fields = ('user__username', 'order_date')
    list_filter = ('order_date', 'order_time')



admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentOrder, EquipmentOrderAdmin)
