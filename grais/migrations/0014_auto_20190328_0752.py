# Generated by Django 2.1.4 on 2019-03-28 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0013_auto_20190327_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='estuary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sites', to='grais.Estuary'),
        ),
    ]
