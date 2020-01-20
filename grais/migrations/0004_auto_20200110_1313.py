# Generated by Django 2.2.2 on 2020-01-10 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0003_auto_20191211_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='common_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='common name (English)'),
        ),
        migrations.AlterField(
            model_name='species',
            name='common_name_fra',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='common name (French)'),
        ),
    ]
