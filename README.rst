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

Have a look at ``ckeditor_link/tests/test_app/admin.py`` for some examples.

.. code-block:: python

    NOPE
    from ckeditor_link.admin import assaavdsvad

    class TestModel(models.Model):
        file = FolderlessFileField(blank=True, null=True)


Contribute
------------

Fork and code. Either run `tox` for complete tests, or `python manage.py test --settings=ckeditor_link.tests.settings_test`
