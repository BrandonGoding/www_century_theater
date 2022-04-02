# Generated by Django 4.0.3 on 2022-03-28 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_blogauthor_tagline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='categories',
        ),
        migrations.AddField(
            model_name='blogpage',
            name='categories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blog.blogcategory'),
        ),
    ]