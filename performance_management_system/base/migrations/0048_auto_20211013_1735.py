# Generated by Django 3.1.8 on 2021-10-13 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0047_auto_20211013_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevaluation',
            name='assigned_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
