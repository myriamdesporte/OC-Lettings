"""Tests of the lettings application: models, URLs and views."""

import logging
import pytest
from django.urls import resolve, reverse
from pytest_django.asserts import assertTemplateUsed

from . import views
from .models import Address, Letting


@pytest.fixture
def address():
    """Create and return an Address instance for testing."""
    return Address.objects.create(
        number=7, street='Bedford Street', city='Brunswick',
        state='GA', zip_code=31525, country_iso_code='USA',
    )


@pytest.fixture
def letting(address):
    """Create and return a Letting instance linked to a test Address."""
    return Letting.objects.create(title='Green Haus', address=address)


# Models

@pytest.mark.django_db
def test_address_str(address):
    """An address is represented by its number and street."""
    assert str(address) == f'{address.number} {address.street}'


@pytest.mark.django_db
def test_letting_str(letting):
    """A letting is represented by its title."""
    assert str(letting) == letting.title


def test_address_plural_name():
    """The plural name of Address is 'addresses' (not 'addresss')."""
    assert Address._meta.verbose_name_plural == 'addresses'


@pytest.mark.django_db
def test_deleting_address_deletes_letting(letting):
    """Deleting an address automatically deletes its associated lettings (CASCADE)."""
    letting.address.delete()
    assert not Letting.objects.exists()


# URLs

def test_index_url():
    """The lettings index URL is '/lettings/' and uses the index view."""
    assert reverse('lettings:index') == '/lettings/'
    assert resolve('/lettings/').func == views.index


def test_letting_url():
    """The letting URL is '/lettings/<letting_id>/' and uses the letting view."""
    assert reverse('lettings:letting', kwargs={'letting_id': 1}) == '/lettings/1/'
    assert resolve('/lettings/1/').func == views.letting


# Views

@pytest.mark.django_db
def test_index_view_lists_lettings(client, letting):
    """The index view renders every letting with a link to its page."""
    response = client.get(reverse('lettings:index'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'lettings/index.html')
    assert list(response.context['lettings_list']) == [letting]

    letting_url = reverse(
        'lettings:letting',
        kwargs={'letting_id': letting.pk},
    )
    assert f'href="{letting_url}"'.encode() in response.content


@pytest.mark.django_db
def test_index_view_without_lettings(client):
    """The index view displays a message when no lettings are available."""
    response = client.get(reverse('lettings:index'))
    assert response.status_code == 200
    assert b'No lettings are available.' in response.content


@pytest.mark.django_db
def test_letting_view_shows_details(client, letting):
    """The letting view renders the title and the full address."""
    response = client.get(reverse('lettings:letting', kwargs={'letting_id': letting.pk}))
    assert response.status_code == 200
    assertTemplateUsed(response, 'lettings/letting.html')
    assert response.context['title'] == letting.title
    assert response.context['address'] == letting.address

    expected_location = (
        f'{letting.address.city}, '
        f'{letting.address.state} '
        f'{letting.address.zip_code}'
    )
    assert expected_location.encode() in response.content


@pytest.mark.django_db
def test_letting_view_unknown_id_returns_404(client):
    """The letting view returns a 404 response for an unknown letting ID."""
    response = client.get(reverse('lettings:letting', kwargs={'letting_id': 999}))
    assert response.status_code == 404


# Logging

@pytest.mark.django_db
def test_letting_view_logs_info(client, letting, caplog):
    """Displaying a letting writes an INFO log with its id and title."""
    with caplog.at_level(logging.INFO, logger='lettings'):
        client.get(reverse('lettings:letting', kwargs={'letting_id': letting.pk}))
    assert f'Displaying letting {letting.pk} ({letting.title})' in caplog.text


@pytest.mark.django_db
def test_unknown_letting_logs_warning(client, caplog):
    """An unknown letting id writes a WARNING log with the id."""
    client.get(reverse('lettings:letting', kwargs={'letting_id': 999}))
    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert any('letting_id=999' in r.getMessage() for r in warnings)


# Integration

@pytest.mark.django_db
def test_navigation_from_index_to_letting(client, letting):
    """Users can navigate from the lettings index to a letting detail page and back."""
    detail_url = reverse(
        'lettings:letting',
        kwargs={'letting_id': letting.pk},
    )

    index = client.get(reverse('lettings:index'))
    assert index.status_code == 200
    assert f'href="{detail_url}"'.encode() in index.content

    detail = client.get(detail_url)
    assert detail.status_code == 200
    assert b'href="/lettings/"' in detail.content
