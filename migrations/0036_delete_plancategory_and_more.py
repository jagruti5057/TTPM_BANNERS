# Generated by Django 4.1.7 on 2023-05-08 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0035_statuscategory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PlanCategory',
        ),
        migrations.RemoveField(
            model_name='liccirclars',
            name='type_of_category',
        ),
    ]
