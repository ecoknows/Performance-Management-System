# Generated by Django 3.1.8 on 2021-06-25 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_client_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='status',
            field=models.CharField(choices=[('none', 'None'), ('evaluated', 'Evaluated'), ('on evaluation', 'On Evaluation')], default='none', max_length=255),
        ),
    ]
