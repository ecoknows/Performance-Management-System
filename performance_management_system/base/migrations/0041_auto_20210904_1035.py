# Generated by Django 3.1.8 on 2021-09-04 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0040_auto_20210904_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevaluation',
            name='assigned_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
