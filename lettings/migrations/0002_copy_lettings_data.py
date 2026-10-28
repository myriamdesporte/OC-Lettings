"""Copy Address and Letting data from oc_lettings_site to the lettings app."""

from django.db import migrations


def copy_lettings_data(apps, schema_editor):
    """Copy address then lettings from the old tables, keeping the same ids."""
    OldAddress = apps.get_model('oc_lettings_site', 'Address')
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    Address = apps.get_model('lettings', 'Address')
    Letting = apps.get_model('lettings', 'Letting')

    Address.objects.bulk_create([
        Address(
            id=old.id,
            number=old.number,
            street=old.street,
            city=old.city,
            state=old.state,
            zip_code=old.zip_code,
            country_iso_code=old.country_iso_code,
        )
        for old in OldAddress.objects.all()
    ])
    Letting.objects.bulk_create([
        Letting(
            id=old.id,
            title=old.title,
            address_id=old.address_id,
        )
        for old in OldLetting.objects.all()
    ])


def restore_lettings_data(apps, schema_editor):
    """Copy address and lettings back to the old tables (reverse migration)."""
    OldAddress = apps.get_model('oc_lettings_site', 'Address')
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    Address = apps.get_model('lettings', 'Address')
    Letting = apps.get_model('lettings', 'Letting')

    OldAddress.objects.bulk_create([
        OldAddress(
            id=new.id,
            number=new.number,
            street=new.street,
            city=new.city,
            state=new.state,
            zip_code=new.zip_code,
            country_iso_code=new.country_iso_code,
        )
        for new in Address.objects.all()
    ])
    OldLetting.objects.bulk_create([
        OldLetting(
            id=new.id,
            title=new.title,
            address_id=new.address_id,
        )
        for new in Letting.objects.all()
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('lettings', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_lettings_data, restore_lettings_data),
    ]
