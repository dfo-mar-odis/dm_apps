# Generated by Django 2.2.2 on 2020-01-07 20:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectyear',
            name='expenditure_initiation_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 1, 0, 0), null=True),
        ),
    ]
