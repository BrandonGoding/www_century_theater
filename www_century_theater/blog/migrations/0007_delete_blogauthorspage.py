# Generated by Django 4.0.3 on 2022-03-09 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blogpage_featured_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BlogAuthorsPage',
        ),
    ]