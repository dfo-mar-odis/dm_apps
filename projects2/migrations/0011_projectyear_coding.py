# Generated by Django 3.1.2 on 2020-11-12 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0010_auto_20201112_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectyear',
            name='coding',
            field=models.TextField(blank=True, editable=False, null=True, verbose_name='financial coding'),
        ),
    ]
