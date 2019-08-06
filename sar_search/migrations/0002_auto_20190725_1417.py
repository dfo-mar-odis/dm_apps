# Generated by Django 2.2.2 on 2019-07-25 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0024_auto_20190715_1550'),
        ('sar_search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SARASchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=255)),
                ('nom', models.CharField(blank=True, max_length=255, null=True)),
                ('description_eng', models.CharField(blank=True, max_length=1000, null=True)),
                ('description_fre', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SpeciesStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=255)),
                ('nom', models.CharField(blank=True, max_length=255, null=True)),
                ('description_eng', models.CharField(blank=True, max_length=1000, null=True)),
                ('description_fre', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Taxon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbrev', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('nom', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.RemoveField(
            model_name='species',
            name='life_stage_eng',
        ),
        migrations.RemoveField(
            model_name='species',
            name='life_stage_fre',
        ),
        migrations.AddField(
            model_name='species',
            name='population_eng',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='population (English)'),
        ),
        migrations.AddField(
            model_name='species',
            name='population_fre',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='population (French)'),
        ),
        migrations.AlterField(
            model_name='species',
            name='common_name_eng',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name (English)'),
        ),
        migrations.AlterField(
            model_name='species',
            name='common_name_fre',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name (French)'),
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('nom', models.CharField(blank=True, max_length=255, null=True)),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='counties', to='shared_models.Province')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='species',
            name='sara_schedule',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='spp', to='sar_search.SARASchedule', verbose_name='SARA schedule'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='species',
            name='species_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='spp', to='sar_search.SpeciesStatus', verbose_name='COSEWIC species status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='species',
            name='taxon',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='spp', to='sar_search.Taxon'),
            preserve_default=False,
        ),
    ]
