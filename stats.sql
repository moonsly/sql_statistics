WITH pids AS (
    SELECT all(impressions.pid)
    FROM impressions WHERE created BETWEEN now() - interval '31 days' AND now() - interval '20 days'
    UNION
        SELECT all(orders.pid)
        FROM orders WHERE created BETWEEN now() - interval '31 days' AND now() - interval '20 days'
    UNION
        SELECT all(clicks.pid)
        FROM clicks WHERE created BETWEEN now() - interval '31 days' AND now() - interval '20 days'
),
impressions_joined AS (
    SELECT pids.pid AS pid, COUNT(i.pid) AS impressions FROM pids
    LEFT JOIN impressions AS i ON pids.pid=i.pid GROUP BY pids.pid ORDER BY pids.pid
),
clicks_joined AS (
    SELECT pids.pid AS pid, COUNT(c.pid) AS clicks FROM pids
    LEFT JOIN clicks AS c ON pids.pid=c.pid GROUP BY pids.pid ORDER BY pids.pid
),
orders_joined AS (
    SELECT pids.pid AS pid, COUNT(o.pid) AS orders from pids
    LEFT JOIN orders AS o ON pids.pid=o.pid GROUP BY pids.pid ORDER BY pids.pid
)

SELECT pids.pid, ij.impressions, cj.clicks, oj.orders, 
    CASE WHEN cj.clicks <= 0 THEN FLOAT8 'infinity' ELSE FLOAT8(oj.orders) / FLOAT8(cj.clicks) END AS cr
    FROM pids, orders_joined oj, clicks_joined cj, impressions_joined ij
    WHERE oj.pid=pids.pid AND cj.pid=oj.pid AND ij.pid=oj.pid
    ORDER BY pids.pid;