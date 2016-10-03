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
    def getItemFromList(self, list, index):
        try:
            return list[index]
        except IndexError:
            return None

    def getIdFromList(self, list, index):
        try:
            id = list[index]
            return id if int(id) != -1 else None
        except (IndexError, ValueError):
            return None
    def addBlogContents(self, blog, request, ids):
        orderList = request.POST.getlist('position')
        bodyList = request.POST.getlist('body')
        typeList = request.POST.getlist("type")
        captionList = request.POST.getlist('caption')
        imageList = request.FILES.getlist('image')
        imageFlagList = request.POST.getlist("hasImage")

        textType = ContentType.objects.filter(type_name = 'TEXT').first()
        imageType = ContentType.objects.filter(type_name = 'IMAGE').first()
        itemCounter = 0
        imgCounter = 0
        imgTypeCounter = 0
        bodyCounter = 0

        # update blog title/page type if we need to
        blog.blog_title = request.POST['title']
        blog.page_type = request.POST['page-type']
        blog.save()

        for typeId in typeList:

            try:
                typeId = int(typeId)
            except ValueError:
                typeId = 0

            if typeId == imageType.id:
                hasImage = self.getItemFromList(imageFlagList, imgTypeCounter)
                hasImage = bool(int(hasImage)) # convert "0"/"1" to false/true
                image = self.getItemFromList(imageList, imgCounter) if hasImage else None
                if (image != None):
                    imgCounter += 1
                    data = image.file.read()
                    ext = image.content_type
                    defaults = {
                        'content_type': imageType,
                        'content_data': data,
                        'file_extension': ext,
                        'created_date': datetime.now(),
                        'content_order': self.getItemFromList(orderList, itemCounter),
                        'content_caption': self.getItemFromList(captionList, imgTypeCounter)
                    }
                else:
                    defaults = {
                        'content_type': imageType,
                        'content_order': self.getItemFromList(orderList, itemCounter),
                        'content_caption': self.getItemFromList(captionList, imgTypeCounter)
                    }
                blog.contents.update_or_create(
                    id = self.getIdFromList(ids, itemCounter),
                    defaults = defaults
                )
                imgTypeCounter += 1
            if typeId == textType.id:
                text = self.getItemFromList(bodyList, bodyCounter)
                bodyCounter += 1
                blog.contents.update_or_create(
                    id = self.getIdFromList(ids, itemCounter),
                    defaults = {
                        'content_type': textType,
                        'content_text': text,
                        'created_date': datetime.now(),
                        'content_order': self.getItemFromList(orderList, itemCounter),
                    }
                )
            itemCounter += 1

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
            context = {
                "blog": blog,
                "types": ContentType.objects.all(),
                "pageTypes": Blog.PAGE_TYPES
            }
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

        context = {
            "types": ContentType.objects.all(),
            "pageTypes": Blog.PAGE_TYPES
        }

        return render(request, self.template_name, context)

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
