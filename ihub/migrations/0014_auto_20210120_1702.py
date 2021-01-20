# Generated by Django 3.1.2 on 2021-01-20 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ihub', '0013_entry_proponent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entryperson',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ihub_entry_people', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
