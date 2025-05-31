# Bookstore BinhT

Bookstore assignment
[![Coverage Status](https://coveralls.io/repos/EastAgile/Bookstore-BinhT-Python/badge.svg?branch=develop)](https://coveralls.io/github/EastAgile/Bookstore-BinhT-Python?branch=develop)
[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Steps to run the application

### Install the requirements
Ensure you have installed `pip` and `python`. For the guide of pip installation, visit this site [here](https://pip.pypa.io/en/stable/installation/). Then install the requirements with this command for local development:

    $ pip install -r requirements/local.txt

If you only want to run the application for production development:

    $ pip install -r requirements/production.txt

### Migrate database

Running data migration files with the command:

    $ python manage.py migrate

If there are any errors happening during running the command, consider delete all migrations files in folder `migrations` of all apps (except for `init.py`). Then run this command:

    $ python manage.py makemigrations
and run the command `python manage.py migrate` again

### Seed data for the database

The seed file will populate data for book's categories. To do this, run the command:

    $ python manage.py seed
You can also seed data optionally for comments, orders, users, books with the command:

    $ python manage.py seed --include-optional

### Run the server

    $ python manage.py runserver
Now, you can view the application at http://127.0.0.1:8000/

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" modal popping up. Go to your email to verify your account

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser
Fill in the correct email and password, then go to your email to verify your account.

## Optional
### Custom the Bootstrap's framework
You can also custom the framework of bootstrap in `bookstore_binht/static/sass/bootstrapv5.2.3.scss`. Then generate the `min.css` file of bootstrap using the command:

      $ python manage.py compile_scss
This command automatically runs when you runs `python manage.py runserver`.
### Test coverage

To execute the following commands, you need to install all requirements for local development. To run the tests, check your test coverage, and generate an HTML coverage report:
- Run unit tests

      $ coverage run --parallel-mode --data-file=.coverage.pytest -m pytest
- Run Behavior-driven development (BDD) tests:

      $ coverage run --parallel-mode --data-file=.coverage.django_behave manage.py behave --noinput
- Generate an HTMl coverage report and open the report:

      $ coverage combine
      $ coverage html
      $ open htmlcov/index.html

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).
