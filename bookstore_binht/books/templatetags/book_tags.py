from django import template
from django.templatetags.static import static
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def star_rating(rating_dict):
    full_stars = rating_dict["full_stars"]
    half_star = rating_dict["half_star"]
    empty_stars = rating_dict["empty_stars"]

    stars_html = ""
    stars_html += (
        '<img src="{}" alt="Full Star" />'.format(static("images/star-fill.svg"))
        * full_stars
    )
    if half_star:
        stars_html += '<img src="{}" alt="Half Star" />'.format(
            static("images/star-half.svg"),
        )
    stars_html += (
        '<img src="{}" alt="Empty Star" />'.format(static("images/star.svg"))
        * empty_stars
    )

    return format_html("".join(stars_html))


@register.simple_tag
def star_distribution(isfull):
    starts_html = ""
    starts_html += (
        '<img src="{}" alt="Full Star" />'.format(static("images/star-fill.svg"))
        * isfull
    )
    starts_html += '<img src="{}" alt="Empty Star" />'.format(
        static("images/star.svg"),
    ) * (5 - isfull)
    return format_html("".join(starts_html))


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)


@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0


@register.filter
def multiply(value, arg):
    return float(value) * float(arg)
