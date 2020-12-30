# Generated by Django 3.1.2 on 2020-12-10 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0046_spawndetsubjcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='containerdetcode',
            name='cont_subj_flag',
            field=models.BooleanField(verbose_name='Subjective detail?'),
        ),
        migrations.AlterField(
            model_name='countdet',
            name='adsc_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.anidetsubjcode', verbose_name='Animal Detail Subjective Code'),
        ),
        migrations.AlterField(
            model_name='cupdet',
            name='cdsc_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.contdetsubjcode', verbose_name='Container Detail Subjective Code'),
        ),
        migrations.AlterField(
            model_name='envcondition',
            name='envsc_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.envsubjcode', verbose_name='Environment Subjective Code'),
        ),
        migrations.AlterField(
            model_name='heathunitdet',
            name='cdsc_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.contdetsubjcode', verbose_name='Container Detail Subjective Code'),
        ),
        migrations.AlterField(
            model_name='heathunitdet',
            name='heat_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.heathunit', verbose_name='Heath Unit'),
        ),
        migrations.AlterField(
            model_name='sampledet',
            name='adsc_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.anidetsubjcode', verbose_name='Animal Detail Subjective Code'),
        ),
        migrations.AlterField(
            model_name='tankdet',
            name='cdsc_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.contdetsubjcode', verbose_name='Container Detail Subjective Code'),
        ),
        migrations.AlterField(
            model_name='traydet',
            name='cdsc_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.contdetsubjcode', verbose_name='Container Detail Subjective Code'),
        ),
        migrations.AlterField(
            model_name='troughdet',
            name='cdsc_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.contdetsubjcode', verbose_name='Container Detail Subjective Code'),
        ),
    ]