# Generated by Django 4.0.3 on 2022-03-16 15:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0032_alter_movie_review_page_alter_showtime_show_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='imdb_id',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='showtime',
            name='show_date',
            field=models.DateField(default=datetime.datetime(2022, 3, 16, 15, 25, 22, 138112, tzinfo=utc)),
        ),
    ]
