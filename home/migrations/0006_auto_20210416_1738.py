# Generated by Django 3.1.8 on 2021-04-16 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_companies'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='company_name',
        ),
        migrations.AddField(
            model_name='client',
            name='companies',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.companies'),
        ),
    ]
