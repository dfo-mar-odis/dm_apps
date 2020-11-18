# Generated by Django 2.2.2 on 2020-07-14 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whalebrary', '0009_auto_20200713_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='confirm_received',
        ),
        migrations.AddField(
            model_name='order',
            name='cost',
            field=models.FloatField(blank=True, null=True, verbose_name='order cost'),
        ),
    ]
