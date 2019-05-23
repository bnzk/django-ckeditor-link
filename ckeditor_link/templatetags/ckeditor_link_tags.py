import importlib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist

from ckeditor_link import conf
from django import template
from django.template.defaultfilters import stringfilter


try:
    module_name, class_name = conf.CKEDITOR_LINK_MODEL.rsplit(".", 1)
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
        # TODO: use some log thing, or rais ImproperlyConfigured!
        if settings.DEBUG:
            msg = "Warning: CKEDITOR_LINK_MODEL (%s) could not be imported!?" % (conf.CKEDITOR_LINK_MODEL, )
            raise ImproperlyConfigured(msg)
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
                    # DEPRECATED: use CKEDITOR_LINK_ATTR_MODIFIERS setting!
                    if new_key == 'page_2':
                        new_key = 'cms_page'  # backward compat, for 0.2.0
                    if new_key == 'cms_page_2':
                        new_key = 'cms_page'
                    # until here
                    if hasattr(dummy_link, new_key):
                        if hasattr(dummy_link, new_key + "_id"):
                            # set fk directly
                            new_key = new_key + "_id"
                            if not value:
                                value = None
                        kwargs[new_key] = value
                        link.attrib.pop(key)
            for key, formatted_string in conf.CKEDITOR_LINK_ATTR_MODIFIERS.items():
                try:
                    kwargs[key] = formatted_string.format(**kwargs)
                except KeyError:
                    # this is an option, we dont know at all how our link is/was built (ages ago)
                    pass
            try:
                # this can go wrong with fk and the like
                real_link = ckeditor_link_class(**kwargs)
                link.set('href', real_link.get_link())
                if getattr(real_link, 'get_link_target', None):
                    link.set('target', real_link.get_link_target())
                if getattr(real_link, 'get_link_style', None):
                    link.set('class', real_link.get_link_style())
            except (ValueError, ObjectDoesNotExist) as e:
            # except (ValueError) as e:
                continue
    # arf: http://makble.com/python-why-lxml-etree-tostring-method-returns-bytes
    # beautifulsoup to the rescue!
    return tostring(fragment, encoding='unicode')
