import datetime

from django.forms import widgets
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    StreamFieldPanel,
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
    FieldRowPanel,
)
from wagtail.api import APIField
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtailseo.models import SeoMixin

from blog.models import BlogPage
from streams.blocks import (
    ParallaxBlock,
    FeaturesListBlock,
    TeamHighlightBlock,
    RecentPostsBlock,
    StudiosBlock,
)
from django.conf import settings as django_settings
import os
import json
import requests
from decouple import config


class BasicPage(SeoMixin, Page):
    body = StreamField(
        [
            ("parallax_section", ParallaxBlock()),
            ("feature_list_section", FeaturesListBlock()),
            ("team_members_section", TeamHighlightBlock()),
            ("recent_post_section", RecentPostsBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]

    promote_panels = SeoMixin.seo_panels

    def get_context(self, value, *args, **kwargs):
        context = super(BasicPage, self).get_context(value)
        context["post_row"] = BlogPage.objects.order_by("-post_date").live()[:3]
        return context

    @property
    def seo_struct_org_dict(self) -> dict:
        sd_dict = super().seo_struct_org_dict
        sd_dict.update(
            {
                "sameAs": [
                    "https://www.facebook.com/TheCenturyTheater/",
                    "https://www.instagram.com/thecenturytheater/",
                ]
            }
        )

        return sd_dict


class FormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class ContactPage(AbstractEmailForm):
    max_count = 1
    template = "website/contact_form.html"
    landing_page_template = "website/contact_form.html"

    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel("form_fields", label="Form Fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            heading="Email Settings",
        ),
    ]

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        for name, field in form.fields.items():
            # here we want to adjust the widgets on each field
            # if the field is a TextArea - adjust the rows
            if isinstance(field.widget, widgets.Textarea):
                field.widget.attrs.update({"rows": "5"})
            # for all fields, get any existing CSS classes and add 'form-control'
            # ensure the 'class' attribute is a string of classes with spaces
            css_classes = field.widget.attrs.get("class", "").split()
            css_classes.append("form-control")
            field.widget.attrs.update({"class": " ".join(css_classes)})
        return form


@register_snippet
class Theater(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


@register_snippet
class Rate(models.Model):
    name = models.CharField(max_length=25)
    fee = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.fee}"


class ShowTime(models.Model):
    """Between 1 and 5 images for the home page carousel."""

    movie = ParentalKey(
        "website.Movie", related_name="showtimes", null=True, on_delete=models.CASCADE
    )
    show_date = models.DateField(default=None)
    show_time = models.TimeField()
    matinee = models.BooleanField(default=False)
    on_sale = models.BooleanField(default=False)
    theater = models.ForeignKey(to=Theater, on_delete=models.SET_NULL, null=True, blank=True)

    panels = [
        FieldPanel("show_date"),
        FieldPanel("show_time"),
        FieldPanel("theater"),
        FieldPanel("matinee"),
        FieldPanel("on_sale"),
    ]


class Movie(ClusterableModel):
    title = models.CharField(max_length=50, null=False, blank=False, default="TITLE")
    slug = models.SlugField(null=True, blank=True, auto_created=True)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    youtube_id = models.CharField(
        max_length=25, null=True, blank=True, verbose_name="YouTube ID"
    )
    imdb_id = models.CharField(
        max_length=25, null=True, blank=True, verbose_name="IMDB ID"
    )
    open_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    review_page = models.ForeignKey(
        "blog.BlogPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="movies",
    )

    def __str__(self):
        return self.title

    @property
    def last_day_for_calender(self):
        return self.close_date + datetime.timedelta(days=1)

    @property
    def get_description(self):
        return NowPlayingPage.get_imdb_json(self).get("plot", False)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("slug"),
                ImageChooserPanel("featured_image"),
                FieldPanel("confirmed"),
            ],
            "Movie Title & Slug",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("youtube_id"),
                        FieldPanel("imdb_id"),
                    ]
                ),
            ],
            "External Resources",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("open_date"),
                        FieldPanel("close_date"),
                    ]
                ),
            ],
            "Movie Run",
        ),
        MultiFieldPanel([InlinePanel("showtimes")], "Showtimes"),
        MultiFieldPanel([PageChooserPanel("review_page")], "Rick's Review"),
    ]

    api_fields = [APIField("youtube_id"), APIField("imdb_id")]


class NowPlayingPage(RoutablePageMixin, Page):
    body = StreamField(
        [
            ("feature_list_section", FeaturesListBlock()),
            ("recent_post_section", RecentPostsBlock()),
            ("studio_logo_section", StudiosBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]

    max_count = 1

    @property
    def first_day_of_week(self):
        current_day = datetime.date.today()
        return (
            current_day
            - datetime.timedelta(days=current_day.weekday())
            + datetime.timedelta(days=4)
        )

    @property
    def last_day_of_week(self):
        current_day = datetime.date.today()
        return (
            current_day
            - datetime.timedelta(days=current_day.weekday())
            + datetime.timedelta(days=6)
        )

    def get_context(self, value, *args, **kwargs):
        context = super(NowPlayingPage, self).get_context(value)
        context["now_playing"] = Movie.objects.filter(
            close_date__gte=self.first_day_of_week, open_date__lt=self.last_day_of_week
        ).order_by("open_date")[:2]
        return context

    @staticmethod
    def get_imdb_json(movie):
        if not os.path.exists(
            f"{django_settings.BASE_DIR}/cache/title_{movie.imdb_id}.json"
        ):
            title_dict = dict()
            title_dict["data"] = requests.get(
                f"https://imdb-api.com/en/API/Title/{config('imdb_api_key')}/{movie.imdb_id}"
            ).json()
            title_dict["timestamp"] = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )
            with open(
                    f"{django_settings.BASE_DIR}/cache/title_{movie.imdb_id}.json", "w"
            ) as f:
                json.dump(title_dict, f)
            f.close()
            return title_dict.get("data")
        else:
            f = open(f"{django_settings.BASE_DIR}/cache/title_{movie.imdb_id}.json")
            title_dict = json.load(f)
            if (
                datetime.datetime.fromisoformat(title_dict.get("timestamp"))
                + datetime.timedelta(hours=24)
                < datetime.datetime.now()
            ):
                os.remove(f"{django_settings.BASE_DIR}/cache/title_{movie.imdb_id}.json")
                NowPlayingPage.get_imdb_json(movie)
            else:
                return title_dict.get("data")
            f.close()

        # if not os.path.exists(
        #     f"{django_settings.BASE_DIR}/cache/reviews_{movie.imdb_id}.json"
        # ):
        #     response = requests.get(
        #         f"https://imdb-api.com/en/API/Ratings/{config('imdb_api_key')}/{movie.imdb_id}"
        #     ).json()
        #     with open(
        #         f"{django_settings.BASE_DIR}/cache/reviews_{movie.imdb_id}.json",
        #         "w",
        #     ) as f:
        #         json.dump(response, f)
        #     f.close()
        #     context["reviews"] = response
        # else:
        #     f = open(
        #         f"{django_settings.BASE_DIR}/cache/reviews_{movie.imdb_id}.json"
        #     )
        #     context["reviews"] = json.load(f)
        #     f.close()

    @route(r"^search/$")
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get("q", None)
        self.posts = self.get_posts()
        if search_query:
            self.posts = self.posts.search(search_query)
        return self.render(request)

    @route(r"^(?P<slug>[-\w]*)/detail/$")
    def movie_detail_page(self, request, slug, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        movie = get_object_or_404(Movie, slug=slug)
        context["movie"] = movie
        showtimes = []
        show_week = []

        for week in movie.showtimes.all():

            if datetime.datetime.fromisoformat(
                str(week.show_date)
            ).isocalendar().week not in [
                value for elem in show_week for value in elem.values()
            ]:
                show_dates = []
                for show_date in movie.showtimes.all():
                    if (
                        show_date.show_date
                        not in [value for elem in show_dates for value in elem.values()]
                        and show_date.show_date.isocalendar().week
                        == datetime.datetime.fromisoformat(str(week.show_date))
                        .isocalendar()
                        .week
                    ):
                        time_list = []
                        for time in ShowTime.objects.filter(
                            show_date=show_date.show_date, movie_id=movie.id
                        ):
                            time_list.append(time.show_time)
                        show_dates.append(
                            {"date": show_date.show_date, "times": time_list}
                        )

                show_week.append(
                    {
                        "week": datetime.datetime.fromisoformat(str(week.show_date))
                        .isocalendar()
                        .week,
                        "dates": show_dates,
                    }
                )

        context["showtimes"] = show_week

        if movie.imdb_id:
            context["imdb_title_data"] = self.get_imdb_json(movie)

        return render(request, "website/movie.html", context)

    @route(r"upcoming/$")
    def upcoming_movies_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["movies"] = Movie.objects.filter(
            open_date__gt=datetime.datetime.now() - datetime.timedelta(days=31)
        )
        context["up_next"] = Movie.objects.filter(
            open_date__gt=datetime.datetime.now()
        ).order_by("open_date")[:2]
        return render(request, "website/upcoming_movies.html", context)
