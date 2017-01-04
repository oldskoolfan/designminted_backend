from django.db import models
from django.contrib.auth.models import User, Group
import datetime
from django.utils import timezone
from inflector.languages.base import Base
from inflection import dasherize

class Blog(models.Model):
    class Meta:
        db_table = "blogs_blog"

    # class constants
    HOME = 1
    SERVICES = 2
    PORTFOLIO = 3
    BLOG = 4
    CONTACT = 5
    TESTIMONIALS = 6
    ABOUT = 7
    PAGE_TYPES = (
        (HOME, 'Home'),
        (SERVICES, 'Services'),
        (PORTFOLIO, 'Portfolio'),
        (BLOG, 'Blog'),
        (CONTACT, 'Contact'),
        (TESTIMONIALS, 'Testimonials'),
        (ABOUT, 'About')
    )

    page_type = models.IntegerField(choices=PAGE_TYPES, default=BLOG)
    user = models.ForeignKey(User)
    blog_title = models.CharField(max_length=250)
    pub_date = models.DateTimeField('date published')

    @property
    def has_comments(self):
        return self.comments.count() > 0

    @property
    def guid(self):
        inflector = Base()
        title = dasherize(inflector.urlize(unicode(self.blog_title)))
        guid = "http://designminted.com/blog/{0}/{1}/".format(self.id, title)
        return guid

    def __str__(self):
        return self.blog_title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class ContentType(models.Model):
    # class constants
    TEXT_TYPE = "TEXT"
    IMAGE_TYPE = "IMAGE"

    type_name = models.CharField(max_length=50)
    class Meta:
        db_table = "blogs_content_type"

class Content(models.Model):
    class Meta:
        db_table = "blogs_blog_contents"
        ordering = ["content_order"]
    blog = models.ForeignKey(Blog, related_name="contents")
    content_type = models.ForeignKey(ContentType, related_name="content_type", db_column="content_type_id")
    content_caption = models.CharField(max_length=250, null=True)
    content_text = models.TextField(null=True)
    content_data = models.BinaryField(null=True)
    content_order = models.PositiveIntegerField(null=True)
    file_extension = models.CharField(max_length=10, null=True)
    created_date = models.DateTimeField()

    @property
    def is_text(self):
        return self.content_type.type_name == ContentType.TEXT_TYPE

    @property
    def is_image(self):
        return self.content_type.type_name == ContentType.IMAGE_TYPE

class Comment(models.Model):
    class Meta:
        db_table = "blogs_comment"
    comment_blog = models.ForeignKey(Blog, related_name="comments")
    comment_text = models.TextField(null=True)
    comment_date = models.DateTimeField('date posted')
    is_approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True)
    def __str__(self):
        return self.comment_text

class ContactFormMessage(models.Model):
    class Meta:
        db_table = "contactform_message"
    firstname = models.CharField(max_length=250, null=False)
    lastname = models.CharField(max_length=250, null=False)
    email = models.CharField(max_length=250, null=False)
    message = models.TextField(null=False)
    created_date = models.DateTimeField(auto_now_add=True)


class ErrorMsg(object):
    def __init__(self, msg):
        self.msg = msg