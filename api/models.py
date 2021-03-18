from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_menu = models.BooleanField(default=True, verbose_name='Отображать в меню?')

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    dishes = models.ManyToManyField(Dish, through='DishesInOrder', through_fields=('order', 'dish'))

    class Status(models.TextChoices):
        PAID = 'Оплачен'
        UNPAID = 'Неоплачен'
        CANCELED = 'Отменен'

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNPAID)

    def __str__(self):
        return f"Заказ №{self.id}, статус - {self.status}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class DishesInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Блюдо {self.dish.name}  заказе №{self.order.id}"

    class Meta:
        verbose_name = 'Блюда в заказе'
        verbose_name_plural = 'Блюда в заказе'

    def save(self, *args, **kwargs):
        self.total_price = self.dish.price * self.quantity
        super().save(*args, **kwargs)
