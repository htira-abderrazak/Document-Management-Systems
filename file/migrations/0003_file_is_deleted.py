# Generated by Django 5.0.1 on 2024-01-12 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0002_file_created_at_file_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
