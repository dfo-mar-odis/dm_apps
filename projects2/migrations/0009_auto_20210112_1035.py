# Generated by Django 3.1.2 on 2021-01-12 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0008_review_approval_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='approval_level',
            field=models.IntegerField(blank=True, choices=[(1, 'Division-level'), (2, 'Branch-level'), (3, 'National')], null=True, verbose_name='level of approval'),
        ),
    ]