# Generated by Django 3.1.2 on 2021-01-12 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0007_review_review_notification_email_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='approval_level',
            field=models.IntegerField(blank=True, choices=[(1, 'Division Manager'), (2, 'Branch-level'), (3, 'National')], null=True, verbose_name='level of approval'),
        ),
    ]