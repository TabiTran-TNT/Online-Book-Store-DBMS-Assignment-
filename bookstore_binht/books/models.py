import locale
from math import floor

from django.conf import settings
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

DEFAULT_BOOK_IMAGE = settings.MEDIA_URL + "media/book_placeholder.png"
HALF_STAR_THRESHOLD = 0.5


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    sort_order = models.IntegerField(default=0)

    def get_absolute_url(self):
        return f"{reverse('home')}?category={self.id}"

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "categories"
        app_label = "books"

    def __str__(self):
        return self.name


class Book(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author_name = models.CharField(max_length=200)
    publisher_name = models.CharField(max_length=100)
    published_date = models.DateField(default=timezone.now)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to="media/", default=DEFAULT_BOOK_IMAGE)
    total_rating_value = models.IntegerField(default=0)
    total_rating_count = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name="books")

    isbn_10 = models.CharField(_("ISBN-10"), max_length=15, blank=True)
    edition = models.CharField(_("Edition"), max_length=100, blank=True)
    dimensions = models.CharField(_("Dimensions"), max_length=100, blank=True)
    weight = models.CharField(_("Weight"), max_length=50, blank=True)
    pages = models.PositiveIntegerField(_("Number of pages"))

    class Meta:
        ordering = ["-created"]
        app_label = "books"

    def __str__(self):
        return self.title

    @property
    def avg_rate(self):
        if self.total_rating_count > 0:
            return round(self.total_rating_value / self.total_rating_count, 1)
        return 0

    def get_star_rating(self):
        avg = self.avg_rate
        full_stars = floor(avg)
        half_star = avg - full_stars >= HALF_STAR_THRESHOLD
        empty_stars = 5 - full_stars - (1 if half_star else 0)

        return {
            "full_stars": full_stars,
            "half_star": half_star,
            "empty_stars": empty_stars,
        }

    def get_rating_distribution(self):
        return (
            self.comments.values("rating")
            .annotate(count=Count("rating"))
            .order_by("-rating")
        )

    def get_formatted_price(self):
        locale.setlocale(locale.LC_ALL, "")
        price = round(self.unit_price)
        formatted_price = locale.format_string("%d", price, grouping=True)
        return f"{formatted_price}đ"

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return DEFAULT_BOOK_IMAGE


class Comment(TimeStampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        ordering = ["-created"]
        app_label = "books"
        unique_together = ["book", "author"]

    def __str__(self):
        return f"Comment by {self.author} on {self.book.title}"
