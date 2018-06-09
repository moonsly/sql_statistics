CREATE TABLE impressions (id SERIAL, created TIMESTAMP, pid INT, other_field TEXT, other_field2 INT);
CREATE INDEX impressions_pid_idx ON public.impressions USING btree (pid);
CREATE INDEX ON impressions(created);

CREATE TABLE clicks (id SERIAL, created TIMESTAMP, pid INT, other_field TEXT, other_field2 INT);
CREATE INDEX clicks_pid_idx ON public.clicks USING btree (pid);
CREATE INDEX ON clicks(created);

CREATE TABLE orders (id SERIAL, created TIMESTAMP, pid INT, other_field TEXT, other_field2 INT);
CREATE INDEX orders_pid_idx ON public.orders USING btree (pid);
CREATE INDEX ON orders(created);