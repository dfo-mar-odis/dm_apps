# Generated by Django 2.2.2 on 2020-02-06 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whalesdb', '0002_auto_20200124_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mormooringsetup',
            name='mor_additional_equipment',
            field=models.TextField(blank=True, null=True, verbose_name='Equipment'),
        ),
        migrations.AlterField(
            model_name='mormooringsetup',
            name='mor_general_moor_description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='mormooringsetup',
            name='more_notes',
            field=models.TextField(blank=True, null=True, verbose_name='Notes'),
        ),
    ]
