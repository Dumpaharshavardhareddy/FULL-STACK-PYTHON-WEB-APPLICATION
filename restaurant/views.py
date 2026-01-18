import json
import os
import time
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib import messages

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Q
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import MenuItem, Order


IMAGE_NAME_MAP = [
    ("paneer", "paneer_tikka.jpg"),
    ("biryani", "chicken_biryani.jpg"),
    ("mango", "mango_juice.jpg"),
    ("cool", "cool_drink.jpg"),
    ("gulab", "gulab_jamun.jpg"),
    ("ice", "ice_cream.jpg"),
    ("manchuria", "veg_manchuria.jpg"),
    ("fried rice", "veg_fried_rice.jpg"),


    ("chocolate", "chocolate_lava_cake.jpg"),
]




def _image_path_for_menu_name(name):
    value = (name or "").lower()
    for key, filename in IMAGE_NAME_MAP:
        if key in value:
            return "menu_items/" + filename
    return None


def _ensure_menu_item_images():
    media_root = getattr(settings, "MEDIA_ROOT", None)
    if not media_root:
        return

    directory = os.path.join(media_root, "menu_items")
    if not os.path.isdir(directory):
        return

    def _slug(value):
        value = (value or "").strip().lower()
        if not value:
            return ""
        parts = []
        prev_underscore = False
        for ch in value:
            if ch.isalnum():
                parts.append(ch)
                prev_underscore = False
            else:
                if not prev_underscore:
                    parts.append("_")
                    prev_underscore = True
        slug = "".join(parts).strip("_")
        return slug

    filenames = os.listdir(directory)
    file_map = {}
    for name in filenames:
        base, _ext = os.path.splitext(name)
        slug = _slug(base)
        if slug and slug not in file_map:
            file_map[slug] = name

    for item in MenuItem.objects.all():
        if item.image:
            continue
        slug = _slug(item.name)
        if not slug:
            continue
        filename = file_map.get(slug)
        if filename:
            item.image = "menu_items/" + filename
            item.save(update_fields=["image"])


def home(request):
    return render(request, "restaurant/home.html")


def choose_login(request):
    return render(request, "restaurant/choose_login.html")


def signup(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect("restaurant:signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return redirect("restaurant:signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please login.")
            return redirect("restaurant:customer_login")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = False
        user.is_superuser = False
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("restaurant:customer_login")

    return render(request, "restaurant/signup.html")

def menu(request):
    if not MenuItem.objects.exists():
        sample_items = [
            {
                "name": "Paneer Tikka",
                "category": MenuItem.CATEGORY_STARTERS,
                "price": 200,
                "description": "Marinated paneer cubes grilled with spices.",
                "rating": 4.5,
                "is_popular": True,
                "image_url": "https://images.unsplash.com/photo-1604908176997-1251884b08a7",
                "is_available": True,
            },
            {
                "name": "Veg Manchuria",
                "category": MenuItem.CATEGORY_STARTERS,
                "price": 180,
                "description": "Crispy vegetable balls tossed in tangy sauce.",
                "rating": 4.3,
                "is_popular": False,
                "image_url": "https://images.unsplash.com/photo-1604908176997-1251884b08a7",
                "is_available": True,
            },
            {
                "name": "Chicken Biryani",
                "category": MenuItem.CATEGORY_MAIN_COURSE,
                "price": 260,
                "description": "Fragrant basmati rice cooked with spiced chicken.",
                "rating": 4.6,
                "is_popular": True,
                "image_url": "https://images.unsplash.com/photo-1604908176997-1251884b08a7",
                "is_available": True,
            },
            {
                "name": "Veg Fried Rice",
                "category": MenuItem.CATEGORY_MAIN_COURSE,
                "price": 220,
                "description": "Stir fried rice with mixed vegetables and sauces.",
                "rating": 4.2,
                "is_popular": False,
                "image_url": "https://images.unsplash.com/photo-1604908176997-1251884b08a7",
                "is_available": True,
            },
            {
                "name": "Mango Juice",
                "category": MenuItem.CATEGORY_BEVERAGES,
                "price": 90,
                "description": "Refreshing chilled mango juice.",
                "rating": 4.4,
                "is_popular": False,
                "image_url": "https://images.unsplash.com/photo-1577801596755-03888a34ec6c",
                "is_available": True,
            },
            {
                "name": "Cool Drink",
                "category": MenuItem.CATEGORY_BEVERAGES,
                "price": 60,
                "description": "Carbonated soft drink served chilled.",
                "rating": 4.1,
                "is_popular": False,
                "image_url": "https://images.unsplash.com/photo-1541976076758-25a71c0b2f2d",
                "is_available": True,
            },
            {
                "name": "Gulab Jamun",
                "category": MenuItem.CATEGORY_DESSERTS,
                "price": 120,
                "description": "Soft milk dumplings soaked in sugar syrup.",
                "rating": 4.7,
                "is_popular": True,
                "image_url": "https://images.unsplash.com/photo-1606491956689-2ea866880c84",
                "is_available": True,
            },
            {
                "name": "Ice Cream",
                "category": MenuItem.CATEGORY_DESSERTS,
                "price": 100,
                "description": "Creamy vanilla ice cream scoop.",
                "rating": 4.3,
                "is_popular": False,
                "image_url": "https://images.unsplash.com/photo-1501446529957-6226bd447c46",
                "is_available": True,
            },
        ]
        for data in sample_items:
            MenuItem.objects.create(**data)

    _ensure_menu_item_images()

    items = MenuItem.objects.filter(is_available=True).order_by("category", "name")
    context = {"items": items}
    return render(request, "restaurant/menu.html", context)


def cart(request):
    cart = _get_session_cart(request)
    items, subtotal = _cart_items_with_totals(cart)

    delivery_fee = Decimal("30.00") if subtotal > 0 else Decimal("0.00")
    total = subtotal + delivery_fee

    context = {
        "items": items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
    }
    return render(request, "restaurant/cart.html", context)


def checkout(request):
    cart = _get_session_cart(request)
    items, subtotal = _cart_items_with_totals(cart)
    delivery_fee = Decimal("30.00") if subtotal > 0 else Decimal("0.00")
    total = subtotal + delivery_fee

    if request.method == "POST":
        if not items:
            return redirect("restaurant:cart")

        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        address = (request.POST.get("address") or "").strip()
        instructions = (request.POST.get("instructions") or "").strip()
        payment_method = request.POST.get("paymentMethod") or "COD"

        customer = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "instructions": instructions,
        }

        if payment_method == "COD":
            order_id = _create_session_order(request, customer, payment_method, is_online=False)
            if not order_id:
                return redirect("restaurant:cart")
            return redirect("restaurant:order_detail", order_id=order_id)

        request.session["pending_order"] = {
            "customer": customer,
            "payment_method": payment_method,
        }
        request.session.modified = True
        return redirect("restaurant:payment_confirm")

    context = {
        "items": items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
    }
    return render(request, "restaurant/checkout.html", context)


def orders(request):
    stored_orders = request.session.get("orders", [])
    if not isinstance(stored_orders, list):
        stored_orders = []
    orders = list(stored_orders)[::-1]
    return render(request, "restaurant/orders.html", {"orders": orders})


def contact(request):
    return render(request, "restaurant/contact.html")


def payment_confirmation(request):
    return render(request, "restaurant/payment_confirmation.html")


def otp_verification(request):
    return render(request, "restaurant/otp_verification.html")


def payment_failed(request):
    return render(request, "restaurant/payment_failed.html")


def place_order(request):
    cart = _get_session_cart(request)
    items, subtotal = _cart_items_with_totals(cart)
    if not items:
        return redirect("restaurant:cart")

    pending = request.session.get("pending_order") or {}
    customer = pending.get("customer") or {
        "name": "",
        "email": "",
        "phone": "",
        "address": "",
        "instructions": "",
    }
    payment_method = pending.get("payment_method") or "COD"

    order_id = _create_session_order(request, customer, payment_method, is_online=True)
    request.session.pop("pending_order", None)
    request.session.modified = True

    if not order_id:
        return redirect("restaurant:cart")
    return redirect("restaurant:order_detail", order_id=order_id)


def order_detail(request, order_id):
    stored_orders = request.session.get("orders", [])
    order = None
    if isinstance(stored_orders, list):
        for item in stored_orders:
            if item.get("order_id") == order_id:
                order = item
                break
    if not order:
        return render(request, "restaurant/order_not_found.html", {"order_id": order_id}, status=404)
    return render(request, "restaurant/order_detail.html", {"order": order})


def _is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(_is_admin)
def admin_dashboard(request):
    stored_orders = request.session.get("orders", [])
    if not isinstance(stored_orders, list):
        stored_orders = []

    total_orders = len(stored_orders)
    pending_orders = 0
    total_revenue = Decimal("0.00")
    for order in stored_orders:
        status = order.get("status")
        if status in ["Pending", "Placed"]:
            pending_orders += 1
        total_raw = order.get("total", 0)
        try:
            total_revenue += Decimal(str(total_raw))
        except Exception:
            continue

    total_menu_items = MenuItem.objects.count()
    orders = list(stored_orders)[::-1]

    context = {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_revenue": total_revenue,
        "total_menu_items": total_menu_items,
        "orders": orders,
    }
    return render(request, "restaurant/admin_dashboard.html", context)


def choose_login(request):
    return render(request, "restaurant/choose_login.html")


def customer_login(request):
    error = None
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect("restaurant:menu")
        error = "Invalid username or password."
    return render(request, "restaurant/customer_login.html", {"error": error})


def admin_login(request):
    error = None
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            if user.is_staff:
                login(request, user)
                return redirect("restaurant:admin_dashboard")
            error = "You do not have permission to access the admin dashboard."
        else:
            error = "Invalid username or password."
    return render(request, "restaurant/admin_login.html", {"error": error})


@login_required
@user_passes_test(_is_admin)
def update_order_status(request, order_id, new_status):
    allowed_status = ["Pending", "Preparing", "Delivered"]
    if new_status not in allowed_status:
        raise Http404("Invalid status")

    stored_orders = request.session.get("orders", [])
    if isinstance(stored_orders, list):
        for order in stored_orders:
            if order.get("order_id") == order_id:
                order["status"] = new_status
                break
        request.session["orders"] = stored_orders
        request.session.modified = True

    return redirect("restaurant:admin_dashboard")


def cart_count_api(request):
    cart = _get_session_cart(request)
    count = _cart_total_count(cart)
    return JsonResponse({"cart_count": count})


def _get_session_cart(request):
    cart = request.session.get("cart", {})
    if not isinstance(cart, dict):
        cart = {}
    return cart


def _save_session_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True


def _cart_items_with_totals(cart):
    items = []
    subtotal = Decimal("0.00")
    for key, value in cart.items():
        try:
            quantity = int(value.get("quantity", 0))
        except (AttributeError, TypeError, ValueError):
            quantity = 0
        if quantity <= 0:
            continue
        price_raw = value.get("price", 0)
        try:
            price = Decimal(str(price_raw))
        except Exception:
            price = Decimal("0.00")
        line_total = price * quantity
        items.append(
            {
                "id": value.get("id") or key,
                "name": value.get("name", ""),
                "category": value.get("category", ""),
                "price": price,
                "quantity": quantity,
                "image_url": value.get("image_url", ""),
                "line_total": line_total,
            }
        )
        subtotal += line_total
    return items, subtotal


def _cart_total_count(cart):
    total = 0
    for value in cart.values():
        try:
            quantity = int(value.get("quantity", 0))
        except (AttributeError, TypeError, ValueError):
            quantity = 0
        if quantity > 0:
            total += quantity
    return total


def _create_session_order(request, customer, payment_method, is_online):
    cart = _get_session_cart(request)
    items, subtotal = _cart_items_with_totals(cart)
    if not items:
        return None

    delivery_fee = Decimal("30.00") if subtotal > 0 else Decimal("0.00")
    total = subtotal + delivery_fee

    order_id = "ORD" + str(int(time.time() * 1000))

    order_items = []
    for item in items:
        order_items.append(
            {
                "id": item["id"],
                "name": item["name"],
                "category": item["category"],
                "price": float(item["price"]),
                "quantity": item["quantity"],
                "image_url": item["image_url"],
                "line_total": float(item["line_total"]),
            }
        )

    orders = request.session.get("orders", [])
    if not isinstance(orders, list):
        orders = []

    order = {
        "order_id": order_id,
        "items": order_items,
        "subtotal": float(subtotal),
        "delivery_fee": float(delivery_fee),
        "total": float(total),
        "created_at": time.strftime("%Y-%m-%d %H:%M"),
        "status": "Pending",
        "payment_method": payment_method,
        "payment_status": "Paid" if is_online and payment_method != "COD" else ("COD" if payment_method == "COD" else "Pending"),
        "customer": customer,
    }

    orders.append(order)
    request.session["orders"] = orders
    request.session["cart"] = {}
    request.session.modified = True

    return order_id


def _parse_item_id(request):
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            data = {}
        return data.get("item_id")
    return request.POST.get("item_id")


@csrf_exempt
@require_POST
def cart_increase(request):
    item_id = _parse_item_id(request)
    if not item_id:
        if request.content_type == "application/json":
            return JsonResponse({"success": False, "error": "Missing item_id"}, status=400)
        return redirect("restaurant:cart")

    cart = _get_session_cart(request)
    try:
        item_pk = int(item_id)
    except (TypeError, ValueError):
        if request.content_type == "application/json":
            return JsonResponse({"success": False, "error": "Invalid item_id"}, status=400)
        return redirect("restaurant:cart")

    key = str(item_pk)
    data = cart.get(key)
    if data is None:
        try:
            menu_item = MenuItem.objects.get(id=item_pk, is_available=True)
        except MenuItem.DoesNotExist:
            if request.content_type == "application/json":
                return JsonResponse({"success": False, "error": "Item not found"}, status=404)
            return redirect("restaurant:cart")
        data = {
            "id": menu_item.id,
            "name": menu_item.name,
            "category": menu_item.category,
            "price": float(menu_item.price),
            "quantity": 0,
            "image_url": menu_item.image_url or "",
        }

    try:
        quantity = int(data.get("quantity", 0)) + 1
    except (TypeError, ValueError):
        quantity = 1

    data["quantity"] = quantity
    cart[key] = data
    _save_session_cart(request, cart)
    total_count = _cart_total_count(cart)
    if request.content_type == "application/json":
        return JsonResponse({"success": True, "quantity": quantity, "cart_count": total_count})
    return redirect("restaurant:cart")


@csrf_exempt
@require_POST
def cart_decrease(request):
    item_id = _parse_item_id(request)
    if not item_id:
        if request.content_type == "application/json":
            return JsonResponse({"success": False, "error": "Missing item_id"}, status=400)
        return redirect("restaurant:cart")

    cart = _get_session_cart(request)
    try:
        item_pk = int(item_id)
    except (TypeError, ValueError):
        if request.content_type == "application/json":
            return JsonResponse({"success": False, "error": "Invalid item_id"}, status=400)
        return redirect("restaurant:cart")

    key = str(item_pk)
    data = cart.get(key)
    if data is None:
        if request.content_type == "application/json":
            return JsonResponse({"success": True, "quantity": 0, "cart_count": _cart_total_count(cart)})
        return redirect("restaurant:cart")

    try:
        quantity = int(data.get("quantity", 0)) - 1
    except (TypeError, ValueError):
        quantity = 0

    if quantity <= 0:
        cart.pop(key, None)
        quantity = 0
    else:
        data["quantity"] = quantity
        cart[key] = data

    _save_session_cart(request, cart)
    total_count = _cart_total_count(cart)
    if request.content_type == "application/json":
        return JsonResponse({"success": True, "quantity": quantity, "cart_count": total_count})
    return redirect("restaurant:cart")


@csrf_exempt
@require_POST
def cart_remove(request):
    item_id = _parse_item_id(request)
    if not item_id:
        if request.content_type == "application/json":
            return JsonResponse({"success": False, "error": "Missing item_id"}, status=400)
        return redirect("restaurant:cart")

    cart = _get_session_cart(request)
    try:
        item_pk = int(item_id)
    except (TypeError, ValueError):
        if request.content_type == "application/json":
            return JsonResponse({"success": False, "error": "Invalid item_id"}, status=400)
        return redirect("restaurant:cart")

    key = str(item_pk)
    cart.pop(key, None)
    _save_session_cart(request, cart)
    total_count = _cart_total_count(cart)
    if request.content_type == "application/json":
        return JsonResponse({"success": True, "quantity": 0, "cart_count": total_count})
    return redirect("restaurant:cart")
