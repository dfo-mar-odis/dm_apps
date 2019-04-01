# Generated by Django 2.1.4 on 2019-03-26 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0003_project'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cruise',
            options={'ordering': ['mission_number']},
        ),
        migrations.AlterField(
            model_name='cruise',
            name='number_of_profiles',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
