# Generated by Django 3.1.2 on 2020-12-08 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0035_sample_sampledet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='samp_num',
            field=models.IntegerField(verbose_name='Sample Fish Number'),
        ),
    ]