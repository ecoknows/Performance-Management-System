# Generated by Django 3.1.8 on 2021-06-05 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_auto_20210605_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluationrates',
            name='rate',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
