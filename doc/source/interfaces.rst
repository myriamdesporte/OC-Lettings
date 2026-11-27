Programming interfaces
=======================

The website does not expose a JSON API: its interfaces consist of **HTML pages**
(Django URLs and views) and the **administration interface**.

Routes
------

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - URL
     - Name (``{% url %}``)
     - View
     - Template
   * - ``/``
     - ``index``
     - ``oc_lettings_site.views.index``
     - ``index.html``
   * - ``/lettings/``
     - ``lettings:index``
     - ``lettings.views.index``
     - ``lettings/index.html``
   * - ``/lettings/<letting_id>/``
     - ``lettings:letting``
     - ``lettings.views.letting``
     - ``lettings/letting.html``
   * - ``/profiles/``
     - ``profiles:index``
     - ``profiles.views.index``
     - ``profiles/index.html``
   * - ``/profiles/<username>/``
     - ``profiles:profile``
     - ``profiles.views.profile``
     - ``profiles/profile.html``
   * - ``/admin/``
     - ``admin:index``
     - Django administration
     - –
   * - ``/sentry-debug/``
     - ``sentry_debug``
     - ``oc_lettings_site.views.sentry_debug``
     - (only if ``DEBUG`` is enabled)

* All routes respond to the ``GET`` method.
* ``lettings`` and ``profiles`` have their own namespaces (``app_name``) :
  in a template, use ``{% url 'lettings:letting' letting_id=1 %}``.
* Each application's URLs are defined in its ``urls.py`` and included through
  ``oc_lettings_site/urls.py`` (``ROOT_URLCONF``).

Response Codes
---------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Description
   * - 200
     - Page successfully displayed
   * - 404
     - Unknown letting or profile, or non-existent URL: ``404.html`` template
       (a ``WARNING`` log entry is generated)
   * - 500
     - Unexpected error: ``500.html`` template (the error is sent to Sentry if configured)

Custom 404 and 500 pages are only displayed when ``DEBUG`` is disabled; in debug mode,
Django displays its detailed error page.

Administration Interface
------------------------

The ``Address``, ``Letting`` and ``Profile`` models are registered in the administration interface
(``admin.py`` files), alongside Django users and groups.
It allows all data to be created, updated and deleted.

Code Reference
--------------

Automatically generated from docstrings.

Website Views
~~~~~~~~~~~~~~

.. automodule:: oc_lettings_site.views
   :members:

.. automodule:: lettings.views
   :members:

.. automodule:: profiles.views
   :members:

Models
~~~~~~~

.. automodule:: lettings.models
   :members: Address, Letting

.. automodule:: profiles.models
   :members: Profile

Configuration
~~~~~~~~~~~~~

.. autofunction:: oc_lettings_site.settings.env_bool

.. autofunction:: oc_lettings_site.settings.env_list
