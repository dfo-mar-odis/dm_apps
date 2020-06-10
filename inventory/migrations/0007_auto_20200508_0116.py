# Generated by Django 2.2.2 on 2020-05-08 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_resource_paa_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='open_data_notes',
            field=models.TextField(blank=True, null=True, verbose_name='Open data notes'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='paa_items',
            field=models.ManyToManyField(blank=True, to='shared_models.PAAItem', verbose_name='Program Alignment Architecture (PAA) references'),
        ),
    ]
