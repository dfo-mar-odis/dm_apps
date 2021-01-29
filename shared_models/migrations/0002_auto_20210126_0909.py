# Generated by Django 3.1.2 on 2021-01-26 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared_models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shared_models_branch_admin', to=settings.AUTH_USER_MODEL, verbose_name='admin'),
        ),
        migrations.AddField(
            model_name='division',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shared_models_division_admin', to=settings.AUTH_USER_MODEL, verbose_name='admin'),
        ),
        migrations.AddField(
            model_name='region',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shared_models_region_admin', to=settings.AUTH_USER_MODEL, verbose_name='admin'),
        ),
        migrations.AddField(
            model_name='section',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shared_models_section_admin', to=settings.AUTH_USER_MODEL, verbose_name='admin'),
        ),
    ]