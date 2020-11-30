# Generated by Django 3.1.2 on 2020-11-24 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0022_auto_20201123_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='is_denied',
        ),
        migrations.AddField(
            model_name='review',
            name='approval_status',
            field=models.IntegerField(blank=True, choices=[(1, 'approved'), (0, 'not approved')], null=True, verbose_name='Approval status'),
        ),
    ]