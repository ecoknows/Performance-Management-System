# Generated by Django 3.1.8 on 2021-06-23 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_hr',
            field=models.BooleanField(default=False),
        ),
    ]
