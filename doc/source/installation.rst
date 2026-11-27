Installation
============

Prerequisites
-------------

* Git
* **Python 3.11** (Django 3.0 is not compatible with Python 3.12 and later)
* SQLite3 (optional, for exploring the database)
* Docker (optional, for running the website image)

Clone the repository
--------------------

.. code-block:: bash

   cd /path/to/my/projects
   git clone <https://github.com/myriamdesporte/OC-Lettings>
   cd OC-Lettings

Create the virtual environment
------------------------------

macOS / Linux :

.. code-block:: bash

   python3.11 -m venv venv
   source venv/bin/activate

Windows (PowerShell) :

.. code-block:: powershell

   py -3.11 -m venv venv
   .\venv\Scripts\Activate.ps1

To exit the virtual environment : ``deactivate``.

Install dependencies
---------------------

.. code-block:: bash

   pip install -r requirements.txt

Configure environment variables
-------------------------------

| Sensitive data (secret key, Sentry DSN) is never stored in the source code.
| It is read from a ``.env`` file at the project root, which is ignored by git.

.. code-block:: bash

   cp env.example .env

| The ``env.example`` file already contains ``DJANGO_DEBUG=True``, which is suitable for local development.
| The variables are described in :doc:`deployment`.

.. warning::

    Without ``DJANGO_DEBUG=True`` or ``DJANGO_SECRET_KEY``, the website refuses to start (``ImproperlyConfigured`` error).
    This is intentional, to prevent production from ever running with a known secret key.
