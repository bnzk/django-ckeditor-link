# -*- coding: utf-8 -*-
from django.test import Client
from django.test import TestCase

from ckeditor_link.tests.test_app.models import TestModel, LinkModel

# compat
import django
if django.VERSION[:2] < (1, 10):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse


class CKeditorLinkTemplateTagTests(TestCase):
    fixtures = ['test_app.json', ]

    def setUp(self):
        self.test_object = TestModel.objects.get(pk=2)
        self.test_object_not_existing_fk = TestModel.objects.get(pk=1)

    def tearDown(self):
        pass

    def test_tag_link_target_class_value(self):
        """
        does it transform everything as it should?
        """
        client = Client()
        url = reverse('testmodel_detail', args=[self.test_object.id])
        response = client.get(url)
        content = response.content
        # check it!

    def test_tag_no_destruction_of_existing_links(self):
        """
        normal existing <a href="xx" should not be tinkered with
        """
        pass

    def test_tag_robustness(self):
        """
        can it handle LinkModel with for example no get_css_class method?
        """
        client = Client()
        url = reverse('testmodel_detail', args=[self.test_object.id])
        response = client.get(url)
        content = response.content
        # check it!

    def test_not_existing_foreign_key_value(self):
        """
        can it handle no more existing foreign key values set in links?
        """
        client = Client()
        url = reverse('testmodel_detail', args=[self.test_object_not_existing_fk.id])
        response = client.get(url)
        # no exception, there we go!
        self.assertEqual(response.status_code, 200)

    def test_tag_attr_modifiers(self):
        """
        do attr modifiers work?
        has data-target="targetvalue", needs <a href="targetvalue--xy"
        """
        client = Client()
        url = reverse('testmodel_detail', args=[self.test_object.id])
        response = client.get(url)
        self.assertContains(response, 'href="targetvalue--xy"')