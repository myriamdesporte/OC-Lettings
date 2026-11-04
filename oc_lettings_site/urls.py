"""Root URL configuration of the oc_lettings_site project."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lettings/', include('lettings.urls')),
    path('profiles/', include('profiles.urls')),
    path('admin/', admin.site.urls),
]

# Route used to check the Sentry integration, never exposed in production.
if settings.DEBUG:
    urlpatterns.append(path('sentry-debug/', views.sentry_debug, name='sentry_debug'))
