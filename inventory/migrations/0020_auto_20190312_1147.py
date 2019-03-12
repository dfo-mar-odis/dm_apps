# Generated by Django 2.1.4 on 2019-03-12 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_resource_translation_needed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='language',
            field=models.IntegerField(blank=True, choices=[(1, 'English'), (2, 'French')], null=True, verbose_name='language preference'),
        ),
        migrations.AlterField(
            model_name='person',
            name='organization',
            field=models.ForeignKey(blank=True, default=6, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Organization'),
        ),
    ]
