from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Book

# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author_name",
        "publisher_name",
        "published_date",
        "unit_price",
        "total_rating_value",
        "total_rating_count",
    ]
    search_fields = ["title", "author_name"]
    ordering = ["id"]
    list_filter = ["author_name", "publisher_name"]
    date_hierarchy = "published_date"
    fieldsets = (
        (None, {"fields": ("title", "description", "author_name", "publisher_name")}),
        (_("Book details"), {"fields": ("published_date", "unit_price", "photo")}),
        (_("Rating"), {"fields": ("total_rating_value", "total_rating_count")}),
    )
    readonly_fields = ["total_rating_value", "total_rating_count"]
