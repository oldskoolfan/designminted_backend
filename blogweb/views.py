from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from blogapi.models import *
from forms import ContactForm
from django.views.decorators.gzip import gzip_page
from django.utils.decorators import method_decorator

# Create your views here.

class PublicBaseView(TemplateView):
    page_type = None
    def get(self, request, *args, **kwargs):
        blog = Blog.objects.filter(page_type=self.page_type).first()
        context = { "blog": blog }
        return render(request, self.template_name, context)

class HomeView(PublicBaseView):
    page_type = Blog.HOME
    template_name = "home.html"

class ServicesView(PublicBaseView):
    page_type = Blog.SERVICES
    template_name = "services.html"

class AboutView(PublicBaseView):
    page_type = Blog.ABOUT
    template_name = "about.html"

class BlogPageView(TemplateView):
    template_name = "blog.html"
    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.filter(page_type=Blog.BLOG)
        context = { "blogs": blogs }
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
            toAddr = "harris.1305@gmail.com"
            email = EmailMessage(
                subject,
                msg.message,
                msg.email,
                [toAddr],
                reply_to=[msg.email],
            )
            email.send()
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