# Generated by Django 2.2.13 on 2020-10-02 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whalesdb', '0007_auto_20201002_0802'),
    ]

    operations = [
        migrations.RenameField(
            model_name='etrtechnicalrepairevent',
            old_name='eqp_id',
            new_name='eqp',
        ),
    ]