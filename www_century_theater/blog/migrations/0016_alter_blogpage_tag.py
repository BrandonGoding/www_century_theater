# Generated by Django 4.0.3 on 2022-03-29 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0015_blogtag_blogpage_tag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="tag",
            field=models.ManyToManyField(
                blank=True, related_name="+", to="blog.blogtag"
            ),
        ),
    ]
