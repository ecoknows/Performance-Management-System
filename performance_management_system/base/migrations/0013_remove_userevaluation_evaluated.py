# Generated by Django 3.1.8 on 2021-07-17 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_userevaluation_percentage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userevaluation',
            name='evaluated',
        ),
    ]
