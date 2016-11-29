from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from ckeditor.fields import RichTextField
# from djangocms_text_ckeditor.fields import HTMLField


@python_2_unicode_compatible
class TestModel(models.Model):
    title = models.CharField(max_length=255, )
    richtext = RichTextField(default='')
    richtext_second = RichTextField(default='')

    def __str__(self):
        return "%s" % self.title

    def get_absolute_url(self):
        return reverse('testmodel_detail', args=(self.id, ))


# @python_2_unicode_compatible
# class CMSTestModel(models.Model):
#     title = models.CharField(max_length=255, )
#     richtext = HTMLField()
#
#     def __str__(self):
#         return "%s" % self.title


@python_2_unicode_compatible
class LinkModelBase(models.Model):
    target = models.CharField(max_length=255, blank=True, default='', )
    external_url = models.CharField(max_length=255, blank=True, default='',)
    email = models.EmailField(blank=True, default='',)
    # http://stackoverflow.com/questions/12644142/prefill-a-datetimefield-from-url-in-django-admin
    when = models.DateField(blank=True, null=True)
    testmodel = models.ForeignKey(TestModel, null=True, default=None, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "LINK object: %s" % self.get_link()

    def get_link(self):
        if self.external_url:
            return self.external_url
        else:
            return "http://no-link-given.com/"

    def get_target(self):
        return "_blank"

    def get_css_class(self):
        return "no-css-class"


class LinkModel(LinkModelBase):
    pass
