# Generated by Django 2.2.2 on 2020-05-08 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20200508_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='geo_descr_eng',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Geographic description (English)'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='geo_descr_fre',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Geographic description (French)'),
        ),
    ]
