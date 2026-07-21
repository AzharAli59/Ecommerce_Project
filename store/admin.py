from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Cart, Customer, OrderPlaced, Product


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'email', 'phone', 'address', 'state']
    list_filter = ['state']
    list_select_related = ['user']
    search_fields = ['name', 'email', 'phone', 'address', 'user__username']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'selling_price',
        'discounted_price',
        'brand',
        'category',
        'product_image',
    ]
    list_filter = ['category', 'brand']
    search_fields = ['title', 'brand', 'description']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    list_select_related = ['user', 'product']
    search_fields = ['user__username', 'product__title']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'customer_name',
        'product_name',
        'quantity',
        'ordered_date',
        'status',
    ]
    list_filter = ['status', 'ordered_date']
    list_select_related = ['user', 'customer', 'product']
    search_fields = ['user__username', 'customer__name', 'product__title']

    def customer_name(self, obj):
        link = reverse('admin:store_customer_change', args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    def product_name(self, obj):
        link = reverse('admin:store_product_change', args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
