# Generated by Django 3.1.2 on 2021-01-14 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0035_auto_20210114_0553'),
        ('projects2', '0022_project_references'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='innovation',
            field=models.TextField(blank=True, null=True, verbose_name='Describe how the project will generate or promote innovation (CSRF)'),
        ),
        migrations.AddField(
            model_name='project',
            name='other_funding',
            field=models.TextField(blank=True, null=True, verbose_name='Provide any additional information on the other sources of funding relevant to the project (e.g. type of in-kind contribution) (CSRF)'),
        ),
        migrations.AlterField(
            model_name='project',
            name='references',
            field=models.ManyToManyField(blank=True, editable=False, related_name='projects', to='shared_models.Citation', verbose_name='references'),
        ),
    ]