# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField()),
                ('label', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Vip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=16)),
                ('address', models.GenericIPAddressField()),
                ('device', models.ForeignKey(to='vips.Device')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='login',
            field=models.ForeignKey(to='vips.Login'),
        ),
    ]
