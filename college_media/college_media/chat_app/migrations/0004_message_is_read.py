# Generated by Django 5.1.3 on 2024-12-13 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat_app", "0003_alter_notification_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="is_read",
            field=models.BooleanField(default=False),
        ),
    ]
