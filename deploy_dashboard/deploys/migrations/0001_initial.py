# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(max_length=10)),
                ('code_freeze_date', models.DateTimeField()),
                ('production_release_date', models.DateTimeField()),
                ('release_manager', models.CharField(max_length=200)),
            ],
        ),
    ]
