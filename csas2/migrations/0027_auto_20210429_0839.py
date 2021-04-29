# Generated by Django 3.2 on 2021-04-29 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('csas2', '0026_auto_20210429_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='termsofreference',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='termsofreference',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='termsofreference_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='termsofreference',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='termsofreference',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='termsofreference_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
