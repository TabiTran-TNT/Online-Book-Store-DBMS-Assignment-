import locale

from django.db import models

from bookstore_binht.users.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_formatted_total_price(self):
        total_price = self.get_total_price()
        locale.setlocale(locale.LC_ALL, "")
        formatted_total_price = locale.format_string("%d", total_price, grouping=True)
        return f"{formatted_total_price}đ"

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())
