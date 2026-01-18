def cart_count(request):
    cart = request.session.get("cart", {})
    total = 0
    if isinstance(cart, dict):
        for value in cart.values():
            try:
                quantity = int(value.get("quantity", 0))
            except (AttributeError, TypeError, ValueError):
                quantity = 0
            if quantity > 0:
                total += quantity
    return {"cart_count": total}
