# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legosets', '0002_auto_20150524_0104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discount',
            old_name='number',
            new_name='legeset',
        ),
    ]
