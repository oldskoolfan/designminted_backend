from blogapi.models import Blog, Comment, ContentType, Content
from django.db.models import Q
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import renderer_classes, api_view
from blogapi.renderers import ImageRenderer
from rest_framework.views import APIView
from blogapi.serializers import BlogSerializer, CommentSerializer, UserSerializer, \
    GroupSerializer, ContentSerializer, ContentTypeSerializer

class BlogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blogs to be viewed or edited.
    """
    permission_classes = (AllowAny,)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ImageView(APIView):
    renderer_classes = (ImageRenderer, )
    permission_classes = (AllowAny, )
    def get(*args, **kwargs):
        content = Content.objects.get(pk=kwargs['id'])
        return Response(content.content_data, content_type=content.file_extension)

class NewUserView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']
        existingUsers = User.objects.filter(Q(email=email) | Q(username=name))
        if existingUsers.count() == 0:
            user = User.objects.create_user(name, email, password)
            #serializer = UserSerializer(user, context={'request':request})
            return Response({"msg": "User created successfully!"})
        else:
            return Response({"msg": "Error: User already exists"})