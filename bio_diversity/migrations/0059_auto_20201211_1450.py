# Generated by Django 3.1.2 on 2020-12-11 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0058_anidetailxref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anidetailxref',
            name='grp_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.group', verbose_name='Group'),
        ),
    ]