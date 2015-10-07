# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploys', '0002_auto_20151007_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='extra_detail',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
