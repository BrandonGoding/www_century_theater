# Generated by Django 4.0.3 on 2022-03-28 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0013_remove_blogpage_categories_blogpage_categories"),
    ]

    operations = [
        migrations.RenameField(
            model_name="blogpage",
            old_name="categories",
            new_name="category",
        ),
    ]
