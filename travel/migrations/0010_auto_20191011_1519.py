# Generated by Django 2.2.2 on 2019-10-11 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0009_auto_20191011_1514'),
    ]

    operations = [

        migrations.AlterField(
            model_name='event',
            name='approver_approval_status',
            field=models.IntegerField(default=1, verbose_name='expenditure initiation approval status'),
        ),
        migrations.AlterField(
            model_name='event',
            name='recommender_2_approval_status',
            field=models.IntegerField(default=1, verbose_name='recommender 2 approval status'),
        ),
        migrations.AlterField(
            model_name='event',
            name='recommender_3_approval_status',
            field=models.IntegerField(default=1, verbose_name='recommender 3 approval status'),
        ),
    ]
