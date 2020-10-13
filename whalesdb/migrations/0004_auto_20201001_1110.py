# Generated by Django 2.2.13 on 2020-10-01 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whalesdb', '0003_auto_20201001_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rstrecordingstage',
            name='rst_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Rate (Hz)'),
        ),
    ]