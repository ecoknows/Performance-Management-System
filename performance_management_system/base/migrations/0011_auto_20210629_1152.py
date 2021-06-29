# Generated by Django 3.1.8 on 2021-06-29 03:52

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_evaluationrateassign_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationrateassign',
            name='evaluation_categories',
        ),
        migrations.RemoveField(
            model_name='evaluationrateassign',
            name='name',
        ),
        migrations.AddField(
            model_name='evaluationrateassign',
            name='evaluation_rate',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_rates_assign', to='base.evaluationrates'),
        ),
    ]
