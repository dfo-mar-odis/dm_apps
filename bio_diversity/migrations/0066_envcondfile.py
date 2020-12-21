# Generated by Django 3.1.2 on 2020-12-14 15:22

import bio_diversity.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0065_auto_20201214_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnvCondFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=32, verbose_name='Created By')),
                ('created_date', models.DateField(verbose_name='Created Date')),
                ('env_pdf', models.FileField(blank=True, null=True, upload_to=bio_diversity.models.envcf_directory_path, verbose_name='Environment Condition File')),
                ('comments', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Comments')),
                ('env_id', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.envcondition', verbose_name='Environment Condition')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]