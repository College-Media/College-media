# Generated by Django 5.1.2 on 2025-01-06 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0008_remove_tagmessage_tag_remove_tagmessage_sender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_notifications',
            name='post_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
