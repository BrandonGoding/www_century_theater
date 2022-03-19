# Generated by Django 4.0.3 on 2022-03-18 23:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0033_movie_imdb_id_alter_showtime_show_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='rating',
        ),
        migrations.AlterField(
            model_name='showtime',
            name='show_date',
            field=models.DateField(default=datetime.datetime(2022, 3, 18, 23, 18, 55, 206067, tzinfo=utc)),
        ),
    ]
