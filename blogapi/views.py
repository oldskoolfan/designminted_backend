from blogapi.models import Blog, Comment, ContentType, Content, ContactFormMessage, ErrorMsg
from django.db.models import Q
from django.views.decorators.gzip import gzip_page
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from blogapi.renderers import ImageRenderer
from rest_framework.views import APIView
from blogapi.serializers import BlogSerializer, CommentSerializer, UserSerializer, \
    GroupSerializer, ContentSerializer, ContentTypeSerializer, ContactFormMessageSerializer, \
    ErrorSerializer

class BlogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blogs to be viewed or edited.
    """
    permission_classes = (AllowAny,)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class ContactFormMessageViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = ContactFormMessage.objects.all()
    serializer_class = ContactFormMessageSerializer
    def create(self, request):
        try:
            serializer = ContactFormMessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                subject = "Contact Form Submission"
                message = request.data["message"]
                fromAddr = request.data["email"]
                toAddr = "designminted@gmail.com"
                #user = "harris.1305.autobot@gmail.com"
                #pwd = "Salem:28"

                # send email
                send_mail(subject, message, fromAddr, [toAddr], False)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer

class ContentViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """
    permission_classes = (AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username = username)
        return queryset

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

#@gzip_page
class ImageView(APIView):
    renderer_classes = (ImageRenderer, )
    permission_classes = (AllowAny, )

    @method_decorator(gzip_page)
    def dispatch(self, request, *args, **kwargs):
        return super(ImageView, self).dispatch(request, *args, **kwargs)

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
            User.objects.create_user(name, email, password)
            #return Response({"msg": "User created successfully!"})
            msg = "User created successfully!"
        else:
            #return Response({"msg": "Error: User already exists"})
            msg = "Error: User already exists"
        serializer = ErrorSerializer(ErrorMsg(msg=msg))
        return Response(serializer.data)

class UpdateCommentApprovalView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, **kwargs):
        approved = request.POST['approve'] == 'true'
        id = kwargs['id']
        comment = Comment.objects.get(pk=id)
        context = {}

        if comment != None:
            #comment.update(is_approved = approved)
            comment.is_approved = approved
            comment.save()
            context = CommentSerializer(comment).data
        return Response(context)