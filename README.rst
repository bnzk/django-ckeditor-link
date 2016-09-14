django-ckeditor-link
*****************

.. image:: https://travis-ci.org/benzkji/django-ckeditor-link.svg
    :target: https://travis-ci.org/benzkji/django-ckeditor-link

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
having a teaser model. And a CKLink model, that has managed=False, so no database table is
created.

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

        class Meta:
            managed = False


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

    not yet available, do it yourself for now :/



Contribute
------------

Fork and code. Either run `tox` for complete tests, or `python manage.py test --settings=ckeditor_link.tests.settings_test`
