# Generated by Django 4.1.7 on 2023-04-29 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_rename_formname_forms_formsname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticals',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
