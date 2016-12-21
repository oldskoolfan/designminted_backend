from django.shortcuts import render
from django.views.generic import TemplateView
from blogapi.models import *

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

class ContactView(TemplateView):
    template_name = "contact.html"

class TestimonialsView(PublicBaseView):
    page_type = Blog.TESTIMONIALS
    template_name = "testimonials.html"