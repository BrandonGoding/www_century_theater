# Generated by Django 4.0.3 on 2022-03-09 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0007_delete_blogauthorspage"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BlogAuthor",
        ),
    ]
