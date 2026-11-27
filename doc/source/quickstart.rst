Quickstart
===========

Once the :doc:`installation <installation>` is complete, all commands should be run from
the project root directory, with the virtual environment activated.

Running the website
-------------------

.. code-block:: bash

   python manage.py runserver

* Website : http://localhost:8000
* Admin panel : http://localhost:8000/admin (username ``admin``,
  password ``Abc1234!``)

The provided SQLite database already contains rental listings and user profiles.

Checking code quality
---------------------

.. list-table::
   :header-rows: 1

   * - Command
     - Purpose
   * - ``flake8``
     - Linting (rules defined in ``setup.cfg``), should report 0 error
   * - ``pytest``
     - Runs all tests
   * - ``pytest --cov``
     - Runs tests and measures coverage, fails if coverage is below 80 %
   * - ``pytest --cov --cov-report=html``
     - Generates a detailed report in ``htmlcov/index.html``

Running the website with Docker
-------------------------------

With Docker as the only prerequisite, a single command pulls the image from Docker Hub
and starts the website at http://localhost:8000 :

.. code-block:: bash

   docker run --rm -p 8000:8000 -e DJANGO_SECRET_KEY=change-me myadsp/oc-lettings:latest

For machines using an ARM architecture (such as some Macs equipped with Apple Silicon),
you can force Docker to use the image compatible with the linux/amd64 architecture :

.. code-block:: bash

    docker run --rm --platform linux/amd64 -p 8000:8000 -e DJANGO_SECRET_KEY=change-me myadsp/oc-lettings:latest

Building this documentation
---------------------------

.. code-block:: bash

   pip install --requirement doc/requirements.txt
   cd doc
   make html

Then open ``doc/build/html/index.html`` in a web browser.
