# Generated by Django 3.1.2 on 2021-02-25 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0004_auto_20210224_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='triprequest1',
            name='name_search',
            field=models.CharField(blank=True, editable=False, max_length=1000, null=True),
        ),
    ]