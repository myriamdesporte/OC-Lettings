Database and Models
====================

Database Engine
---------------

* **SQLite**, database file ``oc-lettings-site.sqlite3`` located at the project root
  (path defined in ``DATABASES`` in ``oc_lettings_site/settings.py``).
* The file is version-controlled: it contains demo data (6 lettings, 4 profiles, the ``admin`` user).
* The database structure is managed exclusively through Django migrations
  (``python manage.py migrate``), never directly through SQL.

Schema
------

.. code-block:: text

   lettings_address                lettings_letting
   ┌──────────────────┐            ┌──────────────────┐
   │ id (PK)          │◄───── 1:1 ─┤ address_id (FK)  │
   │ number           │            │ id (PK)          │
   │ street           │            │ title            │
   │ city             │            └──────────────────┘
   │ state            │
   │ zip_code         │
   │ country_iso_code │
   └──────────────────┘

   auth_user (Django)              profiles_profile
   ┌──────────────────┐            ┌──────────────────┐
   │ id (PK)          │◄───── 1:1 ─┤ user_id (FK)     │
   │ username         │            │ id (PK)          │
   │ ...              │            │ favorite_city    │
   └──────────────────┘            └──────────────────┘

Relationships are **one-to-one** (``OneToOneField``): each address belongs to a single letting,
and each user has a single profile. Deleting an address or a user also deletes the associated
letting or profile (``on_delete=CASCADE``).

``lettings`` application
------------------------

``Address`` model (``lettings_address`` table) : postal address of a rental property.

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Field
     - Type
     - Constraints
   * - ``number``
     - positive integer
     - Maximum 9999
   * - ``street``
     - text
     - Maximum 64 characters
   * - ``city``
     - text
     - Maximum 64 characters
   * - ``state``
     - text
     - Exactly 2 characters (e.g. ``CA``)
   * - ``zip_code``
     - positive integer
     - Maximum 99999
   * - ``country_iso_code``
     - text
     - Exactly 3 characters (e.g. ``USA``)

``Letting`` model (``lettings_letting`` table) : property available for rent.

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Field
     - Type
     - Constraints
   * - ``title``
     - text
     - Maximum 256 characters
   * - ``address``
     - one-to-one relationship with ``Address``
     - required, unique

``profiles`` application
------------------------

``Profile`` model (``profiles_profile`` table) : additional information associated with a user.

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Field
     - Type
     - Constraints
   * - ``user``
     - one-to-one relationship with ``User`` (Django)
     - required, unique
   * - ``favorite_city``
     - text
     - Maximum 64 characters, optional

User accounts (username, first name, last name, email, password) are managed
by the ``User``  model from ``django.contrib.auth``.

Exploring the Database
----------------------

.. code-block:: bash

   sqlite3 oc-lettings-site.sqlite3

.. code-block:: sql

   .tables
   pragma table_info(profiles_profile);
   select user_id, favorite_city from profiles_profile where favorite_city like 'B%';
   .quit
