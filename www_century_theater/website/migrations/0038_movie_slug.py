# Generated by Django 4.0.3 on 2022-03-19 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0037_movie_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(auto_created=True, null=True),
        ),
    ]