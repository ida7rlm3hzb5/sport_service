from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def increase_available_quantity(self, amount):
        self.quantity += amount
        self.save()

    def decrease_available_quantity(self, amount):
        if self.quantity - amount >= 0:
            self.quantity -= amount
            self.save()
        else:
            raise ValueError("Insufficient available quantity to decrease")


class OrderedEquipment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Количество заказанного оборудования
    order = models.ForeignKey('EquipmentOrder', related_name='ordered_equipment', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.equipment.name} - {self.quantity}"


class EquipmentOrder(models.Model):
    STATUS_CHOICES = (
        ('CREATED', 'Создан'),
        ('RENTED', 'Арендован'),
        ('RETURNED', 'Возвращено'),
        ('OVERDUE', 'Просрочено'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField()
    order_time = models.TimeField()
    total_price = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CREATED')

    def __str__(self):
        return f"Order by {self.user.username} on {self.order_date} at {self.order_time}"
