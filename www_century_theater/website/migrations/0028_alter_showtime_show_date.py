# Generated by Django 4.0.3 on 2022-03-14 01:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0027_showtime_show_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="showtime",
            name="show_date",
            field=models.DateField(
                default=datetime.datetime(2022, 3, 14, 1, 56, 30, 552356, tzinfo=utc)
            ),
        ),
    ]
