# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vips', '0004_auto_20150701_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=32)),
                ('address', models.GenericIPAddressField()),
                ('port', models.IntegerField()),
                ('state', models.CharField(max_length=16)),
                ('effective_state', models.CharField(max_length=16)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(related_name='vips', to='vips.Device')),
            ],
        ),
    ]
