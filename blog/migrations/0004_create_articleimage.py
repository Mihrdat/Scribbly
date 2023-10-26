# Generated by Django 4.1.2 on 2023-10-23 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_create_article"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArticleImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("url", models.ImageField(upload_to="blog/articles")),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="blog.article",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]