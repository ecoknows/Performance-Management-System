# Generated by Django 3.1.8 on 2021-06-29 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_remove_evaluationrateassign_evaluation_rates'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationrateassign',
            name='name',
            field=models.TextField(max_length=255, null=True, verbose_name='Question'),
        ),
    ]
