# Generated by Django 4.1.7 on 2023-05-01 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_profileframe'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_av', models.CharField(choices=[('Audio', 'Audio'), ('Video', 'Video')], max_length=50)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='audio_video/')),
                ('description', models.TextField()),
            ],
        ),
    ]
