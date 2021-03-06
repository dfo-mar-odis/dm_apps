# Generated by Django 3.1.2 on 2021-02-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20210205_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitee',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='invitee',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='phone'),
        ),
    ]
