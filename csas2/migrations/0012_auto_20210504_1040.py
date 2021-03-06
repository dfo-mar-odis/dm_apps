# Generated by Django 3.2 on 2021-05-04 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0013_auto_20210430_0759'),
        ('csas2', '0011_auto_20210504_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttracking',
            name='date_division_manager_appr',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date approved by division manager'),
        ),
        migrations.AddField(
            model_name='documenttracking',
            name='date_division_manager_sent',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date sent to division manager'),
        ),
        migrations.AddField(
            model_name='documenttracking',
            name='date_section_head_appr',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date approved by section head'),
        ),
        migrations.AddField(
            model_name='documenttracking',
            name='date_section_head_sent',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date sent to section head'),
        ),
        migrations.AddField(
            model_name='documenttracking',
            name='division_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_division_managers', to='shared_models.person', verbose_name='division manager'),
        ),
        migrations.AddField(
            model_name='documenttracking',
            name='section_head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_section_heads', to='shared_models.person', verbose_name='section head'),
        ),
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.IntegerField(choices=[(0, 'OK'), (1, 'Tracking initiated'), (2, 'Submitted by author'), (3, 'Under review by chair'), (4, 'Approved by chair'), (5, 'Under review by CSAS coordinator'), (6, 'Approved by CSAS coordinator'), (13, 'Under review by section head'), (14, 'Approved by section head'), (15, 'Under review by division manager'), (16, 'Approved by division manager'), (7, 'Under review by director'), (8, 'Approved by director'), (9, 'Submitted to CSAS office'), (10, 'Proof sent to author'), (11, 'Proof approved by author'), (12, 'Posted')], default=1, editable=False, verbose_name='status'),
        ),
    ]
