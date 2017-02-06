from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from blogapi.models import *
from forms import ContactForm
from django.views.decorators.gzip import gzip_page
from django.utils.decorators import method_decorator
from django.conf import settings
from PIL import Image
import PyRSS2Gen
import MyRSS2
import datetime
import re
import os
from django.conf import settings as djangoSettings

# Create your views here.

class PublicBaseView(TemplateView):
    page_type = None
    def get(self, request, *args, **kwargs):
        blog = Blog.objects.filter(page_type=self.page_type).first()
        context = { "blog": blog }
        return render(request, self.template_name, context)

class HomeView(TemplateView):
    template_name = "home.html"
    def get(self, request, *args, **kwargs):
        items = Blog.objects.filter(page_type=Blog.PORTFOLIO).first().contents.all()[:3]
        context = { 'items': items }
        return render(request, self.template_name, context)

class ServicesView(PublicBaseView):
    page_type = Blog.SERVICES
    template_name = "services.html"

class AboutView(PublicBaseView):
    page_type = Blog.ABOUT
    template_name = "about.html"

class BlogPageView(TemplateView):
    template_name = "blog.html"
    def get(self, request, *args, **kwargs):
        # todo: add blogger feed to this page
        # if 'id' in kwargs:
        #     blogs = [Blog.objects.get(pk=kwargs['id'])]
        # else:
        #     blogs = Blog.objects.filter(page_type=Blog.BLOG).order_by('-pub_date')
        # context = { "blogs": blogs }
        context = { 'blogs': [] }
        return render(request, self.template_name, context)

class PortfolioView(PublicBaseView):
    page_type = Blog.PORTFOLIO
    template_name = "portfolio.html"

class ThankYouView(TemplateView):
    template_name = "thanks.html"

class ContactView(TemplateView):
    template_name = "contact.html"
    def get(self, request, *args, **kwargs):
        context = { "form": ContactForm() }
        return render(request, self.template_name, context)
    def post(self, request, **kwargs):
        form = ContactForm(request.POST)
        context = { "form": form }
        if form.is_valid():
            msg = form.save()
            subject = "Contact Form Submission"
            toAddr = "harris.1305@gmail.com" if settings.DEBUG else "maria@designminted.com"
            email = EmailMessage(
                subject,
                msg.message,
                'autobot@andrewfharris.com',
                [toAddr],
                reply_to=[msg.email],
            )
            try:
                email.send()
            except Exception as e:
                raise
            return HttpResponseRedirect('/thank-you/')
        return render(request, self.template_name, context)

class TestimonialsView(PublicBaseView):
    page_type = Blog.TESTIMONIALS
    template_name = "testimonials.html"

class GetImageView(View):
    @method_decorator(gzip_page)
    def get(self, request, *args, **kwargs):
        content = Content.objects.get(pk=kwargs['id'])
        return HttpResponse(content.content_data, content_type=content.file_extension)

class RssFeedView(View):
    def get(self, request):
        items = []
        blogs = Blog.objects.filter(page_type=Blog.BLOG).order_by('-pub_date')

        imageType = ContentType.objects.filter(type_name=ContentType.IMAGE_TYPE).first()
        for blog in blogs:
            img = blog.contents.filter(content_type_id=imageType.id).first()
            item = PyRSS2Gen.RSSItem(
                title = blog.blog_title,
                link = blog.guid,
                author = "maria@designminted.com (Maria)",
                pubDate = blog.pub_date,
                guid = PyRSS2Gen.Guid(blog.guid),
            )
            if img != None:
                item.enclosure = PyRSS2Gen.Enclosure(
                    url = "http://designminted.com/get-img/{0}/".format(img.id),
                    length = len(img.content_data),
                    type = img.file_extension,
                )
            items.append(item)

        rss = MyRSS2.MyRSS2(
            title = "Design Minted, LLC",
            link = "http://designminted.com",
            description = "Maria from Design Minted, LLC's interior decorating blog",
            lastBuildDate = datetime.datetime.now(),
            items = items,
        )

        rss.rss_attrs['xmlns:atom'] = "http://www.w3.org/2005/Atom"

        return HttpResponse(rss.to_xml(), content_type="application/rss+xml")

class UploadImageView(View):
    def post(self, request):
        path = self.resizeImage(request.FILES['image_upload'])
        return JsonResponse({ 'location': path })

    def resizeImage(self, upload):
        limit = 500000
        img = Image.open(upload.file)
        imgPath = "{0}{1}".format(djangoSettings.MEDIA_ROOT, upload.name)
        img.save(imgPath)
        width, height = img.size
        ratio = float(width) / float(height)
        quality = 100
        while os.path.getsize(imgPath) > limit:
            width -= 100
            quality -= 10
            height = int(width / ratio)
            img = img.resize((width, height), Image.ANTIALIAS)
            img.save(imgPath, quality=quality)
            img = Image.open(imgPath)
        return re.sub('blogweb', '', imgPath, 1)