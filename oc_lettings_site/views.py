"""Views of the oc_lettings_site main application."""

import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


# Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque molestie quam lobortis leo
# consectetur ullamcorper non id est. Praesent dictum, nulla eget feugiat sagittis, sem mi
# convallis eros,
# vitae dapibus nisi lorem dapibus sem. Maecenas pharetra purus ipsum, eget consequat ipsum
# lobortis quis. Phasellus eleifend ex auctor venenatis tempus.
# Aliquam vitae erat ac orci placerat luctus. Nullam elementum urna nisi, pellentesque iaculis enim
# cursus in. Praesent volutpat porttitor magna, non finibus neque cursus id.
def index(request):
    """Display the home page.

        Args:
            request: The HTTP request.

        Returns:
            HttpResponse: The rendered home page.
        """
    return render(request, 'index.html')


def sentry_debug(request):
    """Raise an error on purpose to check that Sentry captures it.

    Only routed when DEBUG is True (see urls.py).

    Args:
        request: The HTTP request.

    Raises:
        ZeroDivisionError: Always.
    """
    logger.error("Sentry test: an error log sent on purpose")
    return 1 / 0
