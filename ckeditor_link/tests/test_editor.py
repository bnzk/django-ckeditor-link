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
        self.webdriver = CustomWebDriver()

    def tearDown(self):
        self.webdriver.quit()

    def test_app_index_get(self):
        # if this fails, everything is probably broken.
        self.login()
        self.open(reverse('admin:index'))
        self.webdriver.find_css(".app-test_app")

    def test_editor_has_button_dialog_opens_has_form(self):
        self.login()
        sleep(1)  # must be a better solution!
        self.open(reverse('admin:test_app_testmodel_change', args=[self.existing.id]))
        sleep(1)  # argh
        button = self.webdriver.wait_for_css(".cke_button__djangolink")
        button[0].click()
        dialog_title = self.webdriver.wait_for_css(".cke_dialog_title")
        sleep(1)  # argh
        iframe = self.webdriver.find_css(".cke_dialog_ui_html")
        self.webdriver.switch_to.frame(iframe)
        target = self.webdriver.wait_for_css("#id_target")

    def test_dialog_form_validation(self):
        self.login()
        sleep(1)  # must be a better solution!
        self.open(reverse('admin:test_app_testmodel_change', args=[self.existing.id]))
        sleep(1)  # argh
        button = self.webdriver.wait_for_css(".cke_button__djangolink")
        button[0].click()
        self.webdriver.wait_for_css(".cke_dialog_title")
        sleep(1)  # argh
        iframe = self.webdriver.find_css(".cke_dialog_ui_html")
        self.webdriver.switch_to.frame(iframe)
        email = self.webdriver.wait_for_css("#id_email")
        email.send_keys('what-foo')
        self.webdriver.switch_to.default_content()
        ok = self.webdriver.wait_for_css(".cke_dialog_ui_button_ok")
        ok.click()
        self.webdriver.switch_to.frame(iframe)
        self.webdriver.wait_for_css(".field-email .errorlist")
        email.send_keys('root@example.com')
        self.webdriver.switch_to.default_content()
        ok = self.webdriver.wait_for_css(".cke_dialog_ui_button_ok")
        ok.click()
        sleep(1)  # argh
        try:
            # check that dialog is gone or invisible
            title = self.webdriver.find_css(".cke_dialog_title")
            self.assertFalse(title.is_displayed())
        except NoSuchElementException:
            # ok if removed from the DOM!!
            pass

    def test_no_fake_null_as_string_values(self):
        self.login()
        sleep(1)  # must be a better solution!
        self.open(reverse('admin:test_app_testmodel_change', args=[self.existing.id]))
        sleep(1)  # argh
        button = self.webdriver.wait_for_css(".cke_button__djangolink")
        button[0].click()
        self.webdriver.wait_for_css(".cke_dialog_title")
        sleep(1)  # argh
        iframe = self.webdriver.find_css(".cke_dialog_ui_html")
        self.webdriver.switch_to.frame(iframe)
        self.webdriver.wait_for_css("#id_testmodel")  # just wait for it, then send with "null"
        self.webdriver.switch_to.default_content()
        ok = self.webdriver.wait_for_css(".cke_dialog_ui_button_ok")
        ok.click()
        sleep(1)  # argh
        # inserted at first position in html, so this should work.
        ckcontent_iframe = self.webdriver.find_css("#cke_id_richtext iframe")
        self.webdriver.switch_to.frame(ckcontent_iframe)
        link = self.webdriver.wait_for_css("body a[data-ckeditor-link=true]")
        self.assertEqual('', link.get_attribute('data-testmodel'))

    def test_two_editors_in_same_form(self):
        self.login()
        self.open(reverse('admin:test_app_testmodel_change', args=[self.existing.id]))

    def test_dialog_submit_and_link_attrs(self):
        self.login()
        self.open(reverse('admin:test_app_testmodel_change', args=[self.existing.id]))
