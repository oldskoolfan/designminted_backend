"""dmblogapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from blogapi import views
from blogwebapp.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'blogs', views.BlogViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'content-types', views.ContentTypeViewSet)
router.register(r'contents', views.ContentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^home/', IndexView.as_view()),
    #url(r'^about-us/', AboutView.as_view()),
    url(r'^admin/blogs/', BlogView.as_view()),
    url(r'^admin/delete-blog/(?P<id>[0-9]+)', DeleteBlogView.as_view()),
    url(r'^admin/edit-blog/(?P<id>[0-9]+)', EditBlogView.as_view()),
    url(r'^admin/new-blog/', AddNewBlogView.as_view()),
    url(r'get-img/(?P<id>[0-9]+)', views.ImageView.as_view()),
    url(r'create-user/', views.NewUserView.as_view()),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
