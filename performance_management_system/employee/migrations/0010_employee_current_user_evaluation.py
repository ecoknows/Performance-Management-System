# Generated by Django 3.1.8 on 2021-08-30 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_delete_reportspage'),
        ('employee', '0009_remove_employee_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='current_user_evaluation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='base.userevaluation'),
        ),
    ]
