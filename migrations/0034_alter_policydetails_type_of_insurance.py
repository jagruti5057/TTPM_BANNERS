# Generated by Django 4.1.7 on 2023-05-04 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0033_alter_policydetails_type_of_insurance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policydetails',
            name='type_of_insurance',
            field=models.CharField(choices=[('Life Insurance', 'Life Insurance'), ('Health Insurance', 'Health Hnsurance'), ('General Insurance', 'General Insurance')], max_length=30),
        ),
    ]