import json
from datetime import datetime
from pathlib import Path
from secrets import choice, randbelow

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import connection

from bookstore_binht.books.models import Book, Category, Comment
from bookstore_binht.order.models import Order, OrderItem

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--include-optional",
            action="store_true",
            help="Include optional data (users, books, orders, comments)",
        )

    def handle(self, *args, **options):
        self.clear_data()
        self.seed_categories()
        if options["include_optional"]:
            self.seed_books()
            self.seed_users()
            self.seed_comments()
            self.seed_orders()
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))

    def clear_data(self):
        self.stdout.write("Clearing existing data...")
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Comment.objects.all().delete()
        Book.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE books_comment_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE books_book_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE books_category_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE order_order_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE order_orderitem_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE account_emailaddress_id_seq RESTART WITH 1")

        self.stdout.write(self.style.SUCCESS("Existing data cleared successfully!"))

    def seed_categories(self):
        categories_file = (
            Path(__file__).resolve().parent.parent.parent
            / "seed_data"
            / "categories.json"
        )
        self.stdout.write(str(categories_file))
        with categories_file.open("r") as file:
            categories_data = json.load(file)

        for category_data in categories_data:
            Category.objects.get_or_create(
                id=category_data["pk"],
                defaults={
                    "name": category_data["fields"]["name"],
                    "sort_order": category_data["fields"]["sort_order"],
                },
            )
        self.stdout.write(self.style.SUCCESS("Categories seeded successfully!"))

    def seed_users(self):
        user_data_file = (
            Path(__file__).resolve().parent.parent.parent / "seed_data" / "user.json"
        )
        with user_data_file.open("r") as file:
            user_data = json.load(file)

        for user_info in user_data:
            fields = user_info["fields"]
            email = fields["email"]
            password = fields["password"]
            name = fields["name"]
            birthday_str = fields["birthday"]
            birthday = datetime.strptime(birthday_str, "%d/%m/%Y").date()
            phone = fields["phone"]

            if user_info["pk"] == 1:
                user = User.objects.create_superuser(
                    email=email,
                    password=password,
                    name=name,
                )
            else:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    name=name,
                )

            user.birthday = birthday
            user.phone = phone
            user.save()

            EmailAddress.objects.create(
                user=user,
                email=email,
                verified=True,
                primary=True,
            )

        self.stdout.write(self.style.SUCCESS("Users seeded successfully!"))

    def seed_books(self):
        books_file = (
            Path(__file__).resolve().parent.parent.parent / "seed_data" / "books.json"
        )
        with books_file.open("r") as file:
            books_data = json.load(file)

        for book_data in books_data:
            book_fields = book_data["fields"]
            book, created = Book.objects.update_or_create(
                id=book_data["pk"],
                defaults={
                    "title": book_fields["title"],
                    "description": book_fields["description"],
                    "author_name": book_fields["author_name"],
                    "publisher_name": book_fields["publisher_name"],
                    "published_date": book_fields["published_date"],
                    "unit_price": book_fields["unit_price"],
                    "photo": book_fields.get("photo", ""),
                    "pages": book_fields["page_count"],
                    "isbn_10": book_fields.get("isbn", ""),
                    "dimensions": book_fields.get("dimensions", ""),
                    "weight": book_fields.get("weight", 0),
                    "total_rating_value": book_fields.get("rating_value", 0),
                    "total_rating_count": book_fields.get("rating_count", 0),
                },
            )
            # Add categories to book
            category_ids = book_fields["categories"]
            book.categories.set(Category.objects.filter(id__in=category_ids))

        self.stdout.write(self.style.SUCCESS("Books seeded successfully!"))

    def seed_comments(self):
        books = Book.objects.all()
        users = list(User.objects.all())
        for book in books:
            for _ in range(randbelow(3) + 2):
                user = choice(users)
                while Comment.objects.filter(book=book, author=user).exists():
                    user = choice(users)
                rating = randbelow(5) + 1
                Comment.objects.create(
                    book=book,
                    author=user,
                    content=(
                        f"This is a sample comment from user {user.name} "
                        f"for book {book.title}."
                    ),
                    rating=rating,
                )

                book.total_rating_value += rating
                book.total_rating_count += 1
                book.save()

        self.stdout.write(self.style.SUCCESS("Comments seeded successfully!"))

    def seed_orders(self):
        users = list(User.objects.all())
        books = list(Book.objects.all())

        for _ in range(randbelow(3) + 3):
            user = choice(users)
            order = Order.objects.create(
                user=user,
                shipping_address="123 Main St",
                zip_code="12345",
                city="Sample City",
                country="Sample Country",
            )
            for _ in range(randbelow(3) + 2):
                book = choice(books)
                quantity = randbelow(5) + 1
                OrderItem.objects.create(
                    order=order,
                    book=book,
                    unit_price=book.unit_price,
                    quantity=quantity,
                )
        self.stdout.write(self.style.SUCCESS("Orders seeded successfully!"))
