# Generated by Django 5.1.2 on 2024-10-27 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff_app", "0003_alter_coustomuser_roll_number_alter_student_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="profile_image",
            field=models.ImageField(blank=True, null=True, upload_to="profile_image/"),
        ),
    ]
