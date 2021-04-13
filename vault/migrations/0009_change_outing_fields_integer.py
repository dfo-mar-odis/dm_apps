# Generated by Django 3.1.2 on 2021-02-16 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0008_make_outing_duration_calculated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outing',
            name='purpose',
            field=models.IntegerField(blank=True, choices=[(1, 'Broadscale Marine Mammal Survey'), (2, 'Science Multi-Species Survey'), (3, 'Fisheries Surveillance'), (4, 'Fisheries Management Support'), (5, 'Shipping Lane Surveillance'), (6, 'Whale Survey'), (7, 'Routine Patrol')], null=True, verbose_name='Purpose'),
        ),
        migrations.AlterField(
            model_name='outing',
            name='region',
            field=models.IntegerField(blank=True, choices=[(1, 'St. Lawrence Estuary'), (2, 'Northern GSL'), (3, 'Southern GSL'), (4, 'Cabot Strait'), (5, 'Western NFLD'), (6, 'Northern NFLD'), (7, 'Eastern NFLD'), (8, 'Southern NFLD'), (9, 'Eastern Scotian Shelf'), (10, 'Scotian Shelf'), (11, 'Western Scotian Shelf'), (12, 'Bay of Fundy')], null=True, verbose_name='Region'),
        ),
    ]