# Generated by Django 3.1.2 on 2020-12-01 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0030_remove_organization_province'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['country', 'location_en']},
        ),
    ]