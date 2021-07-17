# Generated by Django 3.1.8 on 2021-07-17 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_employee_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(choices=[('none', 'None'), ('evaluated', 'Evaluated'), ('on-evaluation', 'On Evaluation')], default='none', max_length=255),
        ),
    ]
