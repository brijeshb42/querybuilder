.. contents:: JSON Querybuilder
   :depth: 2

JSON query specification and implementation for Python APIs.
JSON querybuilder helps APIs to support JSON queries.


JSON Query Specification
=========================

Quick example
--------------

All players with ``jersey_no`` equal to ``1`` (``jersey_no == 1``):

.. code:: json

    {
        "EQ": 
              { "jersey_no": 1 }
    }


Operators
--------------

+----------------------------+------------+----------+------------------------------+
| Condition                  | JSON KEY   | Symbol   | JSON Query                   |
+============================+============+==========+==============================+
| Equal to                   | EQ         | ==       | ``{"EQ": {"jersey_no": 2}}`` |
+----------------------------+------------+----------+------------------------------+
| Less than                  | LT         | <        | ``{"LT": {"jersey_no": 2}}`` |
+----------------------------+------------+----------+------------------------------+
| Less than or Equal to      | LE         | <=       | ``{"LE": {"jersey_no": 2}}`` |
+----------------------------+------------+----------+------------------------------+
| Greater than               | GT         | >        | ``{"GT": {"jersey_no": 2}}`` |
+----------------------------+------------+----------+------------------------------+
| Greater than or Equal to   | GE         | >=       | ``{"GE": {"jersey_no": 2}}`` |
+----------------------------+------------+----------+------------------------------+
| Not equal                  | NE         | !=       | ``{"NE": {"jersey_no": 2}}`` |
+----------------------------+------------+----------+------------------------------+

IN
~~

All players where ``jersey_no`` is in ``[1, 2, 3]``:

.. code:: json

    {
       "IN": {
          "quanity": [1, 2, 3]
       }
    }

BETWEEN
~~~~~~~

All items with ``quantity`` between 10000 and 15000

.. code:: json

    {
       "BETWEEN": {
          "quanity": [10000, 15000]
       }
    }

CONTAINS_ANY
~~~~~~~~~~~~~

For all items where ``author_ids`` contains any of ``8, 9, 10``

.. code:: json

    {
       "CONTAINS_ANY": {
          "author_ids": [8, 9, 10]
       }
    }

CONTAINS_ALL
~~~~~~~~~~~~~

For all items where ``author_ids`` contains all of ``8, 9``

.. code:: json

    {
       "CONTAINS_ALL": {
          "author_ids": [8, 9]
       }
    }

STARTSWITH
~~~~~~~~~~~~~

-  For all items where ``title`` starts with ``Film Review``:

   .. code:: json

       {
          "STARTSWITH": {
         "title": "Film Review"
          }
       }


Grouping
--------

Complex queries can be composed using ``OR``, ``AND``   or both.

Example

For all items with ``quanity`` between 10000 and 15000 and whose
``author_ids`` contains ``8``\ (the author’s ID) (in above schema,
``author_ids`` is an ArrayField in Postgres):

.. code:: json

    {
       "AND": [
          {
             "BETWEEN": {
                "quanity": [10000, 15000]
             }
          },
          {
             "CONTAINS": {
                "author_ids": [8]
             }
          }
       ]
    }
