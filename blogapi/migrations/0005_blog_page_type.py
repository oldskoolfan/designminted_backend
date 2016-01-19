# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapi', '0004_contactformmessage_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='page_type',
            field=models.IntegerField(default=4, choices=[(1, b'Home'), (2, b'Services'), (3, b'Portfolio'), (4, b'Blog'), (5, b'Contact'), (6, b'Testimonials')]),
        ),
    ]
