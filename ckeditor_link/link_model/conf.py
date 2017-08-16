from django.utils.translation import ugettext_lazy as _
from django.conf import settings


CKEDITOR_LINK_USE_CMS_FILER = getattr(
    settings,
    'CKEDITOR_LINK_USE_CMS_FILER',
    False
)

CKEDITOR_LINK_STYLE_CHOICES = getattr(
    settings, 'CKEDITOR_LINK_STYLE_CHOICES', (
        ('', _("Default")),
        ('button', _("Button")),
    )
)

if CKEDITOR_LINK_USE_CMS_FILER:
    CKEDITOR_LINK_TYPE_CHOICES = getattr(
        settings, 'CKEDITOR_LINK_TYPE_CHOICES', (
            ('', _("None")),
            ('page', _("page")),
            ('file', _("File")),
            ('external', _("External URL")),
            ('mailto', _("E-Mail")),
            ('free', _("Free")),
        )
    )
else:
    CKEDITOR_LINK_TYPE_CHOICES = getattr(
        settings, 'CKEDITOR_LINK_TYPE_CHOICES', (
            ('', _("None")),
            ('external', _("External URL")),
            ('mailto', _("E-Mail")),
            ('free', _("Free")),
        )
    )
