# Generated by Django 3.1.8 on 2021-09-01 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
        ('base', '0032_remove_userevaluation_percentage'),
    ]

    operations = [
        migrations.CreateModel(
            name='RulesSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('calendar', models.CharField(choices=[('day', 'day'), ('week', 'week'), ('month', 'month'), ('year', 'year')], max_length=255)),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
