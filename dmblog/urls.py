from django.conf.urls import include, url
from django.contrib import admin
from blogadmin.views import *
from blogweb.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # public site
    url(r'^$', HomeView.as_view(), name="index"),
    url('about/', AboutView.as_view(), name="about"),
    url('services/', ServicesView.as_view(), name="services"),
    url('portfolio/', PortfolioView.as_view(), name="portfolio"),
    url('contact/', ContactView.as_view(), name="contact"),
    url('testimonials/', TestimonialsView.as_view(), name="testimonials"),
    url(r'^blog/$', BlogPageView.as_view(), name="blog"),
    url(r'^blog/(?P<id>[0-9]+)/(?P<title>[a-z\-]+)/$', BlogPageView.as_view()),
    url('thank-you/', ThankYouView.as_view(), name="thankyou"),

    # admin stuff
    url(r'^admin/blogs/', BlogsView.as_view()),
    url(r'^admin/delete-blog/(?P<id>[0-9]+)', DeleteBlogView.as_view()),
    url(r'^admin/edit-blog/(?P<id>[0-9]+)', EditBlogView.as_view()),
    url(r'^admin/new-blog/', AddNewBlogView.as_view()),
    url(r'^admin/pages/', PagesView.as_view()),

    # misc
    url(r'get-img/(?P<id>[0-9]+)', GetImageView.as_view()),

    # rss
    url('rss/', RssFeedView.as_view(), name="rss"),
]
