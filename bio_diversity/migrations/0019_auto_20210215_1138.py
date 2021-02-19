# Generated by Django 3.1.2 on 2021-02-15 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0018_auto_20210215_1105'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='envcondition',
            name='Environment_Condition_Uniqueness',
        ),
        migrations.AddConstraint(
            model_name='envcondition',
            constraint=models.UniqueConstraint(fields=('contx_id', 'loc_id', 'inst_id', 'envc_id', 'envsc_id'), name='Environment_Condition_Uniqueness'),
        ),
    ]