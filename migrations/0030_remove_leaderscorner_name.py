# Generated by Django 4.1.7 on 2023-05-04 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0029_licplans_remove_liccirclars_is_frame_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaderscorner',
            name='name',
        ),
    ]
