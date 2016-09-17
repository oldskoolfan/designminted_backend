from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.base import View
from blogapi.models import *
from datetime import datetime

# Create your views here.

class AdminBaseView(TemplateView):
    def __init__(self):
        TemplateView.__init__(self)
        self.isAuthenticated = False
    def authenticate(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/admin/login/?next=/admin/blogs/')
        self.isAuthenticated = True
        return

class BlogView(AdminBaseView):
    template_name = "blogs.html"
    def get(self, request, *args, **kwargs):

        # make sure we're authenticated
        redirect = self.authenticate(request)
        if not self.isAuthenticated:
            return redirect

        blogs = Blog.objects.filter(page_type=Blog.BLOG)
        context = { "blogs": blogs }
        return render(request, self.template_name, context)

class PagesBlogView(AdminBaseView):
    template_name = "pages.html"
    def get(self, request):

        # make sure we're authenticated
        redirect = self.authenticate(request)
        if not self.isAuthenticated:
            return redirect

        blogs = Blog.objects.filter(~Q(page_type = Blog.BLOG))
        context = { "blogs": blogs }
        return render(request, self.template_name, context)

class DeleteBlogView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        blog = Blog.objects.get(pk=id)
        if blog != None: blog.delete()
        return HttpResponseRedirect('/admin/blogs/')


class BlogBaseView(AdminBaseView):
    def getIdFromList(self, list, index):
        try:
            return list[index]
        except IndexError:
            return None
    def addBlogContents(self, blog, request, ids):
        bodyList = request.POST.getlist('body')
        textType = ContentType.objects.get(id=1)
        imageType = ContentType.objects.get(id=2)
        idCounter = 0

        # update blog title if we need to
        blog.blog_title = request.POST['title']
        blog.save()

        for text in bodyList:
            blog.contents.update_or_create(
                id = self.getIdFromList(ids, idCounter),
                defaults = {
                    'content_type': textType,
                    'content_text': text,
                    'created_date': datetime.now()
                }
            )
            idCounter += 1
        imageList = request.FILES.getlist('image')
        for image in imageList:
            data = image.file.read()
            ext = image.content_type
            blog.contents.update_or_create(
                id = self.getIdFromList(ids, idCounter),
                defaults = {
                    'content_type': imageType,
                    'content_data': data,
                    'file_extension': ext,
                    'created_date': datetime.now()
                }
            )
            idCounter += 1

class EditBlogView(BlogBaseView):
    template_name = "blog-form.html"
    def get(self, request, **kwargs):

        # make sure we're authenticated
        redirect = self.authenticate(request)
        if not self.isAuthenticated:
            return redirect

        id = kwargs['id']
        blog = Blog.objects.get(pk=id)
        if blog != None:
            context = {"blog": blog}
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect('/admin/blogs/')

    def post(self, request, **kwargs):

        # make sure we're authenticated
        redirect = self.authenticate(request)
        if not self.isAuthenticated:
            return redirect

        blog = Blog.objects.get(pk=request.POST['blogid'])
        contentIds = request.POST.getlist('contentid')
        self.addBlogContents(blog, request, contentIds)

        link = '/admin/blogs/' if blog.page_type == Blog.BLOG else '/admin/pages/'
        return HttpResponseRedirect(link)

class AddNewBlogView(BlogBaseView):
    template_name = "blog-form.html"
    def get(self, request, *args, **kwargs):

        # make sure we're authenticated
        redirect = self.authenticate(request)
        if not self.isAuthenticated:
            return redirect

        return render(request, self.template_name)

    def post(self, request):

        # make sure we're authenticated
        redirect = self.authenticate(request)
        if not self.isAuthenticated:
            return redirect

        contentIds = request.POST.getlist('contentid')
        blog = Blog(
            blog_title = request.POST['title'],
            pub_date = datetime.now(),
            user = request.user
        )
        blog.save()
        self.addBlogContents(blog, request, contentIds)
        return HttpResponseRedirect('/admin/blogs/')
