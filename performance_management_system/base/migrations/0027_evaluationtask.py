# Generated by Django 3.1.8 on 2021-07-31 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_userevaluation_project_assign'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluationTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.evaluationcategories')),
                ('user_evaluation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.userevaluation')),
            ],
        ),
    ]
