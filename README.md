# Querybuilder

A module to build human readable SQL query string and then optionally convert them to `where()` caluse expressions for [Peewee](http://peewee-orm.com).

```python
from querybuilder import Field as F, AND, OR
query = OR(AND(F('pageviews') >= 10000, F('author_ids').contains(7,8,9)))
```
