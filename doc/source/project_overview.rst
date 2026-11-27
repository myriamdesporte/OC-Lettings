Project Overview
================

The Website
-----------

OC Lettings is the website of Orange County Lettings. It allows users to browse :

* the list of **rental properties** (*lettings*) and view details of each property (title, address);
* the liste of **user profiles** (*profiles*) and view details of each profile (email, favorite city).

An **administration interface** allows all data to be managed.

Live application
----------------

The application is deployed on Render and can be access directly from a web browser.

`Access the OC Lettings application <https://oc-lettings-tjyc.onrender.com>`_

Version 2.0
-----------

Version 2.0 modernizes the website without changing its appearance :

* **Modular architecture** : the code is divided into three Django applications :

    * ``oc_lettings_site``;
    * ``lettings``;
    * ``profiles``.

* **Code quality** : linting without error, custom 404 and 500 error pages, docstrings
  and tests (coverage above 80 %).
* **Monitoring** : logging and error tracking with Sentry.
* **CI/CD** : automated tests, Docker image published to Docker Hub, and deployment to
  Render whenever the ``master`` branch is updated.

Code Structure
--------------

.. code-block:: text

   OC-Lettings/
   ├── oc_lettings_site/            # Django Project : settings, root URLs, homepage
   ├── lettings/                    # Rental properties application (Address, Letting)
   ├── profiles/                    # User profiles application (Profile)
   ├── templates/                   # Shared templates (base, homepage (index), 404, 500)
   ├── static/                      # CSS, JavaScript, images
   ├── doc/                         # This documentation (Sphinx)
   ├── .github/workflows/           # CI/CD pipeline (GitHub Actions)
   ├── Dockerfile                   # Website Docker image
   ├── requirements.txt             # Python dependencies
   ├── setup.cfg                    # flake8 and pytest configuration
   ├── .coveragerc                  # Test coverage configuration
   ├── env.example                  # .env file template (environment variables)
   └── oc-lettings-site.sqlite3     # SQLite database

Each application contains its models (``models.py``), views (``views.py``),
URL configuration (``urls.py``), templates (``templates/<application>/``) and tests (``tests.py``).
