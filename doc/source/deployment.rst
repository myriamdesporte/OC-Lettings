Deployment and Management
=========================

Overview
---------

Deployment is automated through a GitHub Actions pipeline (``.github/workflows/ci-cd.yml``),
triggered on every ``git push``:

.. code-block:: text

   push ──► 1. Linting and tests ──► 2. Docker image ──► 3. Render deployment
            (all branches)           (master only)       (master only)


1. **Linting and tests** : Python 3.11, ``flake8``, then ``pytest --cov``
   (fails if coverage is below 80 %).
2. **Containerization** (if job 1 succeeds) : build the image using the ``Dockerfile`` and push it
   to Docker Hub with two tags: the commit hash and ``latest``.
3. **Deployment** (if job 2 succeeds) : call the Render *deploy hook*, which deploys the image
   corresponding to the commit.

On other branches, only job 1 is executed.

Within the image, the website is served by **Gunicorn**; static files
(CSS, images, administration interface) are collected using ``collectstatic``
during image building and served by **WhiteNoise**.

Environment Variables
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - Variable
     - Purpose
     - Default
   * - ``DJANGO_DEBUG``
     - Debug mode (``True`` locally only)
     - ``False``
   * - ``DJANGO_SECRET_KEY``
     - Secret key, required if ``DJANGO_DEBUG`` is set to ``False``
     - (empty)
   * - ``DJANGO_ALLOWED_HOSTS``
     - Allowed domain names, separated by commas
     - ``localhost,127.0.0.1``
   * - ``SENTRY_DSN``
     - Sentry project key (empty: Sentry disabled)
     - (empty)
   * - ``SENTRY_ENVIRONMENT``
     - Environment displayed in Sentry
     - ``development``
   * - ``SENTRY_TRACES_SAMPLE_RATE``
     - Proportion of requests tracked for performance monitoring (0 to 1)
     - ``0``
   * - ``LOG_LEVEL``
     - Log level for the project applications
     - ``INFO``

Generate a secret key :

.. code-block:: bash

   python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"

Required Configuration
----------------------

- **Docker Hub**, **Render** and **Sentry** accounts.
- **GitHub Secrets** (*Settings > Secrets and variables > Actions*) :

  .. list-table::
     :header-rows: 1
     :widths: 35 65

     * - Secret
       - Content
     * - ``DOCKERHUB_USERNAME``
       - Docker Hub username
     * - ``DOCKERHUB_TOKEN``
       - Docker Hub *access token*  (*Read & Write* permissions)
     * - ``RENDER_DEPLOY_HOOK_URL``
       - Render service *deploy hook* URL

- **Render service variables** (*Environment* tab) :
  ``DJANGO_SECRET_KEY``, ``DJANGO_DEBUG=False``, ``SENTRY_DSN``,
  ``SENTRY_ENVIRONMENT=production``. ``DJANGO_ALLOWED_HOSTS`` is not required :
  the Render domain (``RENDER_EXTERNAL_HOSTNAME``) is added automatically.

Initial Setup
-------------

1. Add the ``DOCKERHUB_USERNAME`` and ``DOCKERHUB_TOKEN`` secrets to GitHub.
2. Push to ``master`` : the ``<utilisateur>/oc-lettings`` image is created on
   Docker Hub (the deployment job fails until the *deploy hook* exists, which is expected).
3. On Render : **New > Web Service > Existing image**,
   ``docker.io/<utilisateur>/oc-lettings:latest`` image, then configure the environment variables.
4. In the Render service **Settings** : copy the **Deploy Hook** into the GitHub
   ``RENDER_DEPLOY_HOOK_URL`` secret and disable **Auto-Deploy**
   (only the pipeline handles deployments).

Deploying an Update
-------------------

1. Work on a branch and push : the test job checks the code.
2. Merge into ``master`` and push.
3. Monitor the pipeline in GitHub's **Actions** tab, then the deployment in the
   Render service's **Events** tab.
4. Check the live website (pages, CSS, administration interface).

Application Management
----------------------

Rolling back to a previous version
    In Render, open the **Events** tab and click **Rollback** on a previous deployment.
    Each image is also available on Docker Hub under its commit hash.

Running a version locally
    .. code-block:: bash

        docker run --rm -p 8000:8000 -e DJANGO_SECRET_KEY=change-me <utilisateur>/oc-lettings:<hash-ou-latest>

   Add ``-e SENTRY_DSN=<dsn>`` to enable Sentry.

Monitoring errors
    | Exceptions and ``ERROR`` logs create an *issue* in **Sentry**;
    | ``INFO`` logs and above are visible in Sentry's **Logs** tab.
    | Logs are also displayed in the Render console (**Logs** tab).

Verifying Sentry
    Locally, with ``DJANGO_DEBUG=True``, open ``/sentry-debug/``:
    a ``ZeroDivisionError`` should appear in Sentry.

Updating this documentation
    Modify the ``doc/source/*.rst`` files and push : Read the Docs
    automatically rebuilds the documentation (configuration in ``.readthedocs.yaml``).

Known Limitations
-----------------

* **SQLite in the image** : data modified in production (through the administration interface)
  is lost with every redeployment. For actual production use, switch to an external database
  (PostgreSQL, for example).
* **Render free tier** : the service spins down after 15 minutes without a visit;
  the first subsequent request takes approximately one minute.
