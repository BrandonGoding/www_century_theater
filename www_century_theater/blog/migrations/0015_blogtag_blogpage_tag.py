# Generated by Django 4.0.3 on 2022-03-29 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_rename_categories_blogpage_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, help_text='A slug to identify posts by this tag', max_length=255, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Blog Tag',
                'verbose_name_plural': 'Blog Tags',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='blogpage',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, related_name='+', to='blog.blogtag'),
        ),
    ]