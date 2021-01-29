# Generated by Django 3.1.2 on 2021-01-26 19:40

from django.db import migrations, models
import travel.models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0006_referencematerial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referencematerial',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='url'),
        ),
        migrations.AlterField(
            model_name='referencematerial',
            name='file_en',
            field=models.FileField(blank=True, null=True, upload_to=travel.models.ref_mat_directory_path, verbose_name='file attachment (English)'),
        ),
    ]