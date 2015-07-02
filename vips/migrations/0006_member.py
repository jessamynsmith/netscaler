# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vips', '0005_vip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=32)),
                ('address', models.GenericIPAddressField()),
                ('port', models.IntegerField()),
                ('protocol', models.CharField(max_length=16)),
                ('state', models.CharField(max_length=16)),
                ('update', models.DateTimeField(auto_now=True)),
                ('vip', models.ForeignKey(related_name='members', to='vips.Vip')),
            ],
        ),
    ]
