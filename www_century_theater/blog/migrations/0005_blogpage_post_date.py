# Generated by Django 4.0.3 on 2022-03-07 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_blogauthorspage"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpage",
            name="post_date",
            field=models.DateField(auto_created=True, default="2022-01-02"),
            preserve_default=False,
        ),
    ]
