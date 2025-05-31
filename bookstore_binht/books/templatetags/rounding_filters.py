from django import template

register = template.Library()


@register.filter(name="round_rating")
def round_rating(value):
    """Round the rating to the nearest 0.5 or 1.0."""
    try:
        value = float(value)
        return round(value * 2) / 2
    except (ValueError, TypeError):
        return 0
