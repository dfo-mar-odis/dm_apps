# Generated by Django 2.1.4 on 2019-01-28 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scifi', '0016_auto_20190128_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount_paid_in_mrs',
            field=models.FloatField(blank=True, null=True, verbose_name='amount paid in MRS'),
        ),
    ]
