from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.base import View
from blogapi.models import *
from datetime import datetime

# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

class BlogView(TemplateView):
    template_name = "blogs.html"
    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.all();
        context = { "blogs": blogs }
        return render(request, self.template_name, context)

class DeleteBlogView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        blog = Blog.objects.get(pk=id)
        if blog != None: blog.delete()
        return HttpResponseRedirect('/admin/blogs/')


class BlogBaseView(TemplateView):
    def getIdFromList(selfself, list, index):
        try:
            return list[index]
        except IndexError:
            return None
    def addBlogContents(self, blog, request, ids):
        bodyList = request.POST.getlist('body')
        textType = ContentType.objects.get(id=1)
        imageType = ContentType.objects.get(id=2)
        idCounter = 0
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
        id = kwargs['id']
        blog = Blog.objects.get(pk=id)
        if blog != None:
            context = {"blog": blog}
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect('/admin/blogs/')
    def post(self, request, **kwargs):
        blog = Blog.objects.get(pk=request.POST['blogid'])
        contentIds = request.POST.getlist('contentid')
        self.addBlogContents(blog, request, contentIds)
        return HttpResponseRedirect('/admin/blogs/')

class AddNewBlogView(BlogBaseView):
    template_name = "blog-form.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    def post(self, request):
        contentIds = request.POST.getlist('contentid')
        blog = Blog(
            blog_title = request.POST['title'],
            pub_date = datetime.now(),
            user = request.user
        )
        blog.save()
        self.addBlogContents(blog, request, contentIds)
        return HttpResponseRedirect('/admin/blogs/')
