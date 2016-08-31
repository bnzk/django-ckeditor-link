# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from ckeditor_link.tests.utils.django_utils import create_superuser
from ckeditor_link.tests.utils.selenium_utils import SeleniumTestCase, CustomWebDriver
from ckeditor_link.tests.test_app.models import TestModelSingle, TestModelAdvanced


class ckeditor_linkDialogTests(SeleniumTestCase):
    def setUp(self):
        self.single_empty = TestModelSingle()
        self.single_empty.save()
        self.single = TestModelSingle(**{'selection': 'octopus', })
        self.single.save()
        self.advanced_empty = TestModelAdvanced()
        self.advanced_empty.save()
        self.advanced = TestModelAdvanced(**{'set': 'set1', })
        self.advanced.save()
        self.superuser = create_superuser()
        # Instantiating the WebDriver will load your browser
        self.wd = CustomWebDriver()

    def tearDown(self):
        self.wd.quit()

    def test_tag_link_target_class_value(self):
        self.login()
        self.open(reverse('admin:test_app_testmodelsingle_change', args=[self.single_empty.id]))
        horse = self.wd.find_css("div.field-horse")
        self.assertFalse(horse.is_displayed())
        bear = self.wd.find_css("div.field-bear")
        self.assertFalse(bear.is_displayed())
        octo = self.wd.find_css("div.field-octopus")
        self.assertFalse(octo.is_displayed())

    def test_tag_no_destruction_of_existing_links(self):
        self.login()
        self.open(reverse('admin:test_app_testmodelsingle_change', args=[self.single.id]))
        horse = self.wd.find_css("div.field-horse")
        self.assertFalse(horse.is_displayed())
        bear = self.wd.find_css("div.field-bear")
        self.assertFalse(bear.is_displayed())
        octo = self.wd.find_css("div.field-octopus")
        self.assertTrue(octo.is_displayed())
        # change select value
        self.wd.find_css("div.field-selection select > option[value=horse]").click()
        horse = self.wd.find_css("div.field-horse")
        self.assertTrue(horse.is_displayed())
        octo = self.wd.find_css("div.field-octopus")
        self.assertFalse(octo.is_displayed())
