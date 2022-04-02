# Generated by Django 4.0.3 on 2022-03-31 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0019_blogpage_movie"),
        ("website", "0056_basicpage_body_nowplayingpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="review_page",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="movies",
                to="blog.blogpage",
            ),
        ),
    ]
