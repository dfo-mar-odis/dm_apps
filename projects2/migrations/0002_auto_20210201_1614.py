# Generated by Django 3.1.2 on 2021-02-01 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upcomingdate',
            name='date',
            field=models.DateTimeField(),
        ),
    ]