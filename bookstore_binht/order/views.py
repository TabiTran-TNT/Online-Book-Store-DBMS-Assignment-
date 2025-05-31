import os

import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, ListView, TemplateView

from bookstore_binht.cart.models import Cart

from .forms import OrderCreateForm
from .models import Order, OrderItem

NUM_PAST_ORDERS = 4


class CheckoutView(LoginRequiredMixin, ListView, FormView):
    template_name = "order/checkout.html"
    form_class = OrderCreateForm
    context_object_name = "cart_items"
    success_url = reverse_lazy("order:order_payment")

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        return cart.items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        context["total_price"] = cart.get_total_price()
        context["full_name"] = self.request.user.name
        context["first_name"] = self.request.user.get_first_name()
        context["last_name"] = self.request.user.get_last_name()
        context["phone"] = self.request.user.phone
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        checkout_data = form.cleaned_data.copy()
        checkout_data["full_name"] = user.name
        checkout_data["phone"] = user.phone

        self.request.session["checkout_data"] = checkout_data
        return super().form_valid(form)


stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = "order/payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checkout_data"] = self.request.session.get("checkout_data", {})
        cart = Cart.objects.get(user=self.request.user)
        context["cart_items"] = cart.items.all()
        context["total_price"] = cart.get_total_price()
        context["stripe_publishable_key"] = os.environ.get("STRIPE_PUBLIC_KEY")
        context["domain"] = os.environ.get("DOMAIN")

        formatted_price = cart.get_total_price().replace("đ", "").replace(",", "")
        amount = int(formatted_price)

        payment_intent_id = self.request.session.get("payment_intent_id")

        if payment_intent_id:
            try:
                intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                if intent.status in [
                    "requires_payment_method",
                    "requires_confirmation",
                    "requires_action",
                ]:
                    context["client_secret"] = intent.client_secret
                else:
                    payment_intent_id = None
            except stripe.error.StripeError:
                payment_intent_id = None

        if not payment_intent_id:
            try:
                intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency="vnd",
                    automatic_payment_methods={
                        "enabled": True,
                    },
                )
                self.request.session["payment_intent_id"] = intent.id
                context["client_secret"] = intent["client_secret"]
            except stripe.error.StripeError as e:
                context["stripe_error"] = str(e)
        return context


def payment_status(request):
    client_secret = request.GET.get("payment_intent")

    if client_secret:
        intent = stripe.PaymentIntent.retrieve(client_secret)
        status = intent.status

        if status == "succeeded":
            if request.session.get("checkout_data"):
                save_order(request)
    else:
        status = "unknown"

    return render(request, "order/payment_status.html", {"status": status})


def save_order(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = cart.items.all()

    order = Order.objects.create(
        user=user,
        shipping_address=request.session.get("checkout_data")["shipping_address"],
        zip_code=request.session.get("checkout_data")["zip_code"],
        city=request.session.get("checkout_data")["city"],
        country=request.session.get("checkout_data")["country"],
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            book=item.book,
            unit_price=item.get_unit_price(),
            quantity=item.quantity,
        )

    cart.items.all().delete()
    del request.session["checkout_data"]


@csrf_exempt
def cash_payment(request):
    if request.method == "POST":
        if request.session.get("checkout_data"):
            save_order(request)
        return render(request, "order/payment_status.html", {"status": "succeeded"})
    return None


class PastOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "order/past_order_list.html"
    context_object_name = "orders"
    ordering = ["-created"]
    paginate_by = NUM_PAST_ORDERS

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context["paginator"]
        page_obj = context["page_obj"]
        context["elided_page_range"] = paginator.get_elided_page_range(
            number=page_obj.number,
            on_each_side=1,
            on_ends=2,
        )

        return context
