# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legosets', '0003_auto_20150524_0416'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discount',
            old_name='legeset',
            new_name='legoset',
        ),
    ]
