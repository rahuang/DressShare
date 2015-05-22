# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20150520_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='dress',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
