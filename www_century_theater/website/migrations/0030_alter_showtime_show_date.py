# Generated by Django 4.0.3 on 2022-03-14 02:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0029_movie_close_date_movie_open_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="showtime",
            name="show_date",
            field=models.DateField(
                default=datetime.datetime(2022, 3, 14, 2, 3, 8, 180937, tzinfo=utc)
            ),
        ),
    ]
