# Generated by Django 2.1.4 on 2019-05-06 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0005_status_old_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='review_completion_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
