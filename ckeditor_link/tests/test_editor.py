# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from selenium.webdriver.support.expected_conditions import visibility_of
from selenium.webdriver.support.wait import WebDriverWait

from ckeditor_link.tests.utils.selenium_utils import SeleniumTestCase, CustomWebDriver
from ckeditor_link.tests.test_app.models import TestModel, LinkModel


class ckeditor_linkEditorTests(SeleniumTestCase):
    fixtures = ['test_app.json', ]
    username = 'admin'
    password = 'admin'

    def setUp(self):
        superuser = User.objects.create_superuser('admin', 'admin@free.fr', 'admin')
        self.existing = TestModel.objects.get(pk=1)
        # Instantiating the WebDriver will load your browser
        self.wd = CustomWebDriver()

    def tearDown(self):
        self.wd.quit()

    def test_app_index_get(self):
        # if this fails, everything is probably broken.
        self.login()
        self.open(reverse('admin:index'))
        self.wd.find_css(".app-test_app")

    def test_editor_has_button_dialog_opens_has_form(self):
        self.login()
        self.open(reverse('admin:test_app_testmodel_change', args=[self.existing.id]))
        button = self.wd.wait_for_css("a.cke_button__djangolink")
        button[0].click()
        dialog_title = self.wd.wait_for_css(".cke_dialog_title")
        # self.assertTrue(dialog_title.is_displayed())

    def test_dialog_form_validation(self):
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

    def test_dialog_submit_and_link_attrs(self):
        self.login()
        self.open(reverse('admin:test_app_testmodeladvanced_change', args=[self.advanced_empty.id]))
        inline = self.wd.find_css("#testinlinemodel_set-group")
        self.assertFalse(inline.is_displayed())
        f11 = self.wd.find_css("div.field-set1_1")
        self.assertFalse(f11.is_displayed())
        f31 = self.wd.find_css("div.field-set3_1")
        self.assertFalse(f31.is_displayed())

