# Generated by Django 2.2.2 on 2020-05-12 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mmutools', '0021_remove_lending_table_fix_quantities_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='status')),
                ('nom', models.CharField(max_length=250, verbose_name='status')),
            ],
        ),
        migrations.RenameField(
            model_name='quantity',
            old_name='item',
            new_name='items',
        ),
        migrations.RemoveField(
            model_name='quantity',
            name='status',
        ),
        migrations.AddField(
            model_name='quantity',
            name='statuses',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.DO_NOTHING, related_name='quantities', to='mmutools.Status', verbose_name='status'),
            preserve_default=False,
        ),
    ]