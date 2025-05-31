from django.db import models

from bookstore_binht.books.models import Book

from .order import Order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.book.title} in order {self.order.id}"

    def get_cost(self):
        return self.unit_price * self.quantity
