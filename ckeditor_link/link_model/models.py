from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from conf import CKEDITOR_LINK_TYPE_CHOICES

class LinkBase(models.Model):
    name = models.CharField(
        verbose_name=_('Link Text'),
        max_length=255,
        blank=True,
        default='',
    )
    link_class = models.CharField(
        verbose_name=_('Link Style'),
        max_length=64,
        blank=True,
        default='',
    )
    link_type = models.CharField(
        verbose_name=_('Link'),
        max_length=20,
        blank=True,
        default='',
    )
    external = models.URLField(
        null=True,
        blank=True,
    )
    mailto = models.EmailField(
        null=True,
        blank=True,
    )
    free = models.CharField(
        max_length=512,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def get_link(self):
        if self.link_type == 'newsletter':
            return "#newsletter-signup"
        if self.link_type:
            for key, display in CKEDITOR_LINK_TYPE_CHOICES:
                if not key == self.link_type:
                    setattr(self, key, None)
        if self.page_id:
            try:
                page_url = self.page.get_absolute_url()
            except Page.DoesNotExist:
                return ''
            if self.page.site.id == settings.SITE_ID:
                return page_url
            else:
                return 'http://' + self.page.site.domain + page_url
        if self.article:
            return self.article.get_absolute_url()
            # return 'http://' + self.article.site.domain + self.article.get_absolute_url()
        elif self.file:
            return self.file.url
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
        elif self.page:
            obj = self.page
        elif self.article:
            obj = self.article
        elif self.file:
            obj = self.file
        elif self.external:
            return self.external
        elif self.mailto:
            return self.mailto

        if not object is None:
            return unicode(obj)
        return ''

    def get_link_type(self):
        return self.link_type

    def get_link_cssclass(self):
        if self.link_type == 'newsletter':
            return "newsletter_overlay " + self.link_style
        return self.link_style

    def get_link_target(self):
        type = self.get_link_type()
        if type in ['file', 'external']\
                or (type == 'page' and self.page and not self.page.site.id == settings.SITE_ID):
            return "_blank"
        return ""


if False:
    class CMSLinkBase(LinkBase):
        page = PageField(
            null=True,
            blank=True
        )
        file = FilerFileField(
            null=True,
            blank=True,
        )