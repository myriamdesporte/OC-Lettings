"""Tests of the profiles application: models, URLs and views."""

import pytest
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from pytest_django.asserts import assertTemplateUsed

from . import views
from .models import Profile


@pytest.fixture
def profile():
    """Create and return a Profile instance linked to a test user."""
    user = User.objects.create_user(
        username='johndoe', first_name='John', last_name='Doe', email='john@doe.com',
    )
    return Profile.objects.create(user=user, favorite_city='Paris')


# Models

@pytest.mark.django_db
def test_profile_str(profile):
    """A profile is represented by its username."""
    assert str(profile) == profile.user.username


@pytest.mark.django_db
def test_deleting_user_deletes_profile(profile):
    """Deleting a user automatically deletes its associated profile (CASCADE)."""
    profile.user.delete()
    assert not Profile.objects.exists()


def test_profile_plural_name():
    """The plural name of Profile is 'profiles'."""
    assert Profile._meta.verbose_name_plural == 'profiles'


# URLs

def test_index_url():
    """The profiles index URL is '/profiles/' and uses the index view."""
    assert reverse('profiles:index') == '/profiles/'
    assert resolve('/profiles/').func == views.index


def test_profile_url():
    """The profile URL is '/profiles/<username>/' and uses the profile view."""
    assert reverse('profiles:profile', kwargs={'username': 'johndoe'}) == '/profiles/johndoe/'
    assert resolve('/profiles/johndoe/').func == views.profile


# Views

@pytest.mark.django_db
def test_index_view_lists_profiles(client, profile):
    """The index view renders every profile with a link to its page."""
    response = client.get(reverse('profiles:index'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'profiles/index.html')
    assert list(response.context['profiles_list']) == [profile]

    profile_url = reverse(
        'profiles:profile',
        kwargs={'username': profile.user.username},
    )
    assert f'href="{profile_url}"'.encode() in response.content


@pytest.mark.django_db
def test_index_view_without_profiles(client):
    """The index view displays a message when no profiles are available."""
    response = client.get(reverse('profiles:index'))
    assert response.status_code == 200
    assert b'No profiles are available.' in response.content


@pytest.mark.django_db
def test_profile_view_shows_details(client, profile):
    """The profile view displays the user's details and favorite city."""
    response = client.get(
        reverse(
            'profiles:profile',
            kwargs={'username': profile.user.username},
        )
    )
    assert response.status_code == 200
    assertTemplateUsed(response, 'profiles/profile.html')
    assert response.context['profile'] == profile

    for value in (
        profile.user.first_name,
        profile.user.last_name,
        profile.user.email,
        profile.favorite_city,
    ):
        assert value.encode() in response.content


@pytest.mark.django_db
def test_profile_view_unknown_username_returns_404(client):
    """The profile view returns a 404 for an unknown username."""
    response = client.get(reverse('profiles:profile', kwargs={'username': 'unknown'}))
    assert response.status_code == 404


# Integration

@pytest.mark.django_db
def test_navigation_from_index_to_profile(client, profile):
    """Users can navigate from the profiles index to a profile detail page and back."""
    detail_url = reverse(
        'profiles:profile',
        kwargs={'username': profile.user.username},
    )

    index = client.get(reverse('profiles:index'))
    assert index.status_code == 200
    assert f'href="{detail_url}"'.encode() in index.content

    detail = client.get(detail_url)
    assert detail.status_code == 200
    assert b'href="/profiles/"' in detail.content
