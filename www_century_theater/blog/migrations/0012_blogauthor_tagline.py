# Generated by Django 4.0.3 on 2022-03-10 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0011_blogauthor_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogauthor",
            name="tagline",
            field=models.CharField(
                default="This is a tagline please update it.", max_length=120
            ),
        ),
    ]
