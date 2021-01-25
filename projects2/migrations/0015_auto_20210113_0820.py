# Generated by Django 3.1.2 on 2021-01-13 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0014_csrfpriority_csrfsubtheme_csrftheme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csrfpriority',
            name='code',
            field=models.CharField(max_length=25, verbose_name='Priority identification number'),
        ),
        migrations.AlterField(
            model_name='csrfpriority',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='additional information (en)'),
        ),
        migrations.AlterField(
            model_name='csrfpriority',
            name='description_fr',
            field=models.IntegerField(blank=True, null=True, verbose_name='additional information (fr)'),
        ),
        migrations.AlterField(
            model_name='csrfpriority',
            name='name',
            field=models.IntegerField(verbose_name='priority for research (en)'),
        ),
        migrations.AlterField(
            model_name='csrfpriority',
            name='nom',
            field=models.IntegerField(verbose_name='priority for research (fr)'),
        ),
        migrations.AlterField(
            model_name='csrftheme',
            name='code',
            field=models.CharField(max_length=25),
        ),
    ]
