# Generated by Django 3.1.2 on 2021-01-08 16:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scuba', '0015_auto_20210108_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='interval',
            field=models.IntegerField(choices=[(1, '1 (0-5m)'), (2, '2 (5-10m)'), (3, '3 (10-15m)'), (4, '4 (15-20m)'), (5, '5 (20-25m)'), (6, '6 (25-30m)'), (7, '7 (30-35m)'), (8, '8 (35-40m)'), (9, '9 (40-45m)'), (10, '10 (45-50m)'), (11, '11 (50-55m)'), (12, '12 (55-60m)'), (13, '13 (60-65m)'), (14, '14 (65-70m)'), (15, '15 (70-75m)'), (16, '16 (75-80m)'), (17, '17 (80-85m)'), (18, '18 (85-90m)'), (19, '19 (90-95m)'), (20, '20 (95-100m)')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)], verbose_name='5m interval (1-20)'),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together={('dive', 'interval')},
        ),
    ]