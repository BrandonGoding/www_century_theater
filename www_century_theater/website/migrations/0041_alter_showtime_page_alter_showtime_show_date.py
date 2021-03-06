# Generated by Django 4.0.3 on 2022-03-19 01:42

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0040_alter_movie_imdb_id_alter_movie_youtube_id_showtime"),
    ]

    operations = [
        migrations.AlterField(
            model_name="showtime",
            name="page",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="showtimes",
                to="website.movie",
            ),
        ),
        migrations.AlterField(
            model_name="showtime",
            name="show_date",
            field=models.DateField(
                default=datetime.datetime(2022, 3, 19, 1, 42, 42, 560818, tzinfo=utc)
            ),
        ),
    ]
