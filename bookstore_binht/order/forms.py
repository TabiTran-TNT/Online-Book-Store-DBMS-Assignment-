from django.forms import ModelForm

from .models import Order


class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = ["shipping_address", "zip_code", "city", "country"]

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super().__init__(*args, **kwargs)

        for field in self.fields.items():
            field[1].widget.attrs.update({"class": "form-control"})
