"""Tests of the oc_lettings_site application: home page, error pages and admin."""

import logging
import os
import subprocess
import sys

import pytest
from django.conf import settings
from django.test import Client
from django.urls import resolve, reverse
from pytest_django.asserts import assertTemplateUsed

from . import settings as settings_module
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


def test_sentry_debug_view_logs_and_raises(rf, caplog):
    """The Sentry test view writes an ERROR log then raises an error."""
    with pytest.raises(ZeroDivisionError):
        views.sentry_debug(rf.get('/sentry-debug/'))
    assert 'Sentry test' in caplog.text
    assert caplog.records[-1].levelno == logging.ERROR


@pytest.mark.django_db
def test_sentry_debug_url_hidden_when_debug_is_false(client):
    """The Sentry test URL is not available when DEBUG is False."""
    assert client.get('/sentry-debug/').status_code == 404


def test_env_bool(monkeypatch):
    """env_bool reads true/false values and falls back to the default."""
    monkeypatch.setenv('TEST_FLAG', 'True')
    assert settings_module.env_bool('TEST_FLAG') is True
    monkeypatch.setenv('TEST_FLAG', '0')
    assert settings_module.env_bool('TEST_FLAG', default=True) is False
    monkeypatch.delenv('TEST_FLAG')
    assert settings_module.env_bool('TEST_FLAG', default=True) is True


def test_env_list(monkeypatch):
    """env_list splits on commas and ignores spaces and empty items."""
    monkeypatch.setenv('TEST_HOSTS', ' a.com, b.com ,,')
    assert settings_module.env_list('TEST_HOSTS') == ['a.com', 'b.com']
    assert settings_module.env_list('MISSING_VARIABLE', default='x') == ['x']


def run_settings(**env):
    """Load the Django settings in a fresh process with only the given variables."""
    # Empty SENTRY_DSN: a value from the local .env file must not enable Sentry here.
    base = {
        'PATH': os.environ['PATH'],
        'DJANGO_SETTINGS_MODULE': 'oc_lettings_site.settings',
        'SENTRY_DSN': '',
    }
    code = 'from django.conf import settings; print(settings.DEBUG, settings.ALLOWED_HOSTS)'
    return subprocess.run(
        [sys.executable, '-c', code], cwd=settings.BASE_DIR,
        env={**base, **env}, capture_output=True, text=True,
    )


def test_production_settings_require_secret_key():
    """In production, the site refuses to start without DJANGO_SECRET_KEY."""
    result = run_settings(DJANGO_DEBUG='False', DJANGO_SECRET_KEY='')
    assert result.returncode != 0
    assert 'DJANGO_SECRET_KEY' in result.stderr


def test_production_settings_read_environment():
    """In production, settings come from the environment, including the Render host."""
    result = run_settings(
        DJANGO_DEBUG='False', DJANGO_SECRET_KEY='test-key',
        DJANGO_ALLOWED_HOSTS='example.com', RENDER_EXTERNAL_HOSTNAME='app.onrender.com',
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "False ['example.com', 'app.onrender.com']"
