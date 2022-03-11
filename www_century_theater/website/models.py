from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from blog.models import BlogPage
from streams.blocks import ParallaxBlock, FeaturesListBlock, TeamHighlightBlock, RecentPostsBlock


class BasicPage(Page):
    body = StreamField([
        ('parallax_section', ParallaxBlock()),
        ('feature_list_section', FeaturesListBlock()),
        ('team_members_section', TeamHighlightBlock()),
        ('recent_post_section', RecentPostsBlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    def get_context(self, value):
        context = super(BasicPage, self).get_context(value)
        context['featured_post'] = BlogPage.objects.order_by('-post_date').live()[:1]
        context['second_post'] = BlogPage.objects.order_by('-post_date').live()[1:2]
        context['post_row'] = BlogPage.objects.order_by('-post_date').live()[2:5]
        return context

