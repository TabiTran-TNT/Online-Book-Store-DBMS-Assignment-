from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from bookstore_binht.books.models import Book, Category

from .factories import BookFactory, CategoryFactory

# Define constants
EXPECTED_AVG_RATE = 5
FUTURE_BOOK_PRICE = Decimal("29.99")


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = CategoryFactory(name="Fiction", sort_order=1)

    def test_category_creation(self):
        assert isinstance(self.category, Category)
        assert str(self.category) == self.category.name

    def test_category_ordering(self):
        CategoryFactory(name="Non-fiction", sort_order=2)
        categories = Category.objects.all()
        assert categories[0].name == "Fiction"
        assert categories[1].name == "Non-fiction"


class BookModelTest(TestCase):
    def setUp(self):
        self.category = CategoryFactory(name="Science Fiction")
        self.book = BookFactory(
            title="Test Book",
            description="A test book description",
            author_name="John Doe",
            publisher_name="Test Publisher",
            published_date=timezone.now().date(),
            unit_price=Decimal("19.99"),
            photo="media/test.jpg",
            total_rating_value=0,
            total_rating_count=0,
            pages=300,
        )
        self.book.total_rating_count = 0
        self.book.total_rating_value = 0
        self.book.categories.add(self.category)

    def test_book_creation(self):
        assert isinstance(self.book, Book)
        assert str(self.book) == self.book.title

    def test_book_category_relationship(self):
        assert self.book.categories.count() == 1
        assert self.book.categories.first() == self.category

    def test_avg_rate_property(self):
        assert self.book.avg_rate == 0
        self.book.total_rating_value = 10
        self.book.total_rating_count = 2
        self.book.save()
        assert self.book.avg_rate == EXPECTED_AVG_RATE

    def test_decimal_field_precision(self):
        self.book.unit_price = Decimal("19.999")
        self.book.save()
        self.book.refresh_from_db()
        assert self.book.unit_price == Decimal("20.00")
