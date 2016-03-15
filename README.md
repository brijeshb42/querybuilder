# Querybuilder


For the following Table example:
```sql
CREATE TABLE article (
    id integer NOT NULL,
    created timestamp without time zone NOT NULL,
    title character varying(255) NOT NULL,
    type_id integer NOT NULL,
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
```


## Specifications

* For all articles with `type_id` equal to `1` (`type_id = 1`):
   ```json
   {
      "EQ": {
         "type_id": 1
      }
   }
   ```
   Same structure is for:

   | Condition     | JSON KEY   | Symbol  | JSON Query |
   | ------------- |:----------- |:----- |:------ |
   | Less than | LT | < | `{"LT": {"type_id": 2}}` |
   | Less than or Equal to | LE | <= | `{"LE": {"type_id": 2}}` |
   | Greater than | GT | > | `{"GT": {"type_id": 2}}` |
   | Greater than or Equal to | GE | >= | `{"GE": {"type_id": 2}}` |
   | Not equal | NE | != | `{"NE": {"type_id": 2}}` |

##### IN
For all articles where `type_id` is in `[1, 2, 3]`, the JSON query will be:
```json
{
   "IN": {
      "pageviews": [1, 2, 3]
   }
}
```

##### BETWEEN
For all articles with `pageviews` between 10000 and 15000, the JSON query will be:
```json
{
   "BETWEEN": {
      "pageviews": [10000, 15000]
   }
}
```

##### CONTAINS_ANY
For all articles where `author_ids` contains any of `8, 9, 10`, the JSON query will be:
```json
{
   "CONTAINS_ANY": {
      "author_ids": [8, 9, 10]
   }
}
```
##### CONTAINS_ALL
For all articles where `author_ids` contains all of `8, 9`, the JSON query will be:
```json
{
   "CONTAINS_ALL": {
      "author_ids": [8, 9]
   }
}
```

##### STARTSWITH
* For all articles where `title` starts with `Film Review`, the JSON query will be:
```json
{
   "STARTSWITH": {
      "title": "Film Review"
   }
}
```

#### Complex Queries

* Complex queryies can contain nested structures of `OR` or `AND` or both.

For all articles with `pageviews` between 10000 and 15000 and whose `author_ids` contains `8`(the author's ID) (in above schema, `author_ids` is an ArrayField in Postgres), the JSON query will be:
```json
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
```

#### Requirements

* If there is only one condition, like `pageviews` > 100, the query can directly contain outermost key as one of `EQ, NE, GT, GE, LT, LE, STARTSWITH, CONTAINS, CONTAINS_ALL, CONTAINS_ANY, BETWEEN`.

example:
```json
{
   "STARTSWITH": {
      "title": "Film Review"
   }
}
```

* But if there are more conditions involved, the outermost key must be one of `OR, AND` and their values must be array of conditions.

example:
```json
{
   "OR":[
      {
         "EQ": {
            "type_id": 1,
         }
      },
      {
         "GE": {
            "pageviews": 10000
         }
      }
   ]
}
```

### Helper for generating query

`Querybuilder` contains python implementation to generate the above queries without you having to create them by typing lots of `dict`s in your code.

Below is a query to retrieve all the articles where:

* `pageviews` >= 100 and `author_ids` contains 1
* OR
* `pageviews` <= 1000 and `type_id` != 2

The JSON will be:
```json
{
   "OR":[
      {
         "AND":[
            {
               "GE":{
                  "pageviews": 100
               }
            },
            {
               "CONTAINS":{
                  "author_ids": [1]
               }
            }
         ]
      },
      {
         "AND":[
            {
               "LE":{
                  "pageviews": 1000
               }
            },
            {
               "NE":{
                  "type_id": 2
               }
            }
         ]
      }
   ]
}
```

With helpers
```python
from querybuilder.helpers import Field as F, AND, OR
query = OR(
    AND(F("pageviews") >= 100, F("author_id") == 1),
    AND(F("pageviews") <= 1000, F("author_id") != 0)
)
```

### Example usage with Peewee ORM using builtin extension.

> This module contains an implementation for [Peewee](http://peewee-orm.com) ORM that takes as arguments, the Peewee model and the JSON query and gives an `expression` that can be directly passed as an argument in the `where()` method of the model:

```python
import peewee
from querybuilder.helpers import AND, OR, Field as F
from querybuilder.ext.peewee import get_expression_for


class Article(peewee.Model):
    id = IntegerField(primary_key=True)
    title = CharField(null=False, unique=False, index=True)
    permalink = CharField(default=None, unique=True, null=True)
    type_id = IntegerField(default=1, index=True)
    author_ids = ArrayField(index=True)
    category_ids = ArrayField(default=[], null=True, index=True)
    tags = ArrayField(CharField, null=True, default=[], index=True)
    keywords = ArrayField(CharField, null=True, default=[], index=False)  # SEO
    summary = TextField(null=True)
    content = TextField(default='')
    cover = BinaryJSONField(default={})
    editors_pick = BooleanField(default=False)
    pageviews = BigIntegerField(default=0)
    updated = DateTimeField(null=False, default=datetime.datetime.utcnow)
    published = DateTimeField(null=False, default=None, index=True)
    cust_meta = BinaryJSONField(default={}, index=True)

query = OR(
    AND(F("pageviews") >= 100, F("author_ids").contains(1)),
    AND(F("pageviews") <= 1000, F("type_id") != 0)
)

expression = get_expression_for(PeeweeModel, query)

articles = Article.select().where(expression).execute()
```
