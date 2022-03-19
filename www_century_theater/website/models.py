import datetime
from django.utils import timezone
from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel, \
    FieldRowPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from blog.models import BlogPage
from streams.blocks import ParallaxBlock, FeaturesListBlock, TeamHighlightBlock, RecentPostsBlock, StudiosBlock
from django.conf import settings as django_settings
import os
import json
import requests
from decouple import config


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


class ShowTime(models.Model):
    """Between 1 and 5 images for the home page carousel."""

    movie = ParentalKey('website.Movie', related_name='showtimes', null=True, on_delete=models.CASCADE)
    show_date = models.DateField(default=timezone.now())
    show_time = models.TimeField()
    matinee = models.BooleanField(default=False)

    panels = [
        FieldPanel('show_date'),
        FieldPanel('show_time'),
        FieldPanel('matinee')
    ]


class Movie(ClusterableModel):
    title = models.CharField(max_length=50, null=False, blank=False, default="TITLE")
    slug = models.SlugField(null=True, blank=True, auto_created=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    youtube_id = models.CharField(max_length=25, null=True, blank=True, verbose_name="YouTube ID")
    imdb_id = models.CharField(max_length=25, null=True, blank=True, verbose_name="IMDB ID")
    open_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    review_page = models.ForeignKey(
        'blog.BlogPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('slug'),
                ImageChooserPanel('featured_image'),
            ],
            "Movie Title & Slug"
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel('youtube_id'),
                        FieldPanel('imdb_id'),
                    ]
                ),
            ],
            "External Resources"
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel('open_date'),
                        FieldPanel('close_date'),
                    ]
                ),
            ],
            "Movie Run"
        ),
        MultiFieldPanel(
            [
                InlinePanel('showtimes')
            ],
            "Showtimes"
        ),
        MultiFieldPanel(
            [
                PageChooserPanel("review_page")
            ],
            "Rick's Review"
        )
    ]


    # def get_context(self, value, *args, **kwargs):
    #     context = super(Movie, self).get_context(value)
    #     showtimes = []
    #     show_dates = []
    #
    #     for show_date in self.showtimes.all():
    #         if show_date.show_date not in show_dates:
    #             show_dates.append(show_date.show_date)
    #
    #     for show_date in show_dates:
    #         time_list = []
    #         temp_dict = dict()
    #         temp_dict['date'] = show_date
    #         for time in ShowTime.objects.filter(show_date=show_date, page_id=self.id):
    #             time_list.append(time.show_time)
    #             temp_dict['times'] = time_list
    #         showtimes.append(temp_dict)
    #
    #     context['showtimes'] = showtimes
    #
    #     if self.imdb_id:
    #         if not os.path.exists(f'{django_settings.BASE_DIR}/cache/title_{self.imdb_id}.json'):
    #             title_dict = dict()
    #             title_dict['data'] = requests.get(f"https://imdb-api.com/en/API/Title/{config('imdb_api_key')}/{self.imdb_id}").json()
    #             title_dict['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    #             with open(f'{django_settings.BASE_DIR}/cache/title_{self.imdb_id}.json', 'w') as f:
    #                 json.dump(title_dict, f)
    #             f.close()
    #             context['imdb_title_data'] = title_dict.get('data')
    #         else:
    #             # Opening JSON file
    #             f = open(f'{django_settings.BASE_DIR}/cache/title_{self.imdb_id}.json')
    #             # returns JSON object as
    #             # a dictionary
    #             title_dict = json.load(f)
    #             context['imdb_title_data'] = title_dict.get('data')
    #             # Closing file
    #             f.close()
    #
    #         if not os.path.exists(f'{django_settings.BASE_DIR}/cache/reviews_{self.imdb_id}.json'):
    #             response = requests.get(f"https://imdb-api.com/en/API/Ratings/{config('imdb_api_key')}/{self.imdb_id}").json()
    #             with open(f'{django_settings.BASE_DIR}/cache/reviews_{self.imdb_id}.json', 'w') as f:
    #                 json.dump(response, f)
    #             f.close()
    #             context['reviews'] = response
    #         else:
    #             # Opening JSON file
    #             f = open(f'{django_settings.BASE_DIR}/cache/reviews_{self.imdb_id}.json')
    #
    #             # returns JSON object as
    #             # a dictionary
    #             context['reviews'] = json.load(f)
    #             # Closing file
    #             f.close()
    #     return context


class NowPlayingPage(RoutablePageMixin, Page):
    body = StreamField([
        ('feature_list_section', FeaturesListBlock()),
        ('recent_post_section', RecentPostsBlock()),
        ('studio_logo_section', StudiosBlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    max_count = 1

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
        context['now_playing'] = Movie.objects.filter(open_date__lte=timezone.now(), close_date__gte=timezone.now()).order_by('open_date')[:2]
        return context

    # TODO:  URL FOR DETAIL VIEW

    # TODO:  URL FOR UPCOMING VIEW



