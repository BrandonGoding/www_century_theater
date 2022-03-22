# Generated by Django 4.0.3 on 2022-03-22 02:09

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0055_remove_nowplayingpage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicpage',
            name='body',
            field=wagtail.core.fields.StreamField([('parallax_section', wagtail.core.blocks.StructBlock([('header', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('sub_header', wagtail.core.blocks.CharBlock(max_length=250, required=False)), ('background_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('links', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('link_text', wagtail.core.blocks.CharBlock(max_length=25, required=False)), ('link_page', wagtail.core.blocks.PageChooserBlock(required=False))])))])), ('feature_list_section', wagtail.core.blocks.StructBlock([('feature', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('feature_name', wagtail.core.blocks.CharBlock(max_length=25, required=True)), ('feature_summary', wagtail.core.blocks.CharBlock(max_length=255, required=True)), ('icon_id', wagtail.core.blocks.CharBlock(max_length=24, required=False))])))])), ('team_members_section', wagtail.core.blocks.StructBlock([('team', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('full_name', wagtail.core.blocks.CharBlock(max_length=25, required=True)), ('position', wagtail.core.blocks.CharBlock(max_length=25, required=True)), ('team_member_photo', wagtail.images.blocks.ImageChooserBlock(required=True)), ('bio_page', wagtail.core.blocks.URLBlock(required=False))])))])), ('recent_post_section', wagtail.core.blocks.StructBlock([]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='nowplayingpage',
            name='body',
            field=wagtail.core.fields.StreamField([('feature_list_section', wagtail.core.blocks.StructBlock([('feature', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('feature_name', wagtail.core.blocks.CharBlock(max_length=25, required=True)), ('feature_summary', wagtail.core.blocks.CharBlock(max_length=255, required=True)), ('icon_id', wagtail.core.blocks.CharBlock(max_length=24, required=False))])))])), ('recent_post_section', wagtail.core.blocks.StructBlock([])), ('studio_logo_section', wagtail.core.blocks.StructBlock([('studios', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(max_length=25, required=True)), ('logo', wagtail.images.blocks.ImageChooserBlock(required=True)), ('website', wagtail.core.blocks.URLBlock(required=True))])))]))], blank=True, null=True),
        ),
    ]
