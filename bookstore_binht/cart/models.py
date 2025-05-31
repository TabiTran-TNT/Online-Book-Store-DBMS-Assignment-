import locale

from django.db.models import (
    CASCADE,
    ForeignKey,
    Model,
    OneToOneField,
    PositiveIntegerField,
)


class Cart(Model):
    user = OneToOneField("users.User", on_delete=CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def get_total_price(self):
        total_price = round(sum(item.get_cost() for item in self.items.all()))
        locale.setlocale(locale.LC_ALL, "")
        formatted_total_price = locale.format_string("%d", total_price, grouping=True)
        return f"{formatted_total_price}đ"


class CartItem(Model):
    cart = ForeignKey(Cart, on_delete=CASCADE, related_name="items")
    book = ForeignKey("books.Book", on_delete=CASCADE)
    quantity = PositiveIntegerField(default=1)

    def __str__(self):
        return (
            f"{self.quantity} of {self.book.title} in {self.cart.user.username}'s Cart"
        )

    def get_cost(self):
        return self.quantity * self.book.unit_price

    def get_unit_price(self):
        return self.book.unit_price
