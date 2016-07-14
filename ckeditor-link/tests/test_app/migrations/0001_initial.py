# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selection', models.CharField(blank=True, max_length=20, verbose_name='Selection', choices=[('', 'Empty'), ('hors', 'Horse'), ('bear', 'Bear'), ('octopus', 'Octopus')])),
                ('horse', models.CharField(max_length=20, blank=True)),
                ('bear', models.CharField(max_length=20, blank=True)),
                ('octopus', models.CharField(max_length=20, blank=True)),
            ],
        ),
    ]
