# -*- coding: utf-8 -*-
from time import sleep

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.expected_conditions import visibility_of
from selenium.webdriver.support.wait import WebDriverWait

from ckeditor_link.tests.utils.selenium_utils import SeleniumTestCase, CustomWebDriver
from ckeditor_link.tests.test_app.models import TestModel, LinkModel


class ckeditor_linkEditorTests(SeleniumTestCase):
    fixtures = ['test_app.json', ]
    username = 'admin'
    password = 'admin'

    def setUp(self):
        superuser = User.objects.create_superuser(self.username, 'admin@free.fr', self.password)
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
        sleep(1)  # must be a better solution!
        self.open(reverse('admin:test_app_testmodel_change', args=[self.existing.id]))
        sleep(1)  # argh
        button = self.wd.wait_for_css(".cke_button__djangolink")
        button[0].click()
        dialog_title = self.wd.wait_for_css(".cke_dialog_title")
        sleep(1)  # argh
        iframe = self.wd.find_css(".cke_dialog_ui_html")
        self.wd.switch_to.frame(iframe)
        target = self.wd.wait_for_css("#id_target")

    def test_dialog_form_validation(self):
        self.login()
        sleep(1)  # must be a better solution!
        self.open(reverse('admin:test_app_testmodel_change', args=[self.existing.id]))
        sleep(1)  # argh
        button = self.wd.wait_for_css(".cke_button__djangolink")
        button[0].click()
        self.wd.wait_for_css(".cke_dialog_title")
        sleep(1)  # argh
        iframe = self.wd.find_css(".cke_dialog_ui_html")
        self.wd.switch_to.frame(iframe)
        email = self.wd.wait_for_css("#id_email")
        email.send_keys('what-foo')
        self.wd.switch_to.default_content()
        ok = self.wd.wait_for_css(".cke_dialog_ui_button_ok")
        ok.click()
        self.wd.switch_to.frame(iframe)
        self.wd.wait_for_css(".field-email .errorlist")
        email.send_keys('root@example.com')
        self.wd.switch_to.default_content()
        ok = self.wd.wait_for_css(".cke_dialog_ui_button_ok")
        ok.click()
        sleep(1)  # argh
        try:
            title = self.wd.find_css(".cke_dialog_title")
            self.assertFalse(title.is_displayed())
        except NoSuchElementException:
            # ok if removed from the DOM!!
            pass

    def test_dialog_submit_and_link_attrs(self):
        self.login()
        self.open(reverse('admin:test_app_testmodel_change', args=[self.existing.id]))

    def test_remove_foreign_key_attrs(self):
        self.login()
        self.open(reverse('admin:test_app_testmodel_change', args=[self.existing.id]))