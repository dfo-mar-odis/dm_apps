# Generated by Django 2.1.4 on 2019-03-06 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_auto_20190306_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='translation_needed',
            field=models.BooleanField(default=True, verbose_name='translation needed'),
        ),
    ]
