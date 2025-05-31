from .cart import CartHandler


def cart_total_items(request):
    cart = CartHandler(request)
    return {"cart_total_items": cart.__len__()}
