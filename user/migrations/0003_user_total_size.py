# Generated by Django 5.0.1 on 2024-07-15 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_wallet_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='total_size',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
