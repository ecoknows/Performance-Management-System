# Generated by Django 3.1.8 on 2021-07-31 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_evaluationtask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluationtask',
            name='user_evaluation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_task', to='base.userevaluation'),
        ),
    ]
