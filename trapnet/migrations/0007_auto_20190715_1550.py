# Generated by Django 2.2.2 on 2019-07-15 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trapnet', '0006_trap_samplers'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrapType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('nom', models.CharField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='trap',
            name='min_air_temp',
            field=models.FloatField(blank=True, null=True, verbose_name='Water temperature (°C)'),
        ),
        migrations.AlterField(
            model_name='riversite',
            name='elevation_m',
            field=models.FloatField(blank=True, null=True, verbose_name='elevation (m)'),
        ),
        migrations.AlterField(
            model_name='riversite',
            name='name',
            field=models.CharField(max_length=255, verbose_name='site name'),
        ),
        migrations.AddField(
            model_name='trap',
            name='trap_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='traps', to='trapnet.TrapType'),
        ),
    ]
