# Generated by Django 3.1.8 on 2021-07-30 15:58

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_userevaluation_assigned_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationpage',
            name='legend_evaluation',
            field=wagtail.core.fields.RichTextField(null=True),
        ),
    ]
