# Generated by Django 3.1.8 on 2021-09-04 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0039_auto_20210903_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevaluation',
            name='assigned_date',
            field=models.DateTimeField(null=True),
        ),
    ]