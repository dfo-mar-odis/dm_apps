# Generated by Django 3.1.2 on 2021-01-26 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_auto_20210126_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='processstep',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
