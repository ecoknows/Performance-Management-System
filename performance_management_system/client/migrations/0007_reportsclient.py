# Generated by Django 3.1.8 on 2021-08-28 15:05

from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.routable_page.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
        ('client', '0006_auto_20210717_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportsClient',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
    ]
