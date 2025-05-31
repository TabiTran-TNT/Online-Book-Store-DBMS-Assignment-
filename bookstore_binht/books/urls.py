from django.urls import path

from . import views

app_name = "books"  # This sets up the namespace

urlpatterns = [
    path("<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path(
        "<int:pk>/comment/",
        views.BookCommentListView.as_view(),
        name="book_comments",
    ),
]
