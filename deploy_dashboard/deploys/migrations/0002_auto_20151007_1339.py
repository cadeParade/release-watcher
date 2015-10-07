# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploys', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='release',
            old_name='release_manager',
            new_name='dev_release_manager',
        ),
        migrations.AddField(
            model_name='release',
            name='pm_release_manager',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
