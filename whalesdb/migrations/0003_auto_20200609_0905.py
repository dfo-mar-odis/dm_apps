# Generated by Django 2.2.2 on 2020-06-09 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whalesdb', '0002_auto_20200526_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rcichannelinfo',
            name='rec_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='channels', to='whalesdb.RecDataset', verbose_name='Dataset'),
        ),
    ]
