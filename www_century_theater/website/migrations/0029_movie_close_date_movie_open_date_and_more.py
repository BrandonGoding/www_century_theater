# Generated by Django 4.0.3 on 2022-03-14 02:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0028_alter_showtime_show_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="close_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="movie",
            name="open_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="showtime",
            name="show_date",
            field=models.DateField(
                default=datetime.datetime(2022, 3, 14, 2, 2, 8, 307399, tzinfo=utc)
            ),
        ),
    ]
