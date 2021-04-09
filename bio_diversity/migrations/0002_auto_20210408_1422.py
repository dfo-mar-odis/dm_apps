# Generated by Django 3.1.6 on 2021-04-08 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='relc_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='bio_diversity.releasesitecode', verbose_name='Site Code'),
        ),
        migrations.AlterField(
            model_name='releasesitecode',
            name='rive_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sites', to='bio_diversity.rivercode', verbose_name='River'),
        ),
    ]
