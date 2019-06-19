# Generated by Django 2.1.4 on 2019-04-10 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ios2', '0008_mooring_water_depth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mooring',
            name='water_depth',
        ),
        migrations.AddField(
            model_name='mooring',
            name='orientation',
            field=models.TextField(blank=True, null=True, verbose_name='Orientation'),
        ),
    ]
