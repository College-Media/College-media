# Generated by Django 5.1.3 on 2024-12-30 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("staff_app", "0007_tagmessage"),
    ]

    operations = [
        migrations.RemoveField(model_name="tagmessage", name="tag",),
        migrations.RemoveField(model_name="tagmessage", name="sender",),
        migrations.DeleteModel(name="Tag",),
        migrations.DeleteModel(name="TagMessage",),
    ]