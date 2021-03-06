from wagtail.core import blocks
from wagtail.core.blocks import PageChooserBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock


class ParallaxBlock(blocks.StructBlock):
    header = blocks.CharBlock(max_length=30, required=False)
    sub_header = RichTextBlock(features=["h2", "h3", "h4", "h5", "h6", "bold", "italic"])
    background_image = ImageChooserBlock(required=True)
    links = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("link_text", blocks.CharBlock(max_length=25, required=False)),
                ("link_page", PageChooserBlock(required=False)),
            ]
        )
    )

    class Meta:
        icon = "edit"
        template = "streams/parallax_block.html"


class FeaturesListBlock(blocks.StructBlock):

    feature = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("feature_name", blocks.CharBlock(max_length=25, required=True)),
                ("feature_summary", blocks.CharBlock(max_length=255, required=True)),
                ("icon_id", blocks.CharBlock(max_length=24, required=False)),
            ]
        )
    )

    class Meta:
        icon = "edit"
        template = "streams/features_list_block.html"


class TeamHighlightBlock(blocks.StructBlock):

    team = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("full_name", blocks.CharBlock(max_length=25, required=True)),
                ("position", blocks.CharBlock(max_length=25, required=True)),
                ("team_member_photo", ImageChooserBlock(required=True)),
                ("bio_page", blocks.URLBlock(required=False)),
            ]
        )
    )

    class Meta:
        icon = "edit"
        template = "streams/team_hightlight_block.html"


class RecentPostsBlock(blocks.StructBlock):
    class Meta:
        icon = "edit"
        template = "streams/recent_post_block.html"


class StudiosBlock(blocks.StructBlock):

    studios = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("name", blocks.CharBlock(max_length=25, required=True)),
                ("logo", ImageChooserBlock(required=True)),
                ("website", blocks.URLBlock(required=True)),
            ]
        )
    )

    class Meta:
        icon = "edit"
        template = "streams/studios_block.html"
