# Generated by Django 2.0.4 on 2018-11-19 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0016_auto_20181119_1546'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sample',
            old_name='disolved_o2',
            new_name='dissolved_o2',
        ),
    ]
