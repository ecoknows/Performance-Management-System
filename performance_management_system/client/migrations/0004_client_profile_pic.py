# Generated by Django 3.1.8 on 2021-06-23 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('client', '0003_auto_20210623_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='profile_pic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
