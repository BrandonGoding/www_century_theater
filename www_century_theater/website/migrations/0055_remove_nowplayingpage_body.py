# Generated by Django 4.0.3 on 2022-03-22 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0054_alter_nowplayingpage_body"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="nowplayingpage",
            name="body",
        ),
    ]
