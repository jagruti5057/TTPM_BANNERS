# Generated by Django 4.1.7 on 2023-05-02 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_rename_category_name_category_plans_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='PlanCategory',
        ),
    ]