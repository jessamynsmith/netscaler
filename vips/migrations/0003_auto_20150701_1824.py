# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vips', '0002_vip_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vip',
            name='device',
            field=models.ForeignKey(related_name='vips', to='vips.Device'),
        ),
    ]
