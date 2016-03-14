# Querybuilder

A module to build human readable SQL query string and then optionally convert them to `where()` caluse expressions for [Peewee](http://peewee-orm.com).

For the following query:
```python
from querybuilder import Field as F, AND, OR
query = OR(
    AND(F("pageviews") >= 100, F("author_id") == 1),
    AND(F("pageviews") <= 1000, F("author_id") != 0)
)
```
The output is a JSON:
```json
{
   "OR":[
      {
         "AND":[
            {
               "GE":{
                  "pageviews":100
               }
            },
            {
               "EQ":{
                  "author_id":1
               }
            }
         ]
      },
      {
         "AND":[
            {
               "LE":{
                  "pageviews":1000
               }
            },
            {
               "NE":{
                  "author_id":0
               }
            }
         ]
      }
   ]
}
```
