# Generated by Django 4.0.3 on 2022-03-22 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0052_alter_showtime_show_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basicpage',
            name='body',
        ),
    ]
