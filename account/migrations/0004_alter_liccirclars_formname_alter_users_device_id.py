# Generated by Django 4.1.7 on 2023-04-28 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_rename_category_liccirclars_type_of_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liccirclars',
            name='formname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='device_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]