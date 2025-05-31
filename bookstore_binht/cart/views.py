from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from bookstore_binht.books.models import Book

from .cart import CartHandler
from .models import CartItem


@require_POST
def add_to_cart(request):
    book_id = request.POST.get("book_id")
    book = get_object_or_404(Book, id=book_id)
    cart = CartHandler(request)
    cart.add(book=book)

    if request.user.is_authenticated:
        cart_item = cart.cart.items.get(book_id=book_id)
        add_book_quantity = cart_item.quantity
    else:
        add_book_quantity = cart.cart[book_id]["quantity"]

    return JsonResponse(
        {
            "total_item": str(cart.__len__()),
            "total_price": str(cart.get_total_price()),
            "add_book_id": str(book.id),
            "add_book_quantity": str(add_book_quantity),
        },
    )


@require_POST
def cart_decrease(request):
    book_id = request.POST.get("book_id")
    cart = CartHandler(request)
    book = get_object_or_404(Book, id=book_id)
    cart.decrease(book)

    if request.user.is_authenticated:
        try:
            cart_item = cart.cart.items.get(book_id=book_id)
            decrease_book_quantity = cart_item.quantity
        except CartItem.DoesNotExist:
            decrease_book_quantity = 0
    else:
        decrease_book_quantity = (
            cart.cart[book_id]["quantity"] if book_id in cart.cart else 0
        )

    return JsonResponse(
        {
            "total_item": str(cart.__len__()),
            "total_price": str(cart.get_total_price()),
            "decrease_book_id": str(book.id),
            "decrease_book_quantity": str(decrease_book_quantity),
        },
    )


@require_POST
def cart_remove(request, book_id):
    cart = CartHandler(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect("cart:cart_detail")


class CartListView(ListView):
    template_name = "cart/cart_list.html"
    context_object_name = "cart"

    def get_queryset(self):
        return CartHandler(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_price"] = context["cart"].get_total_price()
        return context
