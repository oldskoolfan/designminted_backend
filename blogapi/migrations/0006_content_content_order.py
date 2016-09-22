# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapi', '0005_blog_page_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='content_order',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
