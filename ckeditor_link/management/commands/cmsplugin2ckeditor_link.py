# coding: utf-8
from __future__ import unicode_literals
import re

from cms.models import CMSPlugin
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    dont use this yet, it assumes too many things of your existing installation.
    rather use it as starting point, and copy and paste it.
    """
    help = 'Check for djangocms-text-ckeditor subplugins, convert to django-ckeditor-link style'  # noqa

    def add_arguments(self, parser):
        parser.add_argument(
            'plugins',
            nargs='+',
            help='Plugins to check',
        )
        parser.add_argument(
            '--field',
            required=True,
            help='Field to check',
        )

    def handle(self, *args, **options):

        text_plugins = CMSPlugin.objects.filter(
            plugin_type__in=options['plugins']
        )
        for plugin in text_plugins:
            instance, plugin_class = plugin.get_plugin_instance()
            img_pattern = re.compile(r'<img.*?>')
            obj_pattern = re.compile(r'plugin_obj_[0-9]*')
            image_tags = re.findall(img_pattern, instance.body)
            if len(image_tags):
                for tag in image_tags:
                    obj_match = re.findall(obj_pattern, tag)
                    if len(obj_match):
                        plugin_id = obj_match[0].replace('plugin_obj_', '')
                        # print plugin_id
                        link_plugin = CMSPlugin.objects.get(pk=plugin_id)
                        # print link_plugin
                        link_instance, link_class = link_plugin.get_plugin_instance()
                        link_data = {
                            'link_text': link_instance.get_link_text(),
                            'link': link_instance.get_link(),
                            'link_type': link_instance.get_link_type(),
                            'page': link_instance.page_id,
                            'file': link_instance.file_id,
                            'external': link_instance.external_url,
                            'mailto': link_instance.mailto,
                            'phone': link_instance.phone,
                        }
                        for key, value in link_data.iteritems():
                            if not value:
                                link_data[key] = ''
                        new_link = '<a href="{link}"' \
                                   ' data-ckeditor-link="true"' \
                                   ' data-link_type="{link_type}"' \
                                   ' data-page="{page}"' \
                                   ' data-file="{file}"' \
                                   ' data-external="{external_url}"' \
                                   ' data-mailto="{mailto}"' \
                                   ' data-phone="{mailto}"' \
                                   '>' \
                                   '{link_text}</a>'.format(**link_data)
                        instance.body = instance.body.replace(tag, new_link)
                instance.save()
