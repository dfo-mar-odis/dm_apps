# Generated by Django 3.1.2 on 2021-02-11 02:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared_models', '0004_auto_20210126_1540'),
        ('travel', '0016_auto_20210210_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='fiscal_year',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trips', to='shared_models.fiscalyear', verbose_name='fiscal year'),
        ),
        migrations.AlterField(
            model_name='cost',
            name='cost_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='travel.costcategory', verbose_name='category'),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=1000, verbose_name='destination location (city, province, country)')),
                ('objective_of_event', models.TextField(blank=True, null=True, verbose_name='what is the objective of this meeting or conference?')),
                ('benefit_to_dfo', models.TextField(blank=True, null=True, verbose_name='what are the benefits to DFO?')),
                ('late_justification', models.TextField(blank=True, null=True, verbose_name='justification for late submissions')),
                ('funding_source', models.TextField(blank=True, null=True, verbose_name='what is the funding source?')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes (optional)')),
                ('admin_notes', models.TextField(blank=True, null=True, verbose_name='Administrative notes')),
                ('submitted', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='date submitted')),
                ('original_submission_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='original submission date')),
                ('status', models.IntegerField(choices=[(8, 'Draft'), (10, 'Denied'), (11, 'Approved'), (12, 'Pending Recommendation'), (14, 'Pending ADM Approval'), (15, 'Pending RDG Approval'), (16, 'Changes Requested'), (17, 'Pending Review'), (22, 'Cancelled')], default=8, editable=False, verbose_name='trip request status')),
                ('bta_attendees', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='other attendees covered under BTA')),
                ('fiscal_year', models.ForeignKey(blank=True, default=2021, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='requests', to='shared_models.fiscalyear', verbose_name='fiscal year')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='travel_leads', to=settings.AUTH_USER_MODEL, verbose_name='Who is the lead on this request?')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='requests', to='shared_models.section', verbose_name='under which section is this request being made?')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='requests', to='travel.conference', verbose_name='trip')),
            ],
            options={
                'verbose_name': 'trip request',
                'ordering': ['-trip__start_date'],
            },
        ),
        migrations.AddField(
            model_name='file',
            name='request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='travel.request'),
        ),
        migrations.AddField(
            model_name='reviewer',
            name='request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewers', to='travel.request'),
        ),
        migrations.AddField(
            model_name='triprequestcost',
            name='request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='costs', to='travel.request', verbose_name='trip request NEW'),
        ),
        migrations.AlterUniqueTogether(
            name='triprequestcost',
            unique_together={('request', 'cost'), ('trip_request', 'cost')},
        ),
        migrations.CreateModel(
            name='Traveller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public_servant', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, verbose_name='Is the traveller a public servant?')),
                ('is_research_scientist', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Is the traveller a research scientist (RES)?')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='last name')),
                ('address', models.CharField(blank=True, max_length=1000, null=True, verbose_name='address')),
                ('phone', models.CharField(blank=True, max_length=1000, null=True, verbose_name='phone (xxx-xxx-xxxx)')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='company name')),
                ('departure_location', models.CharField(blank=True, max_length=1000, null=True, verbose_name='departure location (city, province, country)')),
                ('start_date', models.DateTimeField(verbose_name='start date of travel')),
                ('end_date', models.DateTimeField(verbose_name='end date of travel')),
                ('role_of_participant', models.TextField(blank=True, null=True, verbose_name='role description')),
                ('learning_plan', models.BooleanField(default=False, verbose_name='is this request included on your learning plan?')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes (optional)')),
                ('non_dfo_costs', models.FloatField(blank=True, null=True, verbose_name='amount of non-DFO funding (CAD)')),
                ('non_dfo_org', models.CharField(blank=True, max_length=1000, null=True, verbose_name='give the full name(s) of the of the organization(s) providing non-DFO funding')),
                ('request', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='travellers', to='travel.request')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='travel.role', verbose_name='role of traveller')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='DM Apps user')),
            ],
            options={
                'verbose_name': 'trip request',
                'ordering': ['-start_date', 'last_name'],
                'unique_together': {('user', 'request')},
            },
        ),
    ]