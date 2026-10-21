"""Admin registration of the lettings models."""

from django.contrib import admin

from .models import Address, Letting


admin.site.register(Letting)
admin.site.register(Address)
