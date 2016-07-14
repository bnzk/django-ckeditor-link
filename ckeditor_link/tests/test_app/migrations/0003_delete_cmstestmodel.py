# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_auto_20160714_1621'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CMSTestModel',
        ),
    ]
