# Generated by Django 4.0.3 on 2022-03-11 21:45

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_alter_basicpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicpage',
            name='body',
            field=wagtail.core.fields.StreamField([('parallax_section', wagtail.core.blocks.StructBlock([('header', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('sub_header', wagtail.core.blocks.CharBlock(max_length=250, required=False)), ('background_image', wagtail.images.blocks.ImageChooserBlock(required=True))])), ('feature_list_section', wagtail.core.blocks.StructBlock([('feature', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('feature_name', wagtail.core.blocks.CharBlock(max_length=25, required=True)), ('feature_summary', wagtail.core.blocks.CharBlock(max_length=255, required=True)), ('icon_id', wagtail.core.blocks.CharBlock(max_length=24, required=False))])))])), ('team_members_section', wagtail.core.blocks.StructBlock([('team', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('full_name', wagtail.core.blocks.CharBlock(max_length=25, required=True)), ('position', wagtail.core.blocks.CharBlock(max_length=25, required=True)), ('team_member_photo', wagtail.images.blocks.ImageChooserBlock(required=True)), ('bio_page', wagtail.core.blocks.URLBlock(required=False))])))])), ('recent_post_section', wagtail.core.blocks.StructBlock([]))], blank=True, null=True),
        ),
    ]
