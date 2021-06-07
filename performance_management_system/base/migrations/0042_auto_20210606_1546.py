# Generated by Django 3.1.8 on 2021-06-06 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_auto_20210606_1232'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evaluationrates',
            options={},
        ),
        migrations.RemoveField(
            model_name='evaluationrates',
            name='sort_order',
        ),
        migrations.AlterField(
            model_name='evaluationcategories',
            name='category_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='evaluationrates',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='Question'),
        ),
    ]
