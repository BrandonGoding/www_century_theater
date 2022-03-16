import datetime
from django.utils import timezone
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
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


class ShowTime(Orderable):
    """Between 1 and 5 images for the home page carousel."""

    page = ParentalKey("website.Movie", related_name="showtimes")
    show_date = models.DateField(default=timezone.now())
    show_time = models.TimeField()
    matinee = models.BooleanField(default=False)

    panels = [
        FieldPanel('show_date'),
        FieldPanel('show_time'),
        FieldPanel('matinee')
    ]


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
    open_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    review_page = models.ForeignKey(
        'blog.BlogPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('rating'),
                ImageChooserPanel('featured_image'),
                FieldPanel('youtube_id'),
                FieldPanel('open_date'),
                FieldPanel('close_date'),
            ],
            heading="Movie Header Info"
        ),
        MultiFieldPanel(
            [
                InlinePanel("showtimes", label="ShowTime")
            ],
            heading="Showtimes"
        ),
        MultiFieldPanel(
            [
                PageChooserPanel('review_page', 'blog.BlogPage'),
            ],
            heading="Review Page"
        )
    ]
    parent_page_types = ['website.NowPlayingPage', 'website.ComingSoonPage']
    subpage_types = []

    def get_context(self, value, *args, **kwargs):
        context = super(Movie, self).get_context(value)
        showtimes = []
        show_dates = []

        for show_date in self.showtimes.all():
            if show_date.show_date not in show_dates:
                show_dates.append(show_date.show_date)

        print(show_dates)

        for show_date in show_dates:
            time_list = []
            temp_dict = dict()
            temp_dict['date'] = show_date
            for time in ShowTime.objects.filter(show_date=show_date, page_id=self.id):
                time_list.append(time.show_time)
                temp_dict['times'] = time_list
            showtimes.append(temp_dict)

        context['showtimes'] = showtimes
        return context


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
        context['now_playing'] = Movie.objects.filter(open_date__lte=timezone.now(), close_date__gte=timezone.now()).live()[:2]
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
