# Generated by Django 3.1.8 on 2021-06-05 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_evaluationcategories_clean_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationcategories',
            name='clean_name',
        ),
    ]
