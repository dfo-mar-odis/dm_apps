# Generated by Django 3.2 on 2021-04-16 11:54

import csas2.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csasrequest',
            name='client_has_funding',
        ),
        migrations.RemoveField(
            model_name='csasrequest',
            name='client_signed_at',
        ),
        migrations.AddField(
            model_name='csasrequest',
            name='has_funding',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='i.e., special analysis, meeting costs, translation)?', verbose_name='Do you have funds to cover any extra costs associated with this request?'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='assistance_text',
            field=models.TextField(blank=True, null=True, verbose_name=' Please describe the assistance'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='client_funding_description',
            field=models.TextField(blank=True, null=True, verbose_name='Please describe'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='file_attachment',
            field=models.FileField(blank=True, null=True, upload_to=csas2.models.request_directory_path, verbose_name='signed request form'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='had_assistance',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='E.g. with CSAS and/or DFO science staff.', verbose_name='Have you had assistance from Science in developing the question/request?'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='is_multiregional',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Does this request involve more than one region (zonal) or more than one client sector?'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='rationale_for_timeline',
            field=models.TextField(blank=True, help_text='e.g., COSEWIC or consultation meetings, Environmental Assessments, legal or regulatory requirement, Treaty obligation, international commitments, etc).Please elaborate and provide anticipatory dates', null=True, verbose_name='Rationale for deadline?'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='request_rationale',
            field=models.TextField(help_text='What will the information/advice be used for? Who will be the end user(s)? Will it impact other DFO programs or regions?', verbose_name='Rationale or context for the request'),
        ),
    ]
