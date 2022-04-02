# Generated by Django 4.0.3 on 2022-03-19 20:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0047_alter_showtime_show_date_delete_comingsoonpage"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="confirmed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="showtime",
            name="show_date",
            field=models.DateField(
                default=datetime.datetime(2022, 3, 19, 20, 55, 45, 712326, tzinfo=utc)
            ),
        ),
    ]
