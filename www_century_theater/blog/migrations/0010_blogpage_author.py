# Generated by Django 4.0.3 on 2022-03-09 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0009_blogauthor"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpage",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="blog.blogauthor",
            ),
        ),
    ]
