# Generated by Django 3.1.2 on 2021-02-24 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0016_role_name_integer_choices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthstatus',
            name='nom',
        ),
        migrations.RemoveField(
            model_name='lifestage',
            name='nom',
        ),
        migrations.RemoveField(
            model_name='sex',
            name='nom',
        ),
        migrations.AlterField(
            model_name='certainty',
            name='code',
            field=models.IntegerField(blank=True, choices=[(1, 'Unsure'), (2, 'Probable'), (3, 'Certain')], null=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='healthstatus',
            name='name',
            field=models.IntegerField(blank=True, choices=[(1, 'Unknown'), (2, 'Healthy'), (3, 'All Points Bulletin (APB)'), (4, 'New Injury'), (5, 'Entangled'), (6, 'Distressed'), (7, 'Dead')], null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='lifestage',
            name='name',
            field=models.IntegerField(blank=True, choices=[(1, 'Unknown'), (2, 'Calf'), (3, 'Juvenile'), (3, 'Adult')], null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date and time'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='instrument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='observations', to='vault.instrument', verbose_name='instrument'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='longitude'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='observer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='observations', to='vault.person', verbose_name='observer'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='opportunistic',
            field=models.BooleanField(default=False, verbose_name='opportunistic?'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='outing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='observations', to='vault.outing', verbose_name='outing'),
        ),
        migrations.AlterField(
            model_name='sex',
            name='name',
            field=models.IntegerField(blank=True, choices=[(1, 'Unknown'), (2, 'Female'), (3, 'Male')], null=True, verbose_name='name'),
        ),
    ]