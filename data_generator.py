#!/usr/bin/env python3
import psycopg2
import psycopg2.extras
import string
import sys
import re

from random import randint, choice
from datetime import datetime, timedelta


db_name, db_user, db_pass = "", "", ""
tables = ['impressions', 'clicks', 'orders']
conn_string = "host='localhost' dbname='{}' user='{}' password='{}'".format(db_name, db_user, db_pass)


def db_connect(db_name=db_name, db_user=db_user, db_pass=db_pass):
    """ get a connection, if a connect cannot be made an exception will be raised here """
    conn = psycopg2.connect(conn_string)
    return conn


def generate_data(conn, max_pid=10000):
    """ Заполнить таблицы данными с помощью BULK INSERT """
    bulk_count = 10

    current_datetime = datetime.now() - timedelta(days=30)
    start_time = current_datetime
    delta = timedelta(seconds=int(timedelta(days=30).total_seconds() / max_pid))
    cursor = conn.cursor()
    total = dict([(t, 0) for t in tables])

    for tbl in tables:
        query, query_data = "", []
        current_datetime = start_time
        for pid in range(1, max_pid+1):
            # пропустить некоторые случайные project_id в таблице
            if randint(1, 100) % 10 == 0:
                continue

            # вставить несколько записей для случайных project_id
            recN = 1
            if randint(1, 100) % 10 == 3:
                recN = randint(3, 10)

            for i in range(recN):
                rand_int = randint(1, 100000)
                rand_text = ""
                for i in range(100):
                    rand_text += choice(string.ascii_letters)
                query_data.append((current_datetime, pid, rand_text, rand_int))
                current_datetime += delta

            if pid % bulk_count == 0:
                query = "INSERT INTO {} (created, pid, other_field, other_field2) VALUES %s ".format(tbl)

                psycopg2.extras.execute_values(
                    cursor, query, query_data, template=None, page_size=len(query_data))

                conn.commit()

                total[tbl] += len(query_data)
                query = ""
                query_data = []

    for k, v in total.items():
        print("Total inserted in {}: {}".format(k, v))


if __name__ == "__main__":
    connection = db_connect()
    max_pid = 10000
    if len(sys.argv) == 2:
        max_pid = int(sys.argv[1])

    generate_data(connection, max_pid)


""" -- Create tables with indexes:

CREATE TABLE impressions (id SERIAL, created TIMESTAMP, pid INT, other_field TEXT, other_field2 INT);
CREATE INDEX impressions_pid_idx ON public.impressions USING btree (pid);
CREATE INDEX ON impressions(created);

CREATE TABLE clicks (id SERIAL, created TIMESTAMP, pid INT, other_field TEXT, other_field2 INT);
CREATE INDEX clicks_pid_idx ON public.clicks USING btree (pid);
CREATE INDEX ON clicks(created);

CREATE TABLE orders (id SERIAL, created TIMESTAMP, pid INT, other_field TEXT, other_field2 INT);
CREATE INDEX orders_pid_idx ON public.orders USING btree (pid);
CREATE INDEX ON orders(created);

Total inserted in impressions: 139888
Total inserted in clicks: 139433
Total inserted in orders: 139918

# -- count all rows
select count(*) from impressions; select count(*) from clicks; select count(*) from orders; 

# -- drop all
drop table clicks; drop table impressions; drop table orders;

# -- truncate tables
delete from impressions ; delete from clicks; delete from orders;

"""