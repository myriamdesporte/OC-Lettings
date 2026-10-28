"""Tests of the lettings application."""

import pytest
from django.urls import reverse

from .models import Address, Letting


@pytest.fixture
def letting():
    """Create a letting with its address."""
    address = Address.objects.create(
        number=7, street='Bedford Street', city='Brunswick',
        state='GA', zip_code=31525, country_iso_code='USA',
    )
    return Letting.objects.create(title='Green Haus', address=address)


@pytest.mark.django_db
def test_lettings_index_lists_lettings(client, letting):
    """The lettings index page displays the letting."""
    response = client.get(reverse('lettings:index'))
    assert response.status_code == 200
    assert b'Green Haus' in response.content


@pytest.mark.django_db
def test_letting_detail_shows_address(client, letting):
    """The letting detail page shows the title and the address."""
    response = client.get(reverse('lettings:letting', kwargs={'letting_id': letting.pk}))
    assert response.status_code == 200
    assert b'Green Haus' in response.content
    assert b'7 Bedford Street' in response.content


def test_lettings_urls_resolve():
    """The lettings URLs resolve to the expected paths."""
    assert reverse('lettings:index') == '/lettings/'
    assert reverse('lettings:letting', kwargs={'letting_id': 1}) == '/lettings/1/'


@pytest.mark.django_db
def test_lettings_models_str(letting):
    """The Address and Letting models return their expected string representations."""
    assert str(letting.address) == '7 Bedford Street'
    assert str(letting) == 'Green Haus'
