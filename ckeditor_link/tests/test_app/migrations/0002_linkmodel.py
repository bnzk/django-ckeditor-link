# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target', models.CharField(default='', max_length=255, blank=True)),
                ('external_url', models.CharField(default='', max_length=255, blank=True)),
                ('testmodel', models.ForeignKey(default=None, blank=True, to='test_app.TestModel', null=True)),
            ],
        ),
    ]
