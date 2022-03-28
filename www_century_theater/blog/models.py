from django import forms
from django.db import models
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel
from wagtail.api import APIField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class BlogAuthor(models.Model):
    """Blog author for snippets."""
    last_name = models.CharField(max_length=45)
    first_name = models.CharField(max_length=65)
    tagline = models.CharField(max_length=120, default="This is a tagline please update it.")
    slug = models.SlugField(null=True, blank=False)
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
                FieldPanel("last_name"),
                FieldPanel("first_name"),
                FieldPanel("slug"),
                ImageChooserPanel("image"),
                FieldPanel("tagline"),
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
        return f"{self.last_name}, {self.first_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:  # noqa
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"

    # parent_page_types = []
    # subpage_types = []


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


class BlogRollPage(RoutablePageMixin, Page):
    max_count = 1
    subpage_types = ['blog.BlogPage']

    def get_context(self, request, *args, **kwargs):
        context = super(BlogRollPage, self).get_context(request)
        context['categories'] = BlogCategory.objects.all()
        context['routable_target'] = self.get_latest_revision_as_page().specific
        return context

    @route(r'^$')  # will override the default Page serving mechanism
    def recent_posts(self, request):
        """
        View function for the current events page
        """
        featured_post = BlogPage.objects.order_by('-post_date').live()[:1]
        posts = BlogPage.objects.order_by('-post_date').live()[1:5]
        return self.render(request, context_overrides={
            'featured_post': featured_post,
            'posts': posts,
        })

    @route(r'^authors/$')  # will override the default Page serving mechanism
    def authors_list(self, request):
        """
        View function for the current events page
        """
        template = 'blog/blog_authors_page.html'
        posts = BlogAuthor.objects.all()
        return self.render(request, context_overrides={
            'posts': posts,
        }, template=template)

    @route(r'^authors/(?P<author_slug>[-\w]*)/$')
    def recent_posts_by_author(self, request, author_slug):
        template = 'blog/blog_author.html'
        author = BlogAuthor.objects.get(slug=author_slug)
        posts = BlogPage.objects.order_by('-post_date').filter(author__slug=author_slug).live()[:4]
        return self.render(request, context_overrides={
            'author': author,
            'related_posts': posts,
        }, template=template)

    @route(r'^category/(?P<category_slug>[-\w]*)/$')  # will override the default Page serving mechanism
    def recent_posts_by_category(self, request, category_slug):
        """
        View function for the current events page
        """
        try:
            category = BlogCategory.objects.get(slug=category_slug)
            featured_post = BlogPage.objects.order_by('-post_date').filter(category=category).live()[:1]
            posts = BlogPage.objects.order_by('-post_date').filter(category=category).live()[1:5]
        except:
            featured_post = []
            posts = []
        return self.render(request, context_overrides={
            'featured_post': featured_post,
            'posts': posts,
        })


class BlogPage(Page):
    author = models.ForeignKey(to=BlogAuthor, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        "blog.BlogCategory",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    post_date = models.DateField(auto_created=True, null=False, blank=False)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )
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
                FieldPanel('post_date'),
                FieldPanel("category"),
                FieldPanel('content'),
            ],
            heading="Author & Content"
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel("featured_image"),
            ],
            heading="Featured Image"
        )
    ]

    parent_page_types = ['blog.BlogRollPage']
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request)
        context['categories'] = BlogCategory.objects.all()
        context['routable_target'] = self.get_parent().specific
        context['related_posts'] = BlogPage.objects.order_by('-post_date').filter(category=self.category).exclude(id=self.id).live()[:4]
        return context
