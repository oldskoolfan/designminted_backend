# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapi', '0003_contactformmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactformmessage',
            name='message',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
