# Generated by Django 3.1.2 on 2021-01-12 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0006_auto_20210112_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_notification_email_sent',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Notification Email Sent'),
        ),
    ]