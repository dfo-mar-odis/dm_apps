# Generated by Django 3.1.2 on 2021-02-16 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travel', '0022_auto_20210211_0908'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='traveller',
            options={'ordering': ['first_name', 'last_name'], 'verbose_name': 'trip request'},
        ),
        migrations.AddField(
            model_name='triprequest1',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='triprequest1',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='triprequest1',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='travel_requests_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='triprequest1',
            name='funding_source',
            field=models.TextField(blank=True, null=True, verbose_name='what is the DFO funding source?'),
        ),
        migrations.AlterField(
            model_name='tripreviewer',
            name='status',
            field=models.IntegerField(choices=[(23, 'Draft'), (24, 'Queued'), (25, 'Pending'), (26, 'Complete'), (42, 'Skipped'), (44, 'Cancelled')], default=23, verbose_name='review status'),
        ),
    ]