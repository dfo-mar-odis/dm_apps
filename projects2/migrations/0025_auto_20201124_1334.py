# Generated by Django 3.1.2 on 2020-11-24 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0024_auto_20201124_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='approver_comment',
            field=models.TextField(blank=True, null=True, verbose_name='Approver comments (shared with project leads)'),
        ),
    ]