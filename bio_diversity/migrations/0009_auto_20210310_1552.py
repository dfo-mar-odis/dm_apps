# Generated by Django 3.1.2 on 2021-03-10 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0008_auto_20210310_1550'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='tray',
            name='tray_uniqueness',
        ),
        migrations.AddConstraint(
            model_name='tray',
            constraint=models.UniqueConstraint(fields=('name', 'trof_id', 'start_date'), name='tray_uniqueness'),
        ),
    ]