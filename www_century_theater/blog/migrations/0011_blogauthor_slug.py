# Generated by Django 4.0.3 on 2022-03-09 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0010_blogpage_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogauthor",
            name="slug",
            field=models.SlugField(null=True),
        ),
    ]
