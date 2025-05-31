from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def items_per_page_options(selected_value=None):
    options = [10, 20, 30, 40]
    options_html = []

    for value in options:
        selected = " selected" if str(value) == str(selected_value) else ""
        options_html.append(
            format_html('<option value="{}"{}>{}</option>', value, selected, value),
        )

    return format_html("".join(options_html))


@register.simple_tag
def render_page_link(page_obj, page_type, sm_display, **kwargs):
    """
    Renders a pagination link.

    Args:
        page_obj: The Django pagination object.
        page_type: The type of link ('first', 'previous', 'next', 'last').
        **kwargs: Additional attributes to add to the <a> tag.

    Returns:
        The rendered HTML for the pagination link using format_html.
    """

    if page_type == "first":
        disabled = not page_obj.number > 1
        page_number = 1
        text = (
            (
                "First",
                """
        <svg xmlns="http://www.w3.org/2000/svg"
             width="20" height="16" fill="currentColor"
             class="bi bi-chevron-double-left" viewBox="0 0 20 16">
            <path fill="none" stroke="currentColor" stroke-width="1.5"
                  stroke-linecap="miter"
                  stroke-linejoin="miter" fill-rule="evenodd"
                  d="M8.354 1.646a.5.5 0 0 1 0 .708L2.707 8l5.647
                     5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1
                     0-.708l6-6a.5.5 0 0 1 .708 0"/>
            <path fill="none" stroke="currentColor" stroke-width="1.5"
                  stroke-linecap="miter"
                  stroke-linejoin="miter" fill-rule="evenodd"
                  d="M14.354 1.646a.5.5 0 0 1 0 .708L8.707 8l5.647
                     5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1
                     0-.708l6-6a.5.5 0 0 1 .708 0"/>
        </svg>
        """,
            )
            if sm_display
            else "First"
        )
    elif page_type == "previous":
        disabled = not page_obj.number > 1
        page_number = page_obj.previous_page_number() if page_obj.has_previous() else 1
        text = (
            (
                "Prev",
                """
        <svg xmlns="http://www.w3.org/2000/svg"
             width="20" height="16" fill="currentColor"
             class="bi bi-chevron-left" viewBox="0 0 20 16">
            <path fill="none" stroke="currentColor" stroke-width="1.5"
                  stroke-linecap="miter"
                  stroke-linejoin="miter" fill-rule="evenodd"
                  d="M12.354 1.646a.5.5 0 0 1 0 .708L6.707 8l5.647
                     5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1
                     0-.708l6-6a.5.5 0 0 1 .708 0"/>
        </svg>
        """,
            )
            if sm_display
            else "Prev"
        )
    elif page_type == "next":
        disabled = not page_obj.number < page_obj.paginator.num_pages
        page_number = (
            page_obj.next_page_number()
            if page_obj.has_next()
            else page_obj.paginator.num_pages
        )
        text = (
            (
                "Next",
                """
        <svg xmlns="http://www.w3.org/2000/svg"
             width="20" height="16" fill="currentColor"
             class="bi bi-chevron-right" viewBox="0 0 20 16">
            <path fill="none" stroke="currentColor"
                  stroke-width="1.5" stroke-linecap="miter"
                  stroke-linejoin="miter" fill-rule="evenodd"
                  d="M7.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0
                     1 0 .708l-6 6a.5.5 0 0 1-.708-.708L13.293 8
                     7.646 2.354a.5.5 0 0 1 0-.708"/>
        </svg>
        """,
            )
            if sm_display
            else "Next"
        )
    elif page_type == "last":
        disabled = not page_obj.number < page_obj.paginator.num_pages
        page_number = page_obj.paginator.num_pages
        text = (
            (
                "Last",
                """
        <svg xmlns="http://www.w3.org/2000/svg"
             width="20" height="16" fill="currentColor"
             class="bi bi-chevron-double-right" viewBox="0 0 20 16">
            <path fill="none" stroke="currentColor"
                  stroke-width="1.5" stroke-linecap="miter"
                  stroke-linejoin="miter" fill-rule="evenodd"
                  d="M5.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0
                  1 0 .708l-6 6a.5.5 0 0 1-.708-.708L11.293 8
                  5.646 2.354a.5.5 0 0 1 0-.708"/>
            <path fill="none" stroke="currentColor"
                  stroke-width="1.5" stroke-linecap="miter"
                  stroke-linejoin="miter" fill-rule="evenodd"
                  d="M11.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0
                     1 0 .708l-6 6a.5.5 0 0 1-.708-.708L17.293 8
                     11.646 2.354a.5.5 0 0 1 0-.708"/>
        </svg>
        """,
            )
            if sm_display
            else "Last"
        )
    li_class = "page-item me-sm-1" if sm_display else "page-item ms-3"
    if page_type == "next":
        li_class += " ms-sm-1"

    if disabled:
        return format_html(
            f"""
            <li class="{li_class} disabled">
                <a class="page-link" href="#" tabindex="-1" aria-disabled="true">
                    <span class="aria-hidden d-none d-lg-block">{text[0]}</span>
                    <span class="aria-hidden d-none d-lg-none d-sm-block">
                        {text[1]}
                    </span>
                </a>
            </li>
            """
            if sm_display
            else f"""
            <li class="{li_class} disabled px-0">
                <a class="page-link btn btn-page-disabled"
                   href="#"
                   tabindex="-1"
                   aria-disabled="true">
                    {text}
                </a>
            </li>
            """,
        )

    get_params = "&".join(
        [
            f"{key}={value}"
            for key, value in kwargs["request"].GET.items()
            if key != "page"
        ],
    )
    href = f"?{get_params}&page={page_number}" if get_params else f"?page={page_number}"
    return format_html(
        f"""
        <li class="{li_class}">
            <a class="page-link" href="{href}">
                <span class="aria-hidden d-none d-lg-block">{text[0]}</span>
                <span class="aria-hidden d-none d-lg-none d-sm-block">
                    {text[1]}
                </span>
            </a>
        </li>
        """
        if sm_display
        else f"""
        <li class="{li_class} px-0">
            <a class="page-link btn btn-page" href="{href}">
                {text}
            </a>
        </li>
        """,
    )
