# Generated by Django 4.0.3 on 2022-03-06 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='author',
        ),
        migrations.DeleteModel(
            name='BlogAuthor',
        ),
    ]