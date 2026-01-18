from decimal import Decimal

from django.db import models
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    CATEGORY_STARTERS = "Starters"
    CATEGORY_MAIN_COURSE = "Main Course"
    CATEGORY_BEVERAGES = "Beverages"
    CATEGORY_DESSERTS = "Desserts"

    CATEGORY_CHOICES = [
        (CATEGORY_STARTERS, "Starters"),
        (CATEGORY_MAIN_COURSE, "Main Course"),
        (CATEGORY_BEVERAGES, "Beverages"),
        (CATEGORY_DESSERTS, "Desserts"),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    description = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal("4.0"))
    is_popular = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="menu_items/", blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    PAYMENT_METHOD_COD = "COD"
    PAYMENT_METHOD_PHONEPE = "PhonePe"
    PAYMENT_METHOD_GPAY = "GPay"
    PAYMENT_METHOD_PAYTM = "Paytm"

    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_METHOD_COD, "COD"),
        (PAYMENT_METHOD_PHONEPE, "PhonePe"),
        (PAYMENT_METHOD_GPAY, "GPay"),
        (PAYMENT_METHOD_PAYTM, "Paytm"),
    ]

    order_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    address = models.TextField()
    instructions = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, default="Pending")
    status = models.CharField(max_length=20, default="Placed")
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("30.00"))
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_totals(self):
        aggregate = self.items.aggregate(subtotal=Sum("line_total"))
        subtotal = aggregate["subtotal"] or Decimal("0.00")
        self.subtotal = subtotal
        self.total = subtotal + (self.delivery_fee or Decimal("0.00"))
        super().save(update_fields=["subtotal", "total"])

    def save(self, *args, **kwargs):
        if self.subtotal is not None and self.delivery_fee is not None:
            self.total = (self.subtotal or Decimal("0.00")) + (self.delivery_fee or Decimal("0.00"))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))

    def save(self, *args, **kwargs):
        if self.price is not None and self.quantity is not None:
            self.line_total = (self.price or Decimal("0.00")) * self.quantity
        super().save(*args, **kwargs)
        if self.order_id:
            self.order.update_totals()

    def __str__(self):
        return f"{self.name} x {self.quantity}"


class PaymentOTP(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment_otp")
    otp_code = models.CharField(max_length=6)
    attempts = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for order {self.order_id}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
