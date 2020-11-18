# Generated by Django 3.1.2 on 2020-11-09 12:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0024_auto_20201102_1135'),
        ('projects2', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectyear',
            old_name='lab_space_required',
            new_name='requires_lab_space',
        ),
        migrations.AlterField(
            model_name='projectyear',
            name='deliverables',
            field=models.TextField(blank=True, null=True, verbose_name='deliverables / activities'),
        ),
        migrations.AlterField(
            model_name='projectyear',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End date of project'),
        ),
        migrations.AlterField(
            model_name='projectyear',
            name='fiscal_year',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shared_models.fiscalyear', verbose_name='fiscal year'),
        ),
        migrations.AlterField(
            model_name='projectyear',
            name='notification_email_sent',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Notification Email Sent'),
        ),
        migrations.AlterField(
            model_name='projectyear',
            name='open_data_eligible',
            field=models.BooleanField(default=False, verbose_name='Are these data / data products eligible to be placed on the Open Data Platform?'),
        ),
        migrations.AlterField(
            model_name='projectyear',
            name='priorities',
            field=models.TextField(blank=True, null=True, verbose_name='year-specific priorities'),
        ),
        migrations.AlterField(
            model_name='projectyear',
            name='requires_field_staff',
            field=models.BooleanField(default=False, verbose_name='Do you require field support staff?'),
        ),
        migrations.AlterField(
            model_name='projectyear',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Start date of project'),
        ),
        migrations.AlterUniqueTogether(
            name='projectyear',
            unique_together={('project', 'fiscal_year')},
        ),
    ]