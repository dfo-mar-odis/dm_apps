# Generated by Django 2.1.4 on 2019-05-09 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0025_project_priority_area_or_threat'),
    ]

    operations = [
        migrations.AddField(
            model_name='priorityareaorthreat',
            name='type',
            field=models.IntegerField(blank=True, choices=[(1, 'Threat'), (2, 'Priority area')], null=True),
        ),
    ]
