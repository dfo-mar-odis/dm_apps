# Generated by Django 2.2.2 on 2020-04-29 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shared_models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province_eng', models.CharField(blank=True, max_length=255, null=True)),
                ('province_fre', models.CharField(blank=True, max_length=255, null=True)),
                ('abbrev', models.CharField(blank=True, max_length=10, null=True)),
                ('abbrev_fre', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nutrient_sample_id', models.IntegerField(blank=True, null=True, unique=True, verbose_name='nutrient sample ID')),
                ('timezone', models.CharField(blank=True, choices=[('AST', 'AST'), ('ADT', 'ADT'), ('UTC', 'UTC')], max_length=5, null=True)),
                ('start_date', models.DateTimeField(verbose_name='Start date / time (yyyy-mm-dd hh:mm)')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='End date / time (yyyy-mm-dd hh:mm)')),
                ('weather_notes', models.CharField(blank=True, max_length=1000, null=True)),
                ('rain_past_24_hours', models.BooleanField(default=False, verbose_name='Has it rained in the past 24 h?')),
                ('h2o_temperature_c', models.FloatField(blank=True, null=True, verbose_name='Water temperature (°C)')),
                ('salinity', models.FloatField(blank=True, null=True, verbose_name='Salinity (ppt)')),
                ('dissolved_o2', models.FloatField(blank=True, null=True, verbose_name='dissolved oxygen (mg/L)')),
                ('water_turbidity', models.IntegerField(blank=True, choices=[(1, 'Turbid'), (2, 'Clear')], null=True)),
                ('tide_state', models.CharField(blank=True, choices=[('h', 'High'), ('m', 'Mid'), ('l', 'Low')], max_length=5, null=True)),
                ('tide_direction', models.CharField(blank=True, choices=[('in', 'Incoming'), ('out', 'Outgoing')], max_length=5, null=True)),
                ('samplers', models.CharField(blank=True, max_length=1000, null=True)),
                ('percent_sand', models.FloatField(blank=True, null=True, verbose_name='Sand (%)')),
                ('percent_gravel', models.FloatField(blank=True, null=True, verbose_name='Gravel (%)')),
                ('percent_rock', models.FloatField(blank=True, null=True, verbose_name='Rock (%)')),
                ('percent_mud', models.FloatField(blank=True, null=True, verbose_name='Mud (%)')),
                ('visual_sediment_obs', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Visual sediment observations')),
                ('sav_survey_conducted', models.BooleanField(default=False, verbose_name='Was SAV survey conducted?')),
                ('excessive_green_algae_water', models.BooleanField(default=False, verbose_name='Excessive green algae in water?')),
                ('excessive_green_algae_shore', models.BooleanField(default=False, verbose_name='Excessive green algae on shore?')),
                ('unsampled_vegetation_inside', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Vegetation present inside sample area (underwater) but outside of quadrat')),
                ('unsampled_vegetation_outside', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Vegetation present outside of sample area (underwater)')),
                ('per_sediment_water_cont', models.FloatField(blank=True, null=True, verbose_name='sediment water content (%)')),
                ('per_sediment_organic_cont', models.FloatField(blank=True, null=True, verbose_name='sediment organic content (%)')),
                ('mean_sediment_grain_size', models.FloatField(blank=True, null=True, verbose_name='Mean sediment grain size (??)')),
                ('silicate', models.FloatField(blank=True, null=True, verbose_name='Silicate (µM)')),
                ('phosphate', models.FloatField(blank=True, null=True, verbose_name='Phosphate (µM)')),
                ('nitrates', models.FloatField(blank=True, null=True, verbose_name='NO3 + NO2(µM)')),
                ('nitrite', models.FloatField(blank=True, null=True, verbose_name='Nitrite (µM)')),
                ('ammonia', models.FloatField(blank=True, null=True, verbose_name='Ammonia (µM)')),
                ('notes', models.TextField(blank=True, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('month', models.IntegerField(blank=True, null=True)),
                ('last_modified', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-start_date', 'station'],
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='campsites', to='shared_models.Province')),
            ],
            options={
                'ordering': ['province', 'site'],
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name_eng', models.CharField(blank=True, max_length=255, null=True, verbose_name='english name')),
                ('common_name_fre', models.CharField(blank=True, max_length=255, null=True, verbose_name='french name')),
                ('scientific_name', models.CharField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('tsn', models.IntegerField(blank=True, null=True, verbose_name='ITIS TSN')),
                ('aphia_id', models.IntegerField(blank=True, null=True, verbose_name='AphiaID')),
                ('sav', models.BooleanField(default=False, verbose_name='Submerged aquatic vegetation (SAV)')),
                ('ais', models.BooleanField(default=False, verbose_name='Aquatic invasive species')),
                ('notes', models.TextField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['common_name_eng'],
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('latitude_n', models.FloatField(blank=True, null=True)),
                ('longitude_w', models.FloatField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('station_number', models.IntegerField(blank=True, null=True)),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='stations', to='camp.Site')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SpeciesObservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adults', models.IntegerField(blank=True, null=True)),
                ('yoy', models.IntegerField(blank=True, null=True, verbose_name='young of the year (YOY)')),
                ('total_non_sav', models.IntegerField(blank=True, null=True)),
                ('total_sav', models.FloatField(blank=True, null=True, verbose_name='SAV level')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sample_spp', to='camp.Sample')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sample_spp', to='camp.Species')),
            ],
            options={
                'unique_together': {('sample', 'species')},
            },
        ),
        migrations.AddField(
            model_name='sample',
            name='species',
            field=models.ManyToManyField(through='camp.SpeciesObservation', to='camp.Species'),
        ),
        migrations.AddField(
            model_name='sample',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='samples', to='camp.Station'),
        ),
        migrations.AlterUniqueTogether(
            name='sample',
            unique_together={('start_date', 'station')},
        ),
    ]
