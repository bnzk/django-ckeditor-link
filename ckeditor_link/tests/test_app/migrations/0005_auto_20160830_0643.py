# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0004_linkmodel_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmodel',
            name='when',
            field=models.DateTimeField(default='', blank=True),
        ),
    ]
