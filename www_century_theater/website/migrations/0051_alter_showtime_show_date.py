# Generated by Django 4.0.3 on 2022-03-19 22:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0050_alter_showtime_show_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="showtime",
            name="show_date",
            field=models.DateField(
                default=datetime.datetime(2022, 3, 19, 22, 49, 24, 232731, tzinfo=utc)
            ),
        ),
    ]
