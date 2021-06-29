# Generated by Django 3.1.8 on 2021-06-29 03:31

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20210624_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationrateassign',
            name='evaluation_categories_assign',
        ),
        migrations.AddField(
            model_name='evaluationrateassign',
            name='evaluation_categories',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_rates_assign', to='base.evaluationcategories'),
        ),
        migrations.AddField(
            model_name='evaluationrateassign',
            name='user_evaluation',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_rates_assign', to='base.userevaluation'),
        ),
        migrations.DeleteModel(
            name='EvaluationCategoriesAssign',
        ),
    ]
