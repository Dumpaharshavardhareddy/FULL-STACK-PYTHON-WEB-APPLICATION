from django.urls import path
from . import views


app_name = "restaurant"

urlpatterns = [
    path("", views.home, name="home"),
    path("menu/", views.menu, name="menu"),
    path("cart/", views.cart, name="cart"),
    path("login/", views.customer_login, name="customer_login"),
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-order-status/<str:order_id>/<str:new_status>/", views.update_order_status, name="update_order_status"),
    path("orders/<str:order_id>/", views.order_detail, name="order_detail"),
    path("cart/count/", views.cart_count_api, name="cart_count_api"),
    path("cart/increase/", views.cart_increase, name="cart_increase"),
    path("cart/decrease/", views.cart_decrease, name="cart_decrease"),
    path("cart/remove/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.orders, name="orders"),
    path("contact/", views.contact, name="contact"),
    path("login-options/", views.choose_login, name="choose_login"),
    path("signup/", views.signup, name="signup"),

    path("payment/confirm/", views.payment_confirmation, name="payment_confirm"),
    path("otp/verify/", views.otp_verification, name="otp_verification"),
    path("payment/failed/", views.payment_failed, name="payment_failed"),
    path("place-order/", views.place_order, name="place_order"),
]
