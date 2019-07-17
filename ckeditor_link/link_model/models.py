from __future__ import unicode_literals
try:
    from builtins import str
except ImportError:
    from __builtin__ import str

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .conf import (
    CKEDITOR_LINK_TYPE_CHOICES,
    CKEDITOR_LINK_USE_CMS_FILER,
)

# dropped in favour of builtins/str, see above
# try:
#     unicode('')
# except NameError:
#     unicode = str


class LinkBase(models.Model):
    # name = models.CharField(
    #     verbose_name=_('Link Text'),
    #     max_length=255,
    #     blank=True,
    #     default='',
    # )
    link_type = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name=_('Link type'),
    )
    link_style = models.CharField(
        max_length=64,
        blank=True,
        default='',
        verbose_name=_('Link Style'),
    )
    free = models.CharField(
        max_length=512,
        default='',
        blank=True,
        verbose_name=_("Internal / Other"),
    )
    external = models.URLField(
        blank=True,
        default='',
        verbose_name=_("External Address"),
    )
    mailto = models.EmailField(
        default='',
        blank=True,
        verbose_name=_("E-Mail"),
    )
    phone = models.CharField(
        max_length=64,
        default='',
        blank=True,
        verbose_name=_("Phone"),
    )

    class Meta:
        abstract = True

    def get_link(self):
        # if link type set, give priority!
        # this will alter your object!
        if self.link_type:
            for key, display in CKEDITOR_LINK_TYPE_CHOICES:
                if not key == self.link_type:
                    setattr(self, key, None)
        if self.free:
            return self.free
        elif self.external:
            link = self.external
            if not link.startswith('http'):
                link = 'http://%s' % link
            return link
        elif self.mailto:
            return "mailto:%s" % self.mailto
        elif self.phone:
            return "tel:%s" % self.phone
        return ''

    def get_link_text(self):
        obj = None
        if getattr(self, 'name', None):
            return self.name
        if self.link_type:
            obj = getattr(self, self.link_type, None)
        if not object is None:
            return str(obj)
        return ''

    def get_link_type(self):
        return self.link_type

    def get_link_style(self):
        return self.link_style

    def get_link_target(self):
        type = self.get_link_type()
        if type in ['file', 'external']:
            return "_blank"
        return ""


class Link(LinkBase):
    """
    if in installed apps, this will be created and available out of the box
    """
    pass


if CKEDITOR_LINK_USE_CMS_FILER:

    from cms.models import Page
    from cms.models.fields import PageField
    from filer.fields.file import FilerFileField


    class CMSFilerLinkBase(LinkBase):
        cms_page = PageField(
            null=True,
            on_delete=models.SET_NULL,
            blank=True,
        )
        file = FilerFileField(
            null=True,
            on_delete=models.SET_NULL,
            blank=True,
        )

        def __init__(self, *args, **kwargs):
            if kwargs.get('page', None):
                self.cms_page = kwargs.get('page')
            return super(CMSFilerLinkBase, self).__init__(*args, **kwargs)

        class Meta:
            abstract = True

        def get_link(self):
            # best practice is to call super first, so not relevant attrs are nulled
            super_link = super(CMSFilerLinkBase, self).get_link()
            if self.cms_page_id:
                try:
                    page_url = self.cms_page.get_absolute_url()
                except Page.DoesNotExist:
                    return ''
                site = getattr(self.cms_page, 'site', None)
                if not site:
                    site = self.cms_page.node.site  # cms 3.5 or 3.6 and up.
                if site.id == settings.SITE_ID:
                    return page_url
                else:
                    return 'http:/fields /' + self.cms_page.site.domain + page_url
            elif self.file:
                return self.file.url
            return super_link

        def get_link_target(self):
            type = self.get_link_type()
            if type == 'cms_page' or type == 'page' and self.cms_page and not self.cms_page.site.id == settings.SITE_ID:
                return "_blank"
            else:
                return super(CMSFilerLinkBase, self).get_link_target()
