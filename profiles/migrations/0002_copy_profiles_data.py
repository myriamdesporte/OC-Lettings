"""Copy Profile data from oc_lettings_site to the profiles app."""

from django.db import migrations


def copy_profiles_data(apps, schema_editor):
    """Copy profiles from the old tables, keeping the same ids."""
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
    """Copy profiles back to the old tables (reverse migration)."""
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

    dependencies = [
        ('profiles', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_profiles_data, restore_profiles_data),
    ]
