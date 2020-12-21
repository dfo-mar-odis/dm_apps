# Generated by Django 3.1.2 on 2020-12-11 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0054_auto_20201211_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spawning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=32, verbose_name='Created By')),
                ('created_date', models.DateField(verbose_name='Created Date')),
                ('spwn_date', models.DateField(verbose_name='Date of spawning')),
                ('est_fecu', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Estimated Fecundity')),
                ('comments', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Comments')),
                ('pair_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.pairing', verbose_name='Pairing')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]