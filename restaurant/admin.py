from django.contrib import admin
from .models import (
    Category,
    MenuItem,
    Order,
    OrderItem,
    PaymentOTP,
    ContactMessage,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "is_popular",
        "is_available",
        "image",
        "image_url",
        "created_at",
    )
    list_filter = ("category", "is_popular", "is_available")
    search_fields = ("name", "description")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "customer_name",
        "customer_email",
        "total",
        "payment_method",
        "payment_status",
        "status",
        "created_at",
    )
    list_filter = ("status", "payment_status", "payment_method")
    search_fields = ("order_id", "customer_name", "customer_email", "customer_phone", "address")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "category", "price", "quantity", "line_total")
    search_fields = ("name", "category", "order__order_id")


@admin.register(PaymentOTP)
class PaymentOTPAdmin(admin.ModelAdmin):
    list_display = ("order", "otp_code", "attempts", "max_attempts", "is_verified", "created_at", "expires_at")
    list_filter = ("is_verified",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "created_at")
    search_fields = ("name", "email", "phone", "subject", "message")
