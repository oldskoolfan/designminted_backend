__author__ = 'andrew'


from django.contrib.auth.models import User, Group
from blogapi.models import Blog, Content, ContentType, Comment
from rest_framework import serializers

import base64;

# class BlobField(serializers.Field):
# 	def to_representation(self, obj):
# 		return obj
# 	def to_internal_value(self, data):
# 		return base64.encodestring(data);

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
		fields = ('id', 'comment_text', 'comment_date')

class ContentTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ContentType
		fields = ('id', 'type_name')

class ContentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Content
		fields = ('id', 'content_type', 'content_caption', 'content_text', 'file_extension',
			'created_date')
	#contentformat = serializers.PrimaryKeyRelatedField(source='content_type', read_only=True)
	content_type = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
	#content_type = ContentTypeSerializer()

class BlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		#fields = ('id', 'blog_title', 'pub_date', 'user', 'contents', 'comments')
	#contents = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)
	#comments = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)
	contents = ContentSerializer(many=True)
	comments = CommentSerializer(many=True)

class BlogContentCommentSerializer(serializers.Serializer):
	blogs = BlogSerializer(many=True)
	contents = ContentSerializer(many=True)
	comments = CommentSerializer(many=True)
	content_formats = ContentTypeSerializer(many=True)