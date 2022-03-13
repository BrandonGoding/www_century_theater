import datetime
from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from blog.models import BlogPage
from streams.blocks import ParallaxBlock, FeaturesListBlock, TeamHighlightBlock, RecentPostsBlock, StudiosBlock


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

    def get_context(self, value, *args, **kwargs):
        context = super(BasicPage, self).get_context(value)
        context['featured_post'] = BlogPage.objects.order_by('-post_date').live()[:1]
        context['second_post'] = BlogPage.objects.order_by('-post_date').live()[1:2]
        context['post_row'] = BlogPage.objects.order_by('-post_date').live()[2:5]
        return context


class Movie(Page):
    RATING_CHOICES = (
        ("G - General Audiences", "G"),
        ("PG - Parental Guidance Suggested", "PG"),
        ("PG-13 Parents Strongly Cautioned", "PG-13"),
        ("NC-17 - Adults Only", "NC-17")
    )

    rating = models.CharField(max_length=35, choices=RATING_CHOICES, null=True, blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    youtube_id = models.CharField(max_length=25, null=True, blank=True)

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('rating'),
                ImageChooserPanel('featured_image'),
                FieldPanel('youtube_id')
            ],
            heading="Movie Header Info"
        ),
    ]
    parent_page_types = ['website.NowPlayingPage', 'website.ComingSoonPage']
    subpage_types = []


class NowPlayingPage(Page):
    body = StreamField([
        ('feature_list_section', FeaturesListBlock()),
        ('recent_post_section', RecentPostsBlock()),
        ('studio_logo_section', StudiosBlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    max_count = 1

    subpage_types = ['website.Movie']

    @property
    def first_day_of_week(self):
        current_day = datetime.date.today()
        return current_day - datetime.timedelta(days=current_day.weekday()) + datetime.timedelta(days=4)

    @property
    def last_day_of_week(self):
        current_day = datetime.date.today()
        return current_day - datetime.timedelta(days=current_day.weekday()) + datetime.timedelta(days=6)

    def get_context(self, value, *args, **kwargs):
        context = super(NowPlayingPage, self).get_context(value)
        context['now_playing'] = Movie.objects.all().live()[:2]
        return context


class ComingSoonPage(RoutablePageMixin, Page):
    max_count = 1

    subpage_types = ['website.Movie']

    @route(r'^$')  # will override the default Page serving mechanism
    def coming_soon_page(self, request):
        """
        View function for the current events page
        """
        return self.render(request, context_overrides={})
