from django.db import models
from django import forms
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet


class BasicPage(Page):
    pass


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text="A slug to identify posts by this category"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class BlogRollPage(Page):
    subpage_types = ['website.BlogPage']


class BlogPage(Page):
    categories = ParentalManyToManyField("website.BlogCategory", blank=True)
    content = RichTextField(
        blank=True,
        null=True,
        features=[
            'h3',
            'h4',
            'h5',
            'h6',
            'bold',
            'italic',
            'ol',
            'ul',
            'hr',
            'link',
            'document-link',
            'image',
            'embed',
            'superscript',
            'subscript',
            'strikethrough',
            'blockquote'
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel('content'),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"
        )
    ]

    parent_page_types = ['website.BlogRollPage']
    subpage_types = []
