# Generated by Django 3.1.6 on 2021-04-08 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whalebrary', '0007_auto_20210408_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]