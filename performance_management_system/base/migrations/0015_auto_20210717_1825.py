# Generated by Django 3.1.8 on 2021-07-17 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_userevaluation_submit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevaluation',
            name='percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
