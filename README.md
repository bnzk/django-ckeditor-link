# django-ckeditor-link

[![Build Status](https://travis-ci.org/bnzk/django-ckeditor-link.svg "Build Status")](https://travis-ci.org/bnzk/django-ckeditor-link/)
[![PyPi Version](https://img.shields.io/pypi/v/django-ckeditor-link.svg "PyPi Version")](https://pypi.python.org/pypi/django-ckeditor-link/)
[![Licence](https://img.shields.io/pypi/l/django-ckeditor-link.svg "Licence")](https://pypi.python.org/pypi/django-ckeditor-link/)


link plugin for ckeditor, based on django modelforms/modeladmin, allowing direct linking to your models, or to whatever your want.


## Installation

To get the latest stable release from PyPi

    pip install django-ckeditor-link

Add `ckeditor_link` to your `INSTALLED_APPS`

    INSTALLED_APPS = (
        ...,
        'ckeditor_link',
    )

ckeditor_link does not need it's own database tables, so no need to migrate.

If you want an out of the box solution for linking, you can add `ckeditor_link.link_model` to your
`INSTALLED_APPS`. Warning, EXPERIMENTAL feature.


## Usage

Have a look at `ckeditor_link/tests/test_app/settings_test.py` for a complete example.

Following steps are needed.

1. Define a link model. Proposed way: Create an abstract base model, that you can extend from for example when
having a teaser model. And a CKLink model, whose purpose is only to provide a modelform and validation. No data is
ever written to that table, if used with DjangoLinkAdmin.

    ```python
    # your_app/models.py

    @python_2_unicode_compatible
    class LinkModelBase(models.Model):
        target = models.CharField(max_length=255, blank=True, default='', )
        external_url = models.CharField(max_length=255, blank=True, default='',)
        email = models.EmailField(blank=True, default='',)
        testmodel = models.ForeignKey(TestModel, null=True, default=None, blank=True)

        class Meta:
            abstract = True

        def __str__(self):
            # do it better
            return "LINK! %s" % self.target

        def get_link(self):
            # return link value, based on fields.
            return "http://www.dynamic.com"


    class LinkModel(LinkModelBase):
        pass


    class Teaser(LinkModelBase):
        image = models.ImageField()
        title = models.CharField()
        text = models.TextField()
    ```

    For your convinience, we provide a basic abstract link model, and a django-cms / django-filer compatible version, under
    `ckeditor_link.link_model.models`. They are named `LinkBase` and `CMSFilerLinkBase`, and thought to inherit from. To use them, you would need
    to add `ckeditor_link.link_model` to `INSTALLED_APPS` in your settings. To use the cms / filer version, you'll need to set `CKEDITOR_LINK_USE_CMS_FILER` to True in your settings.
    You can provide your own LINK_TYPE_CHOICES, if you add some more fields, with `settings.CKEDITOR_LINK_TYPE_CHOICES`.


2. Register your model with DjangoLinkAdmin.

    ```python
    # your_app/admin.py
    ...
    from ckeditor_link.admin import DjangoLinkAdmin

    class LinkModelAdmin(DjangoLinkAdmin):
        pass

    admin.site.register(LinkModel, LinkModelAdmin)
    ```


3. Configure your django-ckeditor (or whatever ck you use).

    ```python
    # config for django-ckeditor

    CKEDITOR_LINK_MODEL = 'my_app.models.LinkModel'
    CKEDITOR_LINK_IFRAME_URL = reverse_lazy('admin:my_app_linkmodel_add')
    CKEDITOR_LINK_VERIFY_URL = reverse_lazy('admin:my_app_linkmodel_verify')

    CKEDITOR_CONFIGS = {
        'default': {
            'djangolinkIframeURL': CKEDITOR_LINK_IFRAME_URL,
            'djangolinkVerifyURL': CKEDITOR_LINK_VERIFY_URL,
            'djangolinkFallbackField': 'external',
            'extraPlugins': ','.join(
                [
                    # your extra plugins here
                    'djangolink',

                ]),
            'toolbar': 'Custom',
            'toolbar_Custom': [
                ['Bold', 'Underline'],
                ['DjangoLink', 'Unlink'],

            ]
        }
    }
    ```

    If you have existing content with normal `<a href="">` style links, you can migrate them into ckeditor-link mode:
    In the ckeditor configs, specify your model field as `djangolinkFallbackField` (see above), existing href values will
    show up in that field (and stay there).


4. In your template, use the django-ckeditor-link templatetag. This adds `lxml` and `cssselect` as dependencies - you
must install those yourself.

    ```django
    {% load ckeditor_link_tags %}
    {% object.html_field|ckeditor_link_add_link %}
    ```

## Contribute

Fork and code. Quickstart:

```shell
    pip install -r test_requirements.txt
    ./manage.py migrate  # create local sqlite db
    ./manage.py createsuperuser  # you want that
    ./manage.py loaddata test_app  # same data that is used for running tests
    ./manage.py runserver  # goto localhost:8000/admin/ or localhost:8000/testmodel/2/
```

### Testing

Either run `tox` for complete tests, or `python manage.py test
