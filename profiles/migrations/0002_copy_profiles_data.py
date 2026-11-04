"""Copy Profile data from oc_lettings_site to the profiles app."""

from django.db import migrations


def copy_profiles_data(apps, schema_editor):
    """Copy profiles from the old table, keeping the same ids.

    Args:
        apps: Registry of the historical models.
        schema_editor: Database schema editor (unused).
    """
    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    Profile = apps.get_model('profiles', 'Profile')

    Profile.objects.bulk_create([
        Profile(
            id=old.id,
            user_id=old.user_id,
            favorite_city=old.favorite_city,
        )
        for old in OldProfile.objects.all()
    ])


def restore_profiles_data(apps, schema_editor):
    """Copy profiles back to the old table (reverse migration).

    Args:
        apps: Registry of the historical models.
        schema_editor: Database schema editor (unused).
    """
    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    Profile = apps.get_model('profiles', 'Profile')

    OldProfile.objects.bulk_create([
        OldProfile(
            id=new.id,
            user_id=new.user_id,
            favorite_city=new.favorite_city,
        )
        for new in Profile.objects.all()
    ])


class Migration(migrations.Migration):
    """Copy the profiles data from the old table."""

    dependencies = [
        ('profiles', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_profiles_data, restore_profiles_data),
    ]
