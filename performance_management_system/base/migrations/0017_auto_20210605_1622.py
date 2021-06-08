# Generated by Django 3.1.8 on 2021-06-05 16:22

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_auto_20210605_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationcategories',
            name='user_evaluation',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_evaluation_categories', to='base.userevaluation'),
        ),
        migrations.AlterField(
            model_name='evaluationcategories',
            name='evaluation_categories',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_categories', to='base.evaluationpage'),
        ),
    ]
