# Generated by Django 3.1.8 on 2021-09-04 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_auto_20210904_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevaluation',
            name='assigned_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
