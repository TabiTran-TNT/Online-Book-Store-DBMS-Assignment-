from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .cart import CartHandler


@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    request.user = user
    cart_handler = CartHandler(request)
    cart_handler.merge_cart_to_db()
