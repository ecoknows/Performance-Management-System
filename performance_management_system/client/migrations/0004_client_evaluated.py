# Generated by Django 3.1.8 on 2021-06-05 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20210605_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='evaluated',
            field=models.BooleanField(default=False),
        ),
    ]
