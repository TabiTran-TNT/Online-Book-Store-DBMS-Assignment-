import locale
from decimal import Decimal

from django.conf import settings
from django.shortcuts import get_object_or_404

from bookstore_binht.books.models import Book

from .models import Cart, CartItem


class CartHandler:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.user = request.user
        if self.user and self.user.is_authenticated:
            self.cart, created = Cart.objects.get_or_create(user=self.user)
            self.cart_items = self.cart.items.all()
        else:
            cart = self.session.get(settings.CART_SESSION_ID)
            if not cart:
                cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart

    def add(self, book):
        if self.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                cart=self.cart,
                book=book,
            )
            if not created:
                cart_item.quantity += 1
            cart_item.save()
        else:
            book_id = str(book.id)
            if book_id not in self.cart:
                self.cart[book_id] = {"quantity": 0, "price": str(book.unit_price)}
            self.cart[book_id]["quantity"] += 1
            self.save()

    def decrease(self, book):
        if self.user.is_authenticated:
            try:
                cart_item = CartItem.objects.get(cart=self.cart, book=book)
                cart_item.quantity -= 1
                if cart_item.quantity <= 0:
                    cart_item.delete()
                else:
                    cart_item.save()
            except CartItem.DoesNotExist:
                pass
        else:
            book_id = str(book.id)
            if book_id in self.cart:
                self.cart[book_id]["quantity"] -= 1
                if self.cart[book_id]["quantity"] == 0:
                    self.remove(book)
                self.save()

    def save(self):
        self.session.modified = True

    def remove(self, book):
        if self.user.is_authenticated:
            CartItem.objects.filter(cart=self.cart, book=book).delete()
        else:
            book_id = str(book.id)
            if book_id in self.cart:
                del self.cart[book_id]
                self.save()

    def __iter__(self):
        if self.user.is_authenticated:
            for cart_item in self.cart_items:
                yield {
                    "book": cart_item.book,
                    "quantity": cart_item.quantity,
                    "price": cart_item.book.unit_price,
                }
        else:
            book_ids = self.cart.keys()
            books = Book.objects.filter(id__in=book_ids)
            for book in books:
                self.cart[str(book.id)]["book"] = book
            for item in self.cart.values():
                item["price"] = Decimal(item["price"])
                yield item

    def __len__(self):
        if self.user.is_authenticated:
            return sum(item.quantity for item in self.cart_items)
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        if self.user.is_authenticated:
            total_price = round(
                sum(item.book.unit_price * item.quantity for item in self.cart_items),
            )
            locale.setlocale(locale.LC_ALL, "")
            formatted_total_price = locale.format_string(
                "%d",
                total_price,
                grouping=True,
            )
            return f"{formatted_total_price}đ"

        total_price = round(
            sum(
                Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
            ),
        )
        locale.setlocale(locale.LC_ALL, "")
        formatted_total_price = locale.format_string(
            "%d",
            total_price,
            grouping=True,
        )
        return f"{formatted_total_price}đ"

    def clear(self):
        if self.user.is_authenticated:
            self.cart.items.all().delete()
        else:
            del self.session[settings.CART_SESSION_ID]
            self.save()

    def merge_cart_to_db(self):
        if not self.request.user.is_authenticated:
            return

        for book_id, item in self.session.get(settings.CART_SESSION_ID, {}).items():
            book = get_object_or_404(Book, id=book_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=self.cart,
                book=book,
            )
            if not created:
                cart_item.quantity += item["quantity"]
            cart_item.save()

        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
