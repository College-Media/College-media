# Generated by Django 5.1.3 on 2024-12-30 11:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_app", "0003_tag_tagmessage"),
    ]

    operations = [
        migrations.AddField(
            model_name="tagmessage",
            name="post",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tag_messages",
                to="user_app.post",
            ),
        ),
    ]
