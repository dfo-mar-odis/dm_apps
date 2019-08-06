# Generated by Django 2.2.2 on 2019-07-22 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0019_person_email_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='ihub_vetted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='person',
            name='designation',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='title'),
        ),
    ]
