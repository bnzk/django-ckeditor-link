django-ckeditor_link
*****************

.. image:: https://travis-ci.org/benzkji/django-ckeditor_link.svg
    :target: https://travis-ci.org/benzkji/django-ckeditor_link

a better link dialog for ckeditor in django modelforms.


Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-ckeditor_link

Add ``ckeditor_link`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'ckeditor_link',
    )

ckeditor_link does not need it's own database tables, so no need to migrate.


Usage
------------

Have a look at ``ckeditor_link/tests/test_app/settings_test.py`` for a complete example.

Following steps are needed.


1. Define a link model.

.. code-block:: python

    # your_app/models.py

    class LinkModel(models.Model):
        target = models.CharField(max_length=255, blank=True, default='', )
        external_url = models.CharField(max_length=255, blank=True, default='',)
        email = models.EmailField(blank=True, default='',)
        testmodel = models.ForeignKey(TestModel, null=True, default=None, blank=True)

        def __str__(self):
            return "LINK! %s" % self.target

        def get_link(self):
            # return link value, based on choosen fields.
            return "http://www.dynamic.com"


2. Register your model.

.. code-block:: python

    # your_app/admin.py
    ...
    from ckeditor_link.admin import DjangoLinkAdmin


    class LinkAdmin(DjangoLinkAdmin):
        form = LinkModelForm

    admin.site.register(LinkModel, LinkAdmin)


3. Configure your django-ckeditor (or whatever ck you use).

.. code-block:: python

    # config for django-ckeditor

    CKEDITOR_LINK_IFRAME_URL = '/admin/your_app/linkmodel/add/?_popup=true'
    CKEDITOR_LINK_VERIFY_URL = '/admin/your_app/linkmodel/verify/'

    CKEDITOR_CONFIGS = {
        'default': {
            'djangolinkIframeURL': CKEDITOR_LINK_IFRAME_URL,
            'djangolinkVerifyURL': CKEDITOR_LINK_VERIFY_URL,
            'extraPlugins': ','.join(
                [
                    # your extra plugins here
                    'djangolink',
                    ...
                ]),
            'toolbar': 'Custom',
            'toolbar_Custom': [
                ['Bold', 'Underline'],
                ['DjangoLink', 'Unlink'],
                ...
            ]
        }
    }


4. In your template, use the django-ckeditor-link templatetag.

.. code-block:: html

    not yet available



Contribute
------------

Fork and code. Either run `tox` for complete tests, or `python manage.py test --settings=ckeditor_link.tests.settings_test`
