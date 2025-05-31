from factory import Faker, post_generation
from factory.django import DjangoModelFactory
from faker import Faker as FakerClass

from bookstore_binht.books.models import Book, Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Faker("word")
    sort_order = Faker("random_int", min=0, max=100)


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book
        skip_postgeneration_save = True

    title = Faker("sentence", nb_words=4)
    description = Faker("paragraph")
    author_name = Faker("name")
    publisher_name = Faker("company")
    published_date = Faker("date_this_decade")
    unit_price = Faker("pydecimal", left_digits=6, right_digits=2, positive=True)
    photo = Faker("file_path", extension="jpg")
    total_rating_value = Faker("random_int", min=0, max=500)
    total_rating_count = Faker("random_int", min=0, max=100)
    isbn_10 = Faker("isbn10")
    edition = Faker("word")
    dimensions = Faker("word")
    weight = Faker("word")
    pages = Faker("random_int", min=50, max=1000)

    @post_generation
    def set_ratings(self, create, extracted, **kwargs):
        if not create:
            return

        faker = FakerClass()

        self.total_rating_count = faker.random_int(min=0, max=100)
        if self.total_rating_count > 0:
            avg_rating = faker.pyfloat(min_value=1, max_value=5, right_digits=2)
            self.total_rating_value = round(avg_rating * self.total_rating_count)
        else:
            self.total_rating_value = 0

        self.save()
