# Generated by Django 3.1.2 on 2021-01-15 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scuba', '0021_auto_20210115_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='transect',
            name='end_latitude_d',
            field=models.IntegerField(blank=True, null=True, verbose_name='end latitude (degrees)'),
        ),
        migrations.AddField(
            model_name='transect',
            name='end_latitude_mm',
            field=models.FloatField(blank=True, null=True, verbose_name='end latitude (minutes)'),
        ),
        migrations.AddField(
            model_name='transect',
            name='end_longitude_d',
            field=models.IntegerField(blank=True, null=True, verbose_name='end longitude (degrees)'),
        ),
        migrations.AddField(
            model_name='transect',
            name='end_longitude_mm',
            field=models.FloatField(blank=True, null=True, verbose_name='end longitude (minutes)'),
        ),
        migrations.AddField(
            model_name='transect',
            name='start_latitude_d',
            field=models.IntegerField(blank=True, null=True, verbose_name='start latitude (degrees)'),
        ),
        migrations.AddField(
            model_name='transect',
            name='start_latitude_mm',
            field=models.FloatField(blank=True, null=True, verbose_name='start latitude (minutes)'),
        ),
        migrations.AddField(
            model_name='transect',
            name='start_longitude_d',
            field=models.IntegerField(blank=True, null=True, verbose_name='start longitude (degrees)'),
        ),
        migrations.AddField(
            model_name='transect',
            name='start_longitude_mm',
            field=models.FloatField(blank=True, null=True, verbose_name='start longitude (minutes)'),
        ),
        migrations.AlterField(
            model_name='transect',
            name='end_latitude',
            field=models.FloatField(blank=True, editable=False, null=True, verbose_name='end latitude (decimal degrees)'),
        ),
        migrations.AlterField(
            model_name='transect',
            name='end_longitude',
            field=models.FloatField(blank=True, editable=False, null=True, verbose_name='end longitude (decimal degrees)'),
        ),
        migrations.AlterField(
            model_name='transect',
            name='start_latitude',
            field=models.FloatField(blank=True, editable=False, null=True, verbose_name='start latitude (decimal degrees)'),
        ),
        migrations.AlterField(
            model_name='transect',
            name='start_longitude',
            field=models.FloatField(blank=True, editable=False, null=True, verbose_name='start longitude (decimal degrees)'),
        ),
    ]