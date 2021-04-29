# Generated by Django 3.2 on 2021-04-29 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0025_termsofreference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='termsofreference',
            name='meeting',
        ),
        migrations.AddField(
            model_name='termsofreference',
            name='process',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tor', to='csas2.process'),
            preserve_default=False,
        ),
    ]
