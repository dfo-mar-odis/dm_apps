# Generated by Django 3.2 on 2021-04-21 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whalesdb', '0012_auto_20210408_1422'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emmmakemodel',
            options={'ordering': ('emm_make', 'emm_model')},
        ),
        migrations.AlterModelOptions(
            name='eqhhydrophoneproperty',
            options={'ordering': ('emm__emm_make', 'emm__emm_model')},
        ),
        migrations.AlterModelOptions(
            name='eqpequipment',
            options={'ordering': ('emm__emm_make', 'emm__emm_model')},
        ),
        migrations.AlterModelOptions(
            name='eqrrecorderproperties',
            options={'ordering': ('emm__emm_make', 'emm__emm_model')},
        ),
        migrations.AlterModelOptions(
            name='mormooringsetup',
            options={'ordering': ('mor_name',)},
        ),
        migrations.AlterModelOptions(
            name='retrecordingeventtype',
            options={'ordering': ('ret_name',)},
        ),
        migrations.AlterModelOptions(
            name='rscrecordingschedule',
            options={'ordering': ('rsc_name',)},
        ),
        migrations.AlterModelOptions(
            name='rtttimezonecode',
            options={'ordering': ('rtt_offset',)},
        ),
        migrations.AlterModelOptions(
            name='stnstation',
            options={'ordering': ('stn_name',)},
        ),
        migrations.AlterModelOptions(
            name='teateammember',
            options={'ordering': ('tea_last_name', 'tea_first_name')},
        ),
        migrations.AddField(
            model_name='etrtechnicalrepairevent',
            name='hyd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='etr_hydrophones', to='whalesdb.eqpequipment', verbose_name='Hydrophone'),
        ),
        migrations.AlterField(
            model_name='ecpchannelproperty',
            name='ecp_voltage_range_max',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=22, null=True, verbose_name='Minimum voltage'),
        ),
        migrations.AlterField(
            model_name='ecpchannelproperty',
            name='ecp_voltage_range_min',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=22, null=True, verbose_name='Maximum voltage'),
        ),
    ]