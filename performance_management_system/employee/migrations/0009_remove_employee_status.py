# Generated by Django 3.1.8 on 2021-08-30 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_reportsemployee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='status',
        ),
    ]
