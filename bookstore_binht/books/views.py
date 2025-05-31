from django.contrib import messages
from django.db.models import F, Q, Value
from django.db.models.functions import Concat
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from bookstore_binht.books import models

from .forms import CommentForm

DEFAULT_PER_PAGE = 10
DEFAULT_COMMENT_PER_PAGE = 5


class BookListView(ListView):
    model = models.Book
    context_object_name = "books"
    template_name = "home.html"
    paginate_by = DEFAULT_PER_PAGE

    def get_paginate_by(self, queryset):
        return self.request.GET.get("per_page", self.paginate_by)

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get("category")
        search_query = self.request.GET.get("search")

        if category_id and category_id.isdigit():
            queryset = queryset.filter(categories=category_id)

        if search_query:
            queryset = queryset.annotate(
                title_author=Concat(
                    F("title"),
                    Value(" "),
                    F("author_name"),
                ),
                author_title=Concat(
                    F("author_name"),
                    Value(" "),
                    F("title"),
                ),
            )

            queryset = queryset.filter(
                Q(title_author__icontains=search_query)
                | Q(author_title__icontains=search_query),
            )
        queryset = queryset.order_by("id")
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = models.Category.objects.all().order_by(
            "sort_order",
            "name",
        )

        category_param = self.request.GET.get("category", "")
        if category_param.isdigit():
            context["selected_category"] = int(category_param)
        else:
            context["selected_category"] = None

        context["search_query"] = self.request.GET.get("search", "")
        for book in context["books"]:
            book.star_ratings = book.get_star_rating()

        paginator = context["paginator"]
        page_obj = context["page_obj"]
        context["elided_page_range"] = paginator.get_elided_page_range(
            number=page_obj.number,
            on_each_side=1,
            on_ends=2,
        )

        return context


class BookDetailView(FormMixin, DetailView):
    model = models.Book
    template_name = "books/book_detail.html"
    context_object_name = "book"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context["star_rating"] = book.get_star_rating()
        context["total_rating_count"] = book.total_rating_count
        context["comments"] = book.comments.order_by("-created")[:4]
        context["categories"] = models.Category.objects.all().order_by(
            "sort_order",
            "name",
        )
        context["book_categories"] = book.categories.all()
        rating_distribution = book.get_rating_distribution()
        context["rating_distribution"] = {
            str(r["rating"]): int(r["count"]) for r in rating_distribution
        }
        return context


class BookCommentListView(FormMixin, ListView):
    model = models.Comment
    template_name = "books/book_comments.html"
    context_object_name = "comments"
    paginate_by = DEFAULT_COMMENT_PER_PAGE
    form_class = CommentForm

    def get_queryset(self):
        self.book = get_object_or_404(models.Book, pk=self.kwargs["pk"])
        return models.Comment.objects.filter(book=self.book).order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = self.book
        context["star_rating"] = self.book.get_star_rating()
        context["total_rating_count"] = self.book.total_rating_count
        rating_distribution = self.book.get_rating_distribution()
        context["categories"] = models.Category.objects.all().order_by(
            "sort_order",
            "name",
        )
        context["rating_distribution"] = {
            str(r["rating"]): int(r["count"]) for r in rating_distribution
        }

        paginator = context["paginator"]
        page_obj = context["page_obj"]
        context["elided_page_range"] = paginator.get_elided_page_range(
            number=page_obj.number,
            on_each_side=1,
            on_ends=2,
        )

        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if request.user.is_authenticated:
            self.object = None
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            return self.form_invalid(form)

        messages.error(
            request,
            "You need to be logged in to post a comment.",
        )  # Set error message
        return self.get(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.book = self.book
        comment.author = self.request.user

        try:
            comment.save()
        except IntegrityError:
            messages.error(
                self.request,
                "You can only comment once on each book.",
            )
            return redirect(reverse("books:book_comments", kwargs={"pk": self.book.pk}))

        self.book.total_rating_value += comment.rating
        self.book.total_rating_count += 1
        self.book.save()

        return redirect(reverse("books:book_comments", kwargs={"pk": self.book.pk}))
