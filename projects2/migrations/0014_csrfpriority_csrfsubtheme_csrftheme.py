# Generated by Django 3.1.2 on 2021-01-13 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0013_auto_20210112_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSRFTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
                ('code', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CSRFSubTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
                ('csrf_theme', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sub_themes', to='projects2.csrftheme', verbose_name='theme')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CSRFPriority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Priority identification number')),
                ('name', models.IntegerField(verbose_name='priority for research')),
                ('nom', models.IntegerField(verbose_name='priority for research')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='additional information')),
                ('description_fr', models.IntegerField(blank=True, null=True, verbose_name='additional information')),
                ('csrf_sub_theme', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='priorities', to='projects2.csrfsubtheme', verbose_name='sub-theme')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
