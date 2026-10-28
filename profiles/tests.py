"""Tests of the profiles application."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Profile


@pytest.fixture
def profile():
    """Create a user with its profile."""
    user = User.objects.create_user(username='johndoe', first_name='John')
    return Profile.objects.create(user=user, favorite_city='Paris')


@pytest.mark.django_db
def test_profiles_index_lists_profiles(client, profile):
    """The profiles index page displays the profile."""
    response = client.get(reverse('profiles:index'))
    assert response.status_code == 200
    assert b'johndoe' in response.content


@pytest.mark.django_db
def test_profile_detail_shows_user_data(client, profile):
    """The profile detail page shows the user data and favorite city."""
    response = client.get(reverse('profiles:profile', kwargs={'username': 'johndoe'}))
    assert response.status_code == 200
    assert b'John' in response.content
    assert b'Paris' in response.content


def test_profiles_urls_resolve():
    """The profiles URLs resolve to the expected paths."""
    assert reverse('profiles:index') == '/profiles/'
    assert reverse('profiles:profile', kwargs={'username': 'johndoe'}) == '/profiles/johndoe/'


@pytest.mark.django_db
def test_profile_str(profile):
    """A profile returns its username as a string."""
    assert str(profile) == 'johndoe'
