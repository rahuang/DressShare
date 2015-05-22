# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20150520_1824'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dress',
            old_name='thumbnail',
            new_name='picture',
        ),
        migrations.AddField(
            model_name='dress',
            name='availability',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dress',
            name='color',
            field=models.TextField(default='blue'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dress',
            name='formality',
            field=models.CharField(default='N', max_length=1, choices=[(b'B', b'Black-Tie'), (b'C', b'Cocktail'), (b'N', b'Night-Out'), (b'D', b'Day-Time')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dress',
            name='length',
            field=models.CharField(default='long', max_length=4, choices=[(b'mini', b'Mini'), (b'mid', b'Mid-Thigh'), (b'knee', b'Knee'), (b'tea', b'Tea'), (b'long', b'Long')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dress',
            name='size',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
