Technologies
============

Languages
---------

- **Python 3.11** : application code
- **HTML / CSS / JavaScript** : Django templates and static files (Bootstrap)
- **YAML** : CI/CD pipeline and Read the Docs configuration
- **reStructuredText** : this documentation

Application
-----------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Tool
     - Version
     - Purpose
   * - Django
     - 3.0
     - Web framework (models, views, templates, administration)
   * - SQLite
     - 3
     - Database (a single file : ``oc-lettings-site.sqlite3``)
   * - python-dotenv
     - 1.2.4
     - Reading the ``.env`` file
   * - sentry-sdk
     - 2.73.0
     - Sending errors and logs to Sentry
   * - Gunicorn
     - 23.0.0
     - Production web server
   * - WhiteNoise
     - 5.3.0
     - Serving static files in production (latest version compatible with Django 3.0)

Code quality
------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Tool
     - Version
     - Purpose
   * - flake8
     - 3.7.0
     - Linting (style and errors)
   * - pytest / pytest-django
     - 7.4.4 / 4.5.2
     - Unit and integration tests
   * - pytest-cov
     - 4.1.0
     - Test coverage measurement

External Services and Tools
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Service
     - Purpose
   * - GitHub Actions
     - CI/CD pipeline : testing, image building, deployment
   * - Docker / Docker Hub
     - Website containerization and image registry
   * - Render
     - Production website hosting
   * - Sentry
     - Error and log monitoring
   * - Sphinx / Read the Docs
     - Generation and publication of this documentation
