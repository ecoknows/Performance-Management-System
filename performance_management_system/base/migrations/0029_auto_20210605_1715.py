# Generated by Django 3.1.8 on 2021-06-05 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_auto_20210605_1714'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evaluationrates',
            old_name='evaluation_rate',
            new_name='rate',
        ),
    ]
