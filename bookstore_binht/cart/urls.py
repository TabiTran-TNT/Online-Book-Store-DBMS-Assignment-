from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("add/", views.add_to_cart, name="add_to_cart"),
    path("detail/", views.CartListView.as_view(), name="cart_detail"),
    path("decrease/", views.cart_decrease, name="cart_decrease"),
    path("remove/<int:book_id>/", views.cart_remove, name="cart_remove"),
]
