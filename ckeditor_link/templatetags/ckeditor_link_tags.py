import importlib

from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter


try:
    module_name, class_name = settings.CKEDITOR_LINK_MODEL.rsplit(".", 1)
    my_module = importlib.import_module(module_name)
    ckeditor_link_class = getattr(my_module, class_name, None)
except ImportError:
    ckeditor_link_class = None


register = template.Library()


@register.filter
@stringfilter
def ckeditor_link_add_links(html):
    # lxml is not a dependency, but needed for this tag.
    from lxml.html import fragment_fromstring, tostring
    if not ckeditor_link_class:
        # TODO: use some log thing
        if settings.DEBUG:
            print("Warning: CKEDITOR_LINK_MODEL (%s) could not be imported!?" % (settings.CKEDITOR_LINK_MODEL, ))
        return html
    fragment = fragment_fromstring("<div>" + html + "</div>")
    links = fragment.cssselect('a')
    for link in links:
        if link.get('data-ckeditor-link', None):
            link.attrib.pop('data-ckeditor-link')
            kwargs = {}
            dummy_link = ckeditor_link_class()
            for key, value in link.items():
                if key.startswith('data-'):
                    new_key = key.replace('data-', '', 1)
                    # will be removed!
                    if new_key == 'page_2':
                        new_key = 'page'
                    # until here
                    if hasattr(dummy_link, new_key):
                        if hasattr(dummy_link, new_key + "_id"):
                            # set fk directly
                            new_key = new_key + "_id"
                            if not value:
                                value = None
                        kwargs[new_key] = value
                        link.attrib.pop(key)
            try:
                # this can go wrong with fk and the like
                real_link = ckeditor_link_class(**kwargs)
                link.set('href', real_link.get_link())
                if (getattr(real_link, 'get_target')):
                    link.set('target', real_link.get_target())
                if (getattr(real_link, 'get_css_class')):
                    link.set('class', real_link.get_css_class())
            except ValueError:
                continue
    return tostring(fragment)
