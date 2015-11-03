# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blog_title', models.CharField(max_length=250)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.TextField()),
                ('comment_date', models.DateTimeField(verbose_name=b'date posted')),
                ('comment_blog', models.ForeignKey(related_name='comments', to='blogs.Blog')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_caption', models.CharField(max_length=250, null=True)),
                ('content_text', models.TextField(null=True)),
                ('content_data', models.TextField(null=True)),
                ('file_extension', models.CharField(max_length=10, null=True)),
                ('created_date', models.DateTimeField()),
                ('blog', models.ForeignKey(related_name='contents', to='blogs.Blog')),
            ],
            options={
                'db_table': 'blogs_blog_contents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'blogs_content_type',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='content',
            name='content_type',
            field=models.ForeignKey(related_name='contentType', to='blogs.ContentType'),
            preserve_default=True,
        ),
    ]
