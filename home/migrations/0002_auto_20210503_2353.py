# Generated by Django 3.1.8 on 2021-05-03 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='company',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='Companies',
        ),
    ]
