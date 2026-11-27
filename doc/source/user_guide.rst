User Guide
==========

This guide describes the main use cases of the website for visitors and administrators.

Visitor
-------

Browsing rental properties
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Open the homepage ``/``.
2. Click on **Lettings** : the list of all rental properties is displayed.
3. Click on a title : the ``/lettings/<id>/`` page displays the property's title and full address.

Browsing profiles
~~~~~~~~~~~~~~~~~

1. From the homepage, click on **Profiles**.
2. Click on a username : the ``/profiles/<username>/`` page displays the user's first name, last
   name, email address and favorite city.

Page Not Found
~~~~~~~~~~~~~~

An unknown address (e.g. ``/lettings/999/``) displays the website's 404 page, with a link to
return the homepage.

Administrator
-------------

Logging in
~~~~~~~~~~

1. Open ``/admin/``.
2. Log in with a *staff* account (loccaly : ``admin`` / ``Abc1234!``).

Adding a rental property
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Lettings > Addresses > Add address** : enter the address, then click **Save**.
2. **Lettings > Lettings > Add letting** : enter the title, select the address you
   created, then click on **Save**.
3. The rental property appears on ``/lettings/``.

An address can only be linked to one rental property.

Adding a profile
~~~~~~~~~~~~~~~~

1. **Authentication and Authorization > Users > Add user** : create
   the user (username, password), then fill in their first name, last name and email address.
2. **Profiles > Profiles > Add profile** : select the user, enter their favorite city,
   then click on **Save**.
3. The profile appears on ``/profiles/``.

Editing or deleting
~~~~~~~~~~~~~~~~~~~

Click on an object in the administration list, edit the fields then click **Save** or **Delete**.

.. warning::

   | Deleting an address also deletes the associated rental property.
   | Deleting a user also deletes their profile.

.. note::

   In production, the SQLite database is included in the Docker image:
   any changes made through the administration interface are **lost with each
   redeployment**. See :doc:`deployment`.
