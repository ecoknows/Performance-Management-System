# Generated by Django 3.1.8 on 2021-06-29 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20210629_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationrateassign',
            name='evaluation_rates',
        ),
    ]
