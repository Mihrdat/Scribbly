# Generated by Django 4.1.2 on 2023-11-16 10:35

import django.contrib.auth.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_field_username_to_unique_in_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                default=uuid.uuid4,
                max_length=55,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
            ),
        ),
    ]
