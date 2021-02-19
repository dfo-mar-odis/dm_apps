# Generated by Django 3.1.2 on 2021-02-12 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0014_auto_20210211_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnelcode',
            name='initials',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Initials'),
        ),
        migrations.AlterField(
            model_name='envcondition',
            name='inst_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bio_diversity.instrument', verbose_name='Instrument'),
        ),
    ]