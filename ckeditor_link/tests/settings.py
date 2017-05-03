"""Settings that need to be set in order to run the tests."""
import os
import sys
import tempfile
import logging

from django.core.urlresolvers import reverse_lazy


DEBUG = True

logging.getLogger("factory").setLevel(logging.WARN)

# from selenium.webdriver.firefox import webdriver
from selenium.webdriver.phantomjs import webdriver
SELENIUM_WEBDRIVER = webdriver


CKEDITOR_LINK_MODEL = 'ckeditor_link.tests.test_app.models.LinkModel'
CKEDITOR_LINK_IFRAME_URL = reverse_lazy('admin:test_app_linkmodel_add')
CKEDITOR_LINK_VERIFY_URL = reverse_lazy('admin:test_app_linkmodel_verify')

CKEDITOR_CONFIGS = {
    'default': {
        'djangolinkIframeURL': CKEDITOR_LINK_IFRAME_URL,
        'djangolinkVerifyURL': CKEDITOR_LINK_VERIFY_URL,
        'djangolinkFallbackField': 'external_url',
        'linkShowAdvancedTab': False,
        'extraPlugins': ','.join(
            [
                # your extra plugins here
                'djangolink',
                'autolink',
                'autoembed',
                'embedsemantic',
                'autogrow',
                'devtools',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                'elementspath'
            ]),
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Underline'],
            ['DjangoLink', 'Unlink'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ]
    }
}

SITE_ID = 1

APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'ENGLISHS' ),
)

ROOT_URLCONF = 'ckeditor_link.tests.urls'

# media root is overridden when needed in tests
MEDIA_ROOT = tempfile.mkdtemp(suffix='ckeditor_media_root')
MEDIA_URL = "/media/"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(APP_ROOT, '../test_app_static')
STATICFILES_DIRS = (
    os.path.join(APP_ROOT, 'static'),
)

# TEMPLATE_DIRS = (
#     os.path.join(APP_ROOT, 'tests/test_app/templates'),
# )

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(
    os.path.join(APP_ROOT, 'tests/coverage'))
COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', 'urls$', 'locale$',
    'migrations', 'fixtures', 'admin$', 'django_extensions',
]

EXTERNAL_APPS = (
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'ckeditor',
    # 'djangocms_text_ckeditor',
    # 'cms',
    # 'treebeard',
    # 'menus',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # 'django.template.loaders.eggs.Loader',
            ],
        }
    },
]


INTERNAL_APPS = (
    'ckeditor_link',
    'ckeditor_link.tests.test_app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS
COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS

SECRET_KEY = 'foobarXXXxxsvXY'
