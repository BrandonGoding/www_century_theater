from django.db import models
from django import forms
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


class BasicPage(Page):
    pass


@register_snippet
class BlogAuthor(models.Model):
    """Blog author for snippets."""
    name = models.CharField(max_length=100)
    bio = RichTextField(
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
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
                FieldPanel("bio"),
            ],
            heading="Author Name, Image and Bio",
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
                FieldPanel("facebook"),
                FieldPanel("twitter"),
                FieldPanel("linkedin"),
                FieldPanel("instagram"),
            ],
            heading="Links"
        )
    ]

    def __str__(self):
        """String repr of this class."""
        return self.name

    class Meta:  # noqa
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"


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
    author = models.ForeignKey(to=BlogAuthor, null=True, blank=True, on_delete=models.SET_NULL)
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
        MultiFieldPanel(
            [
                SnippetChooserPanel('author'),
                FieldPanel('content'),
            ],
            heading="Author & Content"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"
        )
    ]

    parent_page_types = ['website.BlogRollPage']
    subpage_types = []
