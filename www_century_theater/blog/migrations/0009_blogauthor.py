# Generated by Django 4.0.3 on 2022-03-09 20:46

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0023_add_choose_permissions"),
        ("blog", "0008_delete_blogauthor"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogAuthor",
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
                ("last_name", models.CharField(max_length=45)),
                ("first_name", models.CharField(max_length=65)),
                ("bio", wagtail.core.fields.RichTextField(blank=True, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                ("facebook", models.URLField(blank=True, null=True)),
                ("twitter", models.URLField(blank=True, null=True)),
                ("linkedin", models.URLField(blank=True, null=True)),
                ("instagram", models.URLField(blank=True, null=True)),
                (
                    "image",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Blog Author",
                "verbose_name_plural": "Blog Authors",
            },
        ),
    ]
