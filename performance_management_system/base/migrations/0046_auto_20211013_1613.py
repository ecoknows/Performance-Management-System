# Generated by Django 3.1.8 on 2021-10-13 08:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0045_auto_20211013_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevaluation',
            name='late_and_absence',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None), default=[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], size=None),
        ),
    ]