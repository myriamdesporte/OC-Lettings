"""Tests of the oc_lettings_site main application."""

from django.urls import reverse


def test_index_page(client):
    """The home page is displayed with links to both sections."""
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert b'Welcome to Holiday Homes' in response.content
    assert b'href="/lettings/"' in response.content
    assert b'href="/profiles/"' in response.content
