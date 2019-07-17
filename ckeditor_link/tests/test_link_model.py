# -*- coding: utf-8 -*-
from cms.models import Page

from ckeditor_link.templatetags import ckeditor_link_tags

try:
    reload
except NameError:
    from importlib import reload

from ckeditor_link.tests.utils.selenium_utils import SeleniumTestCase
from cms import api
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from django.test import Client, override_settings

from ckeditor_link.tests.test_app.models import TestModel, LinkModel
from ckeditor_link import conf

# compat
import django
if django.VERSION[:2] < (1, 10):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse


class ContribLinkModelTests(SeleniumTestCase):
    fixtures = ['test_app_link_model.json', ]

    def setUp(self):
        self.test_object = TestModel.objects.get(pk=101)
        self.test_object_cms_page = TestModel.objects.get(pk=102)
        self.page1 = api.create_page(
            slug='page1',
            title="Page1",
            language='en',
            template=TEMPLATE_INHERITANCE_MAGIC,
            parent=None
        )
        self.page1.publish('en')
        self.page2 = api.create_page(
            title="Page2",
            language='en',
            template=TEMPLATE_INHERITANCE_MAGIC,
            parent=None,
            position='first-child',
        )
        self.page2.publish('en')
        # page2 has id=3!
        super(ContribLinkModelTests, self).setUp()

    def tearDown(self):
        self.webdriver.quit()

    def test_admin_loads(self):
        """
        loading link forms
        """
        self.login()
        self.open(reverse('admin:test_app_contriblinkmodel_add'))
        self.webdriver.wait_for_css("#id_external", )
        self.open(reverse('admin:test_app_cmsfilerlinkmodel_add'))
        self.webdriver.wait_for_css("#id_cms_page_0", )

    def test_admin_page_fallback(self):
        """
        older versions have "page" instead of cms_page as data- attributes
        """
        self.login()
        self.open('{}?page={}'.format(
            reverse('admin:test_app_cmsfilerlinkmodel_add'),
            self.page2.id
        ))
        all_options = self.webdriver.wait_for_css("#id_cms_page_1 option", )
        option = self.webdriver.wait_for_css("#id_cms_page_1 option[selected]", )
        self.assertEqual(option.get_attribute('value'), str(self.page2.id))

    @override_settings(
        CKEDITOR_LINK_MODEL='ckeditor_link.tests.test_app.models.CMSFilerLinkModel'
    )
    def test_cms_page_link_fallback(self):
        reload(conf)
        reload(ckeditor_link_tags)
        client = Client()
        url = reverse('testmodel_detail', args=[self.test_object_cms_page.id])
        self.test_object_cms_page.richtext = self.test_object_cms_page.richtext.replace(
            '<cms_page_id_page2>', str(self.page2.id)
        )
        self.test_object_cms_page.save()
        response = client.get(url)
        self.assertContains(response, 'href="/page2/"')