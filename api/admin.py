from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Restaurant, Category, SubCategory, Dish, DishesInOrder, Order


class DishesInline(admin.TabularInline):
    model = Order.dishes.through
    fields = ('order', 'dish', 'quantity', 'total_price')
    readonly_fields = ('order', 'dish', 'quantity', 'total_price')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'total_price', 'operator', 'created_at', 'status')
    fields = ('restaurant', 'total_price', 'operator', 'created_at', 'status')
    search_fields = ('id',)
    readonly_fields = ('restaurant', 'total_price', 'operator', 'created_at')
    inlines = [
        DishesInline
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'in_menu', 'category', 'subcategory')
    fields = ('name', 'price', 'description', 'in_menu', 'category', 'subcategory')
    search_fields = ('name',)
    list_editable = ('in_menu',)


admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)




