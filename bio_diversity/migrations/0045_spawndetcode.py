# Generated by Django 3.1.2 on 2020-12-09 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0044_auto_20201209_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpawnDetCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description (en)')),
                ('description_fr', models.TextField(blank=True, null=True, verbose_name='Description (fr)')),
                ('created_by', models.CharField(max_length=32, verbose_name='Created By')),
                ('created_date', models.DateField(verbose_name='Created Date')),
                ('min_val', models.DecimalField(decimal_places=5, max_digits=11, verbose_name='Minimum Value')),
                ('max_val', models.DecimalField(decimal_places=5, max_digits=11, verbose_name='Maximum Value')),
                ('spwn_subj_flag', models.BooleanField(verbose_name='Subjective?')),
                ('unit_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.unitcode', verbose_name='Units')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]