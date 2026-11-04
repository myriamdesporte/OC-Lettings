"""Views of the profiles application."""

import logging

from django.http import Http404
from django.shortcuts import render

from .models import Profile

logger = logging.getLogger(__name__)


# Sed placerat quam in pulvinar commodo. Nullam laoreet consectetur ex, sed consequat libero
# pulvinar eget. Fusc
# faucibus, urna quis auctor pharetra, massa dolor cursus neque, quis dictum lacus d
def index(request):
    """Display the list of all profiles.

    Args:
        request: The HTTP request.

    Returns:
        HttpResponse: The rendered profiles list page.
    """
    profiles_list = Profile.objects.all()
    logger.info("Displaying profiles list (%d profiles)", len(profiles_list))
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


# Aliquam sed metus eget nisi tincidunt ornare accumsan eget lac
# laoreet neque quis, pellentesque dui. Nullam facilisis pharetra vulputate. Sed tincidunt, dolor
# id facilisis fringilla, eros leo tristique lacus,
# it. Nam aliquam dignissim congue. Pellentesque habitant morbi tristique senectus et netus et
# males
def profile(request, username):
    """Display the profile of a user identified by username.

    Args:
        request: The HTTP request.
        username (str): Username of the profile owner.

    Returns:
        HttpResponse: The rendered profile page.

    Raises:
        Http404: If no profile matches username.
    """
    try:
        profile = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        logger.warning("Profile not found: username=%s", username)
        raise Http404("Profile not found")

    logger.info("Displaying profile of %s", username)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
