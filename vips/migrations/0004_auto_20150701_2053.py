# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vips', '0003_auto_20150701_1824'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=16)),
                ('address', models.GenericIPAddressField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(related_name='servers', to='vips.Device')),
            ],
        ),
        migrations.RemoveField(
            model_name='vip',
            name='device',
        ),
        migrations.DeleteModel(
            name='Vip',
        ),
    ]
