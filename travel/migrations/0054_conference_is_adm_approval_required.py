# Generated by Django 2.2.2 on 2019-11-28 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0053_auto_20191127_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='is_adm_approval_required',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='does attendance to this require ADM approval?'),
        ),
    ]
