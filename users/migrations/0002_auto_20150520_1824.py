# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='interests',
        ),
        migrations.AddField(
            model_name='profile',
            name='dresssize',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
