from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bookstore_binht.cart"
    label = "cart"

    def ready(self):
        from django.contrib.auth.signals import user_logged_in

        from .signals import merge_cart_on_login

        user_logged_in.connect(merge_cart_on_login)
