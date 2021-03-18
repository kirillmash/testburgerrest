from rest_framework import serializers

from .models import Dish, Order, DishesInOrder


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('name', 'description', 'price')


class DishesInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishesInOrder
        fields = ('dish', 'quantity',)


class OrderSerializer(serializers.ModelSerializer):
    dishes = serializers.ListField(child=DishesInOrderSerializer())

    class Meta:
        model = Order
        fields = ('restaurant', 'dishes')


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('price',)
