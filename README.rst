Querybuilder
============

For the following Table example:

.. code:: sql

    CREATE TABLE article (
        id integer NOT NULL,
        created timestamp without time zone NOT NULL,
        title character varying(255) NOT NULL,
        type_id integer NOT NULL,
        topic_id integer NOT NULL,
        author_ids integer[] NOT NULL,
        category_ids integer[],
        tags character varying(255)[],
        keywords character varying(255)[],
        summary text,
        content text NOT NULL,
        cover jsonb NOT NULL,
        editors_pick boolean NOT NULL,
        pageviews bigint NOT NULL,
        updated timestamp without time zone NOT NULL,
        published timestamp without time zone,
        permalink character varying(255),
        cust_meta jsonb
    );

Specifications
--------------

-  For all articles with ``type_id`` equal to ``1`` (``type_id = 1``):
   ``json    {   "EQ": {      "type_id": 1   }    }`` Same structure is
   for:

+----------------------------+------------+----------+------------------------------+
| Condition                  | JSON KEY   | Symbol   | JSON Query                   |
+============================+============+==========+==============================+
| Less than                  | LT         | <        | ``{"LT": {"type_id": 2}}``   |
+----------------------------+------------+----------+------------------------------+
| Less than or Equal to      | LE         | <=       | ``{"LE": {"type_id": 2}}``   |
+----------------------------+------------+----------+------------------------------+
| Greater than               | GT         | >        | ``{"GT": {"type_id": 2}}``   |
+----------------------------+------------+----------+------------------------------+
| Greater than or Equal to   | GE         | >=       | ``{"GE": {"type_id": 2}}``   |
+----------------------------+------------+----------+------------------------------+
| Not equal                  | NE         | !=       | ``{"NE": {"type_id": 2}}``   |
+----------------------------+------------+----------+------------------------------+

IN
''

For all articles where ``type_id`` is in ``[1, 2, 3]``, the JSON query
will be:

.. code:: json

    {
       "IN": {
          "pageviews": [1, 2, 3]
       }
    }

BETWEEN
'''''''

For all articles with ``pageviews`` between 10000 and 15000, the JSON
query will be:

.. code:: json

    {
       "BETWEEN": {
          "pageviews": [10000, 15000]
       }
    }

CONTAINS\_ANY
'''''''''''''

For all articles where ``author_ids`` contains any of ``8, 9, 10``, the
JSON query will be:

.. code:: json

    {
       "CONTAINS_ANY": {
          "author_ids": [8, 9, 10]
       }
    }

CONTAINS\_ALL
'''''''''''''

For all articles where ``author_ids`` contains all of ``8, 9``, the JSON
query will be:

.. code:: json

    {
       "CONTAINS_ALL": {
          "author_ids": [8, 9]
       }
    }

STARTSWITH
''''''''''

-  For all articles where ``title`` starts with ``Film Review``, the
   JSON query will be:

   .. code:: json

       {
          "STARTSWITH": {
         "title": "Film Review"
          }
       }

Complex Queries
^^^^^^^^^^^^^^^

-  Complex queryies can contain nested structures of ``OR`` or ``AND``
   or both.

For all articles with ``pageviews`` between 10000 and 15000 and whose
``author_ids`` contains ``8``\ (the author’s ID) (in above schema,
``author_ids`` is an ArrayField in Postgres), the JSON query will be:

.. code:: json

    {
       "AND": [
          {
             "BETWEEN": {
                "pageviews": [10000, 15000]
             }
          },
          {
             "CONTAINS": {
                "author_ids": [8]
             }
          }
       ]
    }

Requirements
^^^^^^^^^^^^

-  If there is only one condition, like ``pageviews`` > 100, the query
   can directly contain outermost key as one of
   ``EQ, NE, GT, GE, LT, LE, STARTSWITH, CONTAINS, CONTAINS_ALL, CONTAINS_ANY, BETWEEN``.

example:

.. code:: json

    {
       "STARTSWITH": {
          "title": "Film Review"
       }
    }

-  But if there are more conditions involved, the outermost key must be
   one of \`OR
