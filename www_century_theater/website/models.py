from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from streams.blocks import ParallaxBlock, FeaturesListBlock


class BasicPage(Page):
    body = StreamField([
        ('parallax_section', ParallaxBlock()),
        ('feature_list_section', FeaturesListBlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

