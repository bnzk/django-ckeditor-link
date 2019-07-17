from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_link.link_model.models import CMSFilerLinkBase, LinkBase

# compat
import django
if django.VERSION[:2] < (1, 10):
    from django.core.urlresolvers import reverse_lazy, reverse
else:
    from django.urls import reverse_lazy, reverse


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
    external_url = models.CharField(max_length=255, blank=True, default='',)
    email = models.EmailField(blank=True, default='',)
    # http://stackoverflow.com/questions/12644142/prefill-a-datetimefield-from-url-in-django-admin
    when = models.DateField(blank=True, null=True)
    testmodel = models.ForeignKey(
        TestModel,
        null=True,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
    )
    target = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return "LINK object: %s" % self.get_link()

    def get_link(self):
        # print(self.__dict__)
        if self.external_url:
            return self.external_url
        elif self.when:
            return self.when
        elif self.testmodel:
            return self.testmodel.get_absolute_url()
        elif self.target:
            return self.target
        else:
            return "http://no-link-given.com/"

    def get_link_target(self):
        return "_blank"

    def get_link_style(self):
        return "no-css-class"


class LinkModel(LinkModelBase):
    pass


class ContribLinkModel(LinkBase):
    pass


class CMSFilerLinkModel(CMSFilerLinkBase):
    pass
