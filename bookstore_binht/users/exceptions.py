from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class FutureDateValidationError(ValidationError):
    def __init__(self, *args, **kwargs):
        if not args:
            args = (_("Birthday date cannot be in the future."),)
        super().__init__(*args, **kwargs)
