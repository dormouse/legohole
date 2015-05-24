# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('legosets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='legoset',
            name='add_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 24, 1, 2, 53, 655373, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='legoset',
            name='modi_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 24, 1, 4, 36, 247562, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
