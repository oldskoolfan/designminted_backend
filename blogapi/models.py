from django.db import models
from django.contrib.auth.models import User, Group
import datetime
from django.utils import timezone

# Create your models here.
class Blog(models.Model):
    class Meta:
        db_table = "blogs_blog"
    user = models.ForeignKey(User)
    blog_title = models.CharField(max_length=250)
    #contents = models.ForeignKey(Content)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.blog_title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class ContentType(models.Model):
    type_name = models.CharField(max_length=50)
    class Meta:
        db_table = "blogs_content_type"

class Content(models.Model):
    class Meta:
        db_table = "blogs_blog_contents"
    blog = models.ForeignKey(Blog, related_name="contents")
    content_type = models.ForeignKey(ContentType, related_name="contentType")
    content_caption = models.CharField(max_length=250, null=True)
    content_text = models.TextField(null=True)
    #content_data = models.TextField(null=True)
    content_data = models.BinaryField(null=True)
    file_extension = models.CharField(max_length=10, null=True)
    created_date = models.DateTimeField()

class Comment(models.Model):
    class Meta:
        db_table = "blogs_comment"
    comment_blog = models.ForeignKey(Blog, related_name="comments")
    comment_text = models.TextField()
    comment_date = models.DateTimeField('date posted')
    def __str__(self):
        return self.comment_text