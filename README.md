# SQL statistic query
Hard SQL stat query for tables with impressions, clicks, orders.

Each table has project_id field (pid), and we need to extract with one query - aggregated number of impressions,
clicks and orders per each project_id, and additionally conversion rate CR=orders / clicks

# Release notes

Python3 and postgres 9.3 is needed. Table schema is in **create.sql**, statistic query is in 
[**stats.sql**](https://github.com/moonsly/sql_statistics/blob/master/stats.sql)

We can record random data in tables using 
[**data_generator.py**](https://github.com/moonsly/sql_statistics/blob/master/data_generator.py)

# Tests

See testing_sql.txt

# Example output

```
  pid  | impressions | clicks | orders |        cr         
-------+-------------+--------+--------+-------------------
     1 |           8 |      1 |      1 |                 1
     2 |           1 |      1 |      1 |                 1
     3 |           1 |      0 |      1 |          Infinity
     4 |           0 |      1 |      1 |                 1
     5 |           9 |      9 |      1 | 0.111111111111111
     6 |           1 |      1 |      0 |                 0
     7 |           1 |      1 |      1 |                 1
     8 |           1 |      1 |      1 |                 1
     9 |           1 |      0 |      1 |          Infinity
    10 |           1 |     10 |      1 |               0.1
```
