from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from ckeditor.fields import RichTextField
# from djangocms_text_ckeditor.fields import HTMLField


@python_2_unicode_compatible
class TestModel(models.Model):
    title = models.CharField(max_length=255, )
    richtext = RichTextField()

    def __str__(self):
        return "%s" % self.title


# @python_2_unicode_compatible
# class CMSTestModel(models.Model):
#     title = models.CharField(max_length=255, )
#     richtext = HTMLField()
#
#     def __str__(self):
#         return "%s" % self.title

@python_2_unicode_compatible
class LinkModel(models.Model):
    target = models.CharField(max_length=255, blank=True, default='', )
    external_url = models.CharField(max_length=255, blank=True, default='',)
    testmodel = models.ForeignKey(TestModel, null=True, default=None, blank=True)

    def __str__(self):
        return "%s" % self.title
