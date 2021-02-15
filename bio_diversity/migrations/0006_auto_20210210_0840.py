# Generated by Django 3.1.2 on 2021-02-10 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0005_auto_20210205_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='anidetailxref',
            name='final_contx_flag',
            field=models.BooleanField(null=True, verbose_name='Final Container in movement'),
        ),
        migrations.AddField(
            model_name='groupdet',
            name='grpd_valid',
            field=models.BooleanField(default='True', verbose_name='Detail still valid?'),
        ),
        migrations.AddField(
            model_name='individualdet',
            name='indvd_valid',
            field=models.BooleanField(default='True', verbose_name='Detail still valid?'),
        ),
        migrations.AlterField(
            model_name='animaldetcode',
            name='max_val',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=11, null=True, verbose_name='Maximum Value'),
        ),
        migrations.AlterField(
            model_name='animaldetcode',
            name='min_val',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=11, null=True, verbose_name='Minimum Value'),
        ),
        migrations.AlterField(
            model_name='groupdet',
            name='det_val',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Value'),
        ),
        migrations.AlterField(
            model_name='individualdet',
            name='det_val',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Value'),
        ),
    ]