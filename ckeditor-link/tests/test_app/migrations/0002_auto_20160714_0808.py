# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestInlineModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestInlineModelSingle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selection', models.CharField(blank=True, max_length=20, verbose_name='Selection', choices=[('', 'Empty'), ('horse', 'Horse'), ('bear', 'Bear'), ('octopus', 'Octopus')])),
                ('horse', models.CharField(max_length=20, blank=True)),
                ('bear', models.CharField(max_length=20, blank=True)),
                ('octopus', models.CharField(max_length=20, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestModelAdvanced',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('set', models.CharField(blank=True, max_length=20, verbose_name='Selection', choices=[('', 'Empty'), ('set1', '1'), ('set2', '2'), ('set3', '3')])),
                ('set1_1', models.CharField(max_length=20, blank=True)),
                ('set2_1', models.CharField(max_length=20, blank=True)),
                ('set2_2', models.CharField(max_length=20, blank=True)),
                ('set2_3', models.CharField(max_length=20, blank=True)),
                ('set3_1', models.CharField(max_length=20, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestModelInInlineModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestModelSingle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selection', models.CharField(blank=True, max_length=20, verbose_name='Selection', choices=[('', 'Empty'), ('horse', 'Horse'), ('bear', 'Bear'), ('octopus', 'Octopus')])),
                ('horse', models.CharField(max_length=20, blank=True)),
                ('bear', models.CharField(max_length=20, blank=True)),
                ('octopus', models.CharField(max_length=20, blank=True)),
            ],
        ),
        migrations.DeleteModel(
            name='TestModel',
        ),
        migrations.AddField(
            model_name='testinlinemodelsingle',
            name='parent',
            field=models.ForeignKey(to='test_app.TestModelInInlineModel'),
        ),
        migrations.AddField(
            model_name='testinlinemodel',
            name='parent',
            field=models.ForeignKey(to='test_app.TestModelAdvanced'),
        ),
    ]
