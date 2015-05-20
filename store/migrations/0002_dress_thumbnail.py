# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dress',
            name='thumbnail',
            field=models.FileField(upload_to=store.models.get_upload_file_name, blank=True),
        ),
    ]
