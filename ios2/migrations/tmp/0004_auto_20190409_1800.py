# Generated by Django 2.1.4 on 2019-04-09 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ios2', '0003_auto_20190409_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicehistory',
            name='category',
            field=models.IntegerField(choices=[('Calibration', 'Calibration'), ('Repair', 'Repair')], verbose_name='category'),
        ),
    ]
