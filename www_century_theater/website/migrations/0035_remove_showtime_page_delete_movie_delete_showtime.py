# Generated by Django 4.0.3 on 2022-03-18 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0034_remove_movie_rating_alter_showtime_show_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="showtime",
            name="page",
        ),
        migrations.DeleteModel(
            name="Movie",
        ),
        migrations.DeleteModel(
            name="ShowTime",
        ),
    ]
