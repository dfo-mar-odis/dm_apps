# Generated by Django 3.2 on 2021-05-04 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0012_auto_20210504_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttracking',
            name='is_in_house',
            field=models.BooleanField(default=False, verbose_name='Will translation be tackled in-house?'),
        ),
        migrations.AlterField(
            model_name='documenttracking',
            name='target_lang',
            field=models.IntegerField(blank=True, choices=[(1, 'English'), (2, 'French')], null=True, verbose_name='target language'),
        ),
    ]
