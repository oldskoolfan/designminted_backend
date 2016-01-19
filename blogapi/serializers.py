__author__ = 'andrew'


from django.contrib.auth.models import User, Group
from blogapi.models import Blog, Content, ContentType, Comment, ContactFormMessage
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'url', 'username', 'email', 'groups')

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		# fields = ('id', 'comment_text', 'comment_date', 'comment_blog',
		# 		  'user')
		user = UserSerializer

class ContentTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ContentType
		fields = ('id', 'type_name')

class ContentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Content
		fields = ('id', 'content_type', 'content_caption', 'content_text', 'file_extension',
			'created_date')
	content_type = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

class BlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
	contents = ContentSerializer(many=True)
	comments = CommentSerializer(many=True)

class BlogContentCommentSerializer(serializers.Serializer):
	blogs = BlogSerializer(many=True)
	contents = ContentSerializer(many=True)
	comments = CommentSerializer(many=True)
	content_formats = ContentTypeSerializer(many=True)

class ContactFormMessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ContactFormMessage