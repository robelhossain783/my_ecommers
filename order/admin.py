from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):

    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "user",
        "full_name",
        "phone",
        "total_amount",
        "status",
        "payment_type",
        "address",
        "created_at",
    ]

    list_filter = [
        "status",
        "created_at",
    ]

    search_fields = [
        "user__username",
        "phone",
        "full_name",
    ]

    list_editable = [
        "status",
    ]

    readonly_fields = [
        "total_amount",
        "created_at",
    ]

    inlines = [
        OrderItemInline
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "order",
        "product",
        "quantity",
        "price",
    ]

    search_fields = [
        "product__name",
    ]