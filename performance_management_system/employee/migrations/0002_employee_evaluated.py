# Generated by Django 3.1.8 on 2021-06-05 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='evaluated',
            field=models.BooleanField(default=True),
        ),
    ]
