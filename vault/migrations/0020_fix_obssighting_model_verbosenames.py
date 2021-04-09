# Generated by Django 3.1.2 on 2021-02-25 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0019_fix_individualident_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observationsighting',
            name='certainty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='observation_sightings', to='vault.certainty', verbose_name='certainty'),
        ),
        migrations.AlterField(
            model_name='observationsighting',
            name='health_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='observation_sightings', to='vault.healthstatus', verbose_name='health status'),
        ),
        migrations.AlterField(
            model_name='observationsighting',
            name='known_individual',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='observation_sightings', to='vault.individualidentification', verbose_name='known individual'),
        ),
        migrations.AlterField(
            model_name='observationsighting',
            name='life_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='observation_sightings', to='vault.lifestage', verbose_name='life_stage'),
        ),
        migrations.AlterField(
            model_name='observationsighting',
            name='sex',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='observation_sightings', to='vault.sex', verbose_name='sex'),
        ),
        migrations.AlterField(
            model_name='observationsighting',
            name='species',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='observation_sightings', to='vault.species', verbose_name='species'),
        ),
    ]
