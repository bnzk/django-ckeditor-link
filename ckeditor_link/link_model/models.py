from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from conf import CKEDITOR_LINK_TYPE_CHOICES, CKEDITOR_LINK_USE_CMS_FILER


class LinkBase(models.Model):
    # name = models.CharField(
    #     verbose_name=_('Link Text'),
    #     max_length=255,
    #     blank=True,
    #     default='',
    # )
    link_type = models.CharField(
        verbose_name=_('Link'),
        max_length=20,
        blank=True,
        default='',
    )
    link_class = models.CharField(
        verbose_name=_('Link Style'),
        max_length=64,
        blank=True,
        default='',
    )
    external = models.URLField(
        null=True,
        blank=True,
        verbose_name=_("External Address"),
    )
    mailto = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_("E-Mail"),
    )
    free = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name=_("Other"),
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
        return ''

    def get_link_text(self):
        obj = None
        if self.name:
            return self.name
        if self.link_type:
            obj = getattr(self, self.link_type, None)
        if not object is None:
            # TODO: python3
            return unicode(obj)
        return ''

    def get_link_type(self):
        return self.link_type

    def get_link_cssclass(self):
        return self.link_style

    def get_link_target(self):
        type = self.get_link_type()
        if type in ['file', 'external']:
            return "_blank"
        return ""


if CKEDITOR_LINK_USE_CMS_FILER:

    from cms.models import Page
    from cms.fields import PageField
    from filer.fields import FilerFileField


    class CMSFilerLinkBase(LinkBase):
        page = PageField(
            null=True,
            blank=True
        )
        file = FilerFileField(
            null=True,
            blank=True,
        )

        class Meta:
            abstract = True

        def get_link(self):
            # best practice is to call super first, so not relevant attrs are nulled
            super_link = super(CMSFilerLinkBase, self).get_link()
            if self.page_id:
                try:
                    page_url = self.page.get_absolute_url()
                except Page.DoesNotExist:
                    return ''
                if self.page.site.id == settings.SITE_ID:
                    return page_url
                else:
                    return 'http:/fields /' + self.page.site.domain + page_url
            elif self.file:
                return self.file.url
            return super_link

        def get_link_target(self):
            type = self.get_link_type()
            if type == 'page' and self.page and not self.page.site.id == settings.SITE_ID:
                return "_blank"
            else:
                return super(CMSFilerLinkBase, self).get_link_target()
