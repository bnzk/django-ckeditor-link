from django.conf import settings


CKEDITOR_LINK_MODEL = getattr(
    settings,
    'CKEDITOR_LINK_MODEL',
    None
)


# a default, working with the provided contrib link_model
CKEDITOR_LINK_ATTR_MODIFIERS = getattr(
    settings,
    'CKEDITOR_LINK_ATTR_MODIFIERS', {
        'cms_page': '{cms_page_2}'
    }
)
