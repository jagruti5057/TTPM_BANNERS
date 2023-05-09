# Generated by Django 4.1.7 on 2023-05-02 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_rename_category_plancategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='PremiumCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_user', models.CharField(choices=[('head', 'head'), ('member', 'member')], max_length=30)),
                ('mobile_no', models.CharField(max_length=10, unique=True)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PolicyDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_insurance', models.CharField(choices=[('life insurance', 'life insurance'), ('health insurance', 'health insurance'), ('General insurance', 'General insurance')], max_length=30)),
                ('product_name', models.CharField(blank=True, max_length=50, null=True)),
                ('policy_number', models.CharField(blank=True, max_length=50, null=True)),
                ('sum_assured', models.CharField(max_length=10, unique=True)),
                ('type_of_mode', models.CharField(choices=[('yearly', 'yearly'), ('quaterly', 'quaterly'), ('monthly', 'monthly'), ('single', 'single')], max_length=30)),
                ('term', models.CharField(blank=True, max_length=50, null=True)),
                ('ppt', models.CharField(blank=True, max_length=50, null=True)),
                ('policy_start_due', models.DateTimeField(blank=True, null=True)),
                ('policy_next_due', models.DateTimeField(blank=True, null=True)),
                ('premium', models.CharField(blank=True, max_length=50, null=True)),
                ('type_of_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.premiumcalendar')),
            ],
        ),
    ]