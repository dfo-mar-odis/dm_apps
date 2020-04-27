# Generated by Django 2.2.2 on 2020-04-24 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ihub', '0006_relationshiprating'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='relationship_rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='entries', to='ihub.RelationshipRating', verbose_name='relationship rating'),
        ),
    ]