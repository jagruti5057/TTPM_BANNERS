# Generated by Django 4.1.7 on 2023-04-28 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_liccirclars_newsarticals_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='liccirclars',
            old_name='category',
            new_name='type_of_category',
        ),
    ]
