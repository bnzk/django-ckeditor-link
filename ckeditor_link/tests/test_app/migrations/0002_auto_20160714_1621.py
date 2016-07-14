# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMSTestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('richtext', djangocms_text_ckeditor.fields.HTMLField()),
            ],
        ),
        migrations.AlterField(
            model_name='testmodel',
            name='richtext',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
