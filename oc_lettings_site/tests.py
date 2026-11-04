"""Tests of the oc_lettings_site application: home page, error pages and admin."""

import pytest
from django.test import Client
from django.urls import resolve, reverse
from pytest_django.asserts import assertTemplateUsed

from . import views


def test_index_url():
    """The home URL is '/' and uses the index view."""
    assert reverse('index') == '/'
    assert resolve('/').func == views.index


def test_index_view(client):
    """The home page is displayed with links to both sections."""
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'index.html')
    assert b'Welcome to Holiday Homes' in response.content
    assert b'href="/lettings/"' in response.content
    assert b'href="/profiles/"' in response.content


@pytest.mark.django_db
def test_custom_404_page(client):
    """An unknown URL returns the custom 404 page."""
    response = client.get('/unknown-page/')
    assert response.status_code == 404
    assertTemplateUsed(response, '404.html')
    assert b'404 - Page not found' in response.content


@pytest.mark.django_db
def test_custom_500_page(monkeypatch):
    """An unexpected server error displays the custom 500 page."""
    def raise_error(*args, **kwargs):
        """Simulate an unexpected error during view execution."""
        raise RuntimeError('Simulated error')

    monkeypatch.setattr('lettings.views.Letting.objects.all', raise_error)
    client = Client(raise_request_exception=False)
    response = client.get('/lettings/')
    assert response.status_code == 500
    assertTemplateUsed(response, '500.html')
    assert b'500 - Server error' in response.content


@pytest.mark.django_db
def test_admin_shows_correct_plurals(admin_client):
    """The admin index shows 'Addresses' and never 'Addresss'."""
    response = admin_client.get('/admin/')
    assert response.status_code == 200
    assert b'Addresses' in response.content
    assert b'Addresss' not in response.content
