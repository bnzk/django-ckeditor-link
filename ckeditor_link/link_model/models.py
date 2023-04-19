from django.core.exceptions import ObjectDoesNotExist

try:
    from builtins import str
except ImportError:
    from __builtin__ import str

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

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
        # generic foreign key link check
        fk_link = self._check_link_for_foreign_key()
        if fk_link:
            return fk_link
        # other custom link types
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
        if getattr(self, 'link_text', None):
            return self.link_text
        if getattr(self, 'name', None):
            return self.name
        if self.link_type:
            obj = self._check_foreign_key_value()
        if object is not None:
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

    def _check_foreign_key_value(self):
        """
        check if link type and it's value are a foreign key
        Returns: foreign key value, if available
        """
        try:
            value = getattr(self, self.get_link_type(), None)
            return value
        except ObjectDoesNotExist:
            pass
        return None

    def _check_link_for_foreign_key(self):
        value = self._check_foreign_key_value()
        # print(isinstance(value, models.Model))
        if value and getattr(value, 'get_absolute_url', None):
            link = value.get_absolute_url()
            return link
        return None


class Link(LinkBase):
    """
    if in installed apps, this will be created and available out of the box
    beware: no migrations yet!
    """
    pass


if CKEDITOR_LINK_USE_CMS_FILER:

    from cms.models.fields import PageField
    from filer.fields.file import FilerFileField

    class CMSFilerLinkBase(LinkBase):  # noqa
        cms_page = PageField(
            null=True,
            on_delete=models.SET_NULL,
            related_name="%(app_label)s_%(class)s_set",
            blank=True,
        )
        html_anchor = models.SlugField(
            default='',
            blank=True,
            verbose_name='Anker',
        )
        file = FilerFileField(
            null=True,
            on_delete=models.SET_NULL,
            related_name="%(app_label)s_%(class)s_set",
            blank=True,
        )

        def __init__(self, *args, **kwargs):
            if kwargs.get('page', None):
                self.cms_page = kwargs.get('page')
            super(CMSFilerLinkBase, self).__init__(*args, **kwargs)

        class Meta:
            abstract = True

        def get_link(self):
            # best practice is to call super first, so not relevant attrs are nulled
            super_link = super(CMSFilerLinkBase, self).get_link()
            fk_obj = self._check_foreign_key_value()
            if self.get_link_type() == 'cms_page' and super_link:
                if self.html_anchor:
                    super_link += '#%s' % self.html_anchor
                if getattr(self.cms_page, 'node', None):
                    # cms>=3.5
                    site = getattr(self.cms_page.node, 'site', None)
                else:
                    # cms<3.5
                    site = getattr(self.cms_page, 'site', None)
                if site.id == settings.SITE_ID:
                    return super_link
                else:
                    return '//' + site.domain + super_link
            elif self.get_link_type() == 'file' and fk_obj:
                return fk_obj.url
            return super_link

        def get_link_target(self):
            fk_obj = self._check_foreign_key_value()
            if self.get_link_type() == 'cms_page' and fk_obj:
                site = self._get_cms_page_site()
                if not site.id == settings.SITE_ID:
                    return "_blank"
            else:
                return super(CMSFilerLinkBase, self).get_link_target()
            return ""

        def _get_cms_page_site(self):
            fk_obj = self._check_foreign_key_value()
            if self.get_link_type() == 'cms_page' and fk_obj:
                if getattr(self.cms_page, 'node', None):
                    site = self.cms_page.node.site
                else:
                    site = self.cms_page.site
            return site
