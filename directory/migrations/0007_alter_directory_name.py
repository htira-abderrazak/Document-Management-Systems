# Generated by Django 5.0.1 on 2024-04-15 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0006_directory_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]