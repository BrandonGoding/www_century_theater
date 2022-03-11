from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ParallaxBlock(blocks.StructBlock):
    header = blocks.CharBlock(max_length=30, required=False)
    sub_header = blocks.CharBlock(max_length=250, required=False)
    background_image = ImageChooserBlock(required=True)

    class Meta:
        icon = 'edit'
        template = 'streams/parallax_block.html'


class FeaturesListBlock(blocks.StructBlock):

    feature = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("feature_name", blocks.CharBlock(max_length=25, required=True)),
                ("feature_summary", blocks.CharBlock(max_length=255, required=True)),
                ("icon_id", blocks.CharBlock(max_length=24, required=False))
            ]
        )
    )

    class Meta:
        icon = "edit"
        template = "streams/features_list_block.html"