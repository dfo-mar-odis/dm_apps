# Generated by Django 3.1.2 on 2021-02-11 11:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared_models', '0004_auto_20210126_1540'),
        ('travel', '0019_auto_20210210_2249'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Request',
            new_name='TripRequest1',
        ),
    ]