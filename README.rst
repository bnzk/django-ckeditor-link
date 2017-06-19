django-ckeditor-link
*****************

.. image:: https://travis-ci.org/bnzk/django-ckeditor-link.svg
    :target: https://travis-ci.org/bnzk/django-ckeditor-link
.. image:: https://img.shields.io/pypi/v/django-ckeditor-link.svg
    :target: https://pypi.python.org/pypi/django-ckeditor-link/
.. image:: https://img.shields.io/pypi/l/django-ckeditor-link.svg
    :target: https://pypi.python.org/pypi/django-ckeditor-link/

link plugin for ckeditor, based on django modelforms/modeladmin, allowing direct linking to your models, or to whatever your want.


Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-ckeditor-link

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


1. Define a link model. Proposed way: Create a base model, that you can extend from for example when
having a teaser model. And a CKLink model, whose purpose is only to provide a modelform and validation. No data is
ever written to that table, if used with DjangoLinkAdmin.

.. code-block:: python

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


    class CKLinkModel(LinkModelBase):
        pass


2. Register your model with DjangoLinkAdmin.

.. code-block:: python

    # your_app/admin.py
    ...
    from ckeditor_link.admin import DjangoLinkAdmin

    class CKModelLinkAdmin(DjangoLinkAdmin):
        pass

    admin.site.register(CKLinkModel, CKModelLinkAdmin)


3. Configure your django-ckeditor (or whatever ck you use).

.. code-block:: python

    # config for django-ckeditor

    CKEDITOR_LINK_MODEL = 'ckeditor_link.tests.test_app.models.LinkModel'
    CKEDITOR_LINK_IFRAME_URL = reverse_lazy('admin:test_app_linkmodel_add')
    CKEDITOR_LINK_VERIFY_URL = reverse_lazy('admin:test_app_linkmodel_verify')

    CKEDITOR_CONFIGS = {
        'default': {
            'djangolinkIframeURL': CKEDITOR_LINK_IFRAME_URL,
            'djangolinkVerifyURL': CKEDITOR_LINK_VERIFY_URL,
            'djangolinkFallbackField': 'external,
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

If you have existing content with normal <a href=""> style links, you can migrate them into ckeditor-link mode:
In the ckeditor configs, specify your model field as `djangolinkFallbackField` (see above), existing href values will
show up in that field (and stay there).


4. In your template, use the django-ckeditor-link templatetag.

.. code-block:: html

    available, undocumented. at your own risk (needs lxml)


Contribute
------------

Fork and code. Quickstart:

.. code-block:: bash

    pip install -r test_requirements.txt
    ./manage.py migrate  # create local sqlite db
    ./manage.py createsuperuser  # you want that
    ./manage.py loaddata test_app  # same data that is used for running tests
    ./manage.py runserver  # goto localhost:8000/admin/ or localhost:8000/testmodel/2/


Testing
#######

Either run `tox` for complete tests, or `python manage.py test
