# Generated by Django 4.0.3 on 2022-03-16 14:32

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('website', '0030_alter_showtime_show_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='review_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page'),
        ),
        migrations.AlterField(
            model_name='showtime',
            name='show_date',
            field=models.DateField(default=datetime.datetime(2022, 3, 16, 14, 32, 6, 990397, tzinfo=utc)),
        ),
    ]