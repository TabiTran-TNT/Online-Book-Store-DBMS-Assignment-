#!/usr/bin/env python
# ruff: noqa
import os
import sys
import subprocess
from pathlib import Path

if __name__ == "__main__":
    if "DYNO" in os.environ and "CI" not in os.environ:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
        os.environ.setdefault(
            "DOMAIN", "https://ea-training-1-50a1c44f7233.herokuapp.com"
        )
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
        os.environ.setdefault("DOMAIN", "http://127.0.0.1:8000")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    # This allows easy placement of apps within the interior
    # bookstore_binht directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "bookstore_binht"))

    # Run SCSS compilation before collectstatic or runserver
    if len(sys.argv) > 1 and sys.argv[1] in ["collectstatic", "runserver"]:
        subprocess.run(["python", "compile_scss.py"], check=True)

    execute_from_command_line(sys.argv)
