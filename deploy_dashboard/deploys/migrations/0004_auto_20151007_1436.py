# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploys', '0003_release_extra_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='pm_release_manager',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
    ]
