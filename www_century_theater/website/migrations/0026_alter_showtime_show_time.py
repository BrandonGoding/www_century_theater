# Generated by Django 4.0.3 on 2022-03-14 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0025_remove_showtime_ticket_price_showtime_matinee"),
    ]

    operations = [
        migrations.AlterField(
            model_name="showtime",
            name="show_time",
            field=models.TimeField(),
        ),
    ]
