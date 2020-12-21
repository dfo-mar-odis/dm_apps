# Generated by Django 3.1.2 on 2020-12-09 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0039_collection_prioritycode_stockcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=32, verbose_name='Created By')),
                ('created_date', models.DateField(verbose_name='Created Date')),
                ('grp_valid', models.BooleanField(default='False', verbose_name='Group still valid?')),
                ('comments', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Comments')),
                ('coll_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.collection', verbose_name='Collection')),
                ('frm_grp_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.group', verbose_name='From Parent Group')),
                ('spec_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.speciescode', verbose_name='Species')),
                ('stok_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.stockcode', verbose_name='Stock Code')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]