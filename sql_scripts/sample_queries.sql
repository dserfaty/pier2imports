-- This file contains some sample queries for all the basic use cases

-- a total count of orders aggregated by billing zip code, descending or ascending.
SELECT a.zip_code, COUNT(DISTINCT o.id) AS order_count
FROM orders o
         JOIN order_shipping_addresses osa ON o.id = osa.order_id
         JOIN addresses a ON a.id = osa.address_id
GROUP BY a.zip_code
ORDER BY order_count DESC;
-- or ASC

-- a total count of orders aggregated by shipping zip code, descending or ascending.
SELECT a.zip_code, COUNT(DISTINCT o.id) AS order_count
FROM orders o
         JOIN order_shipping_addresses osa ON o.id = osa.order_id
         JOIN addresses a ON a.id = osa.address_id
GROUP BY a.zip_code
ORDER BY order_count DESC
LIMIT 10;


-- what times of day most in-store purchases are made?
SELECT EXTRACT(HOUR FROM o.created_at) AS hour,
       COUNT(*)                        AS order_count
FROM orders o
         LEFT JOIN order_shipping_addresses osa ON o.id = osa.order_id
WHERE osa.order_id IS NULL -- means it's an in-store purchase
GROUP BY hour
ORDER BY order_count DESC; -- or ORDER BY hour ASC


-- List top 5 users with the most number of in-store orders.
SELECT
    c.id,
    c.first_name,
    c.last_name,
    COUNT(o.id) AS order_count
FROM customers c
         JOIN orders o ON o.customer_id = c.id
         LEFT JOIN order_shipping_addresses osa ON o.id = osa.order_id
WHERE osa.order_id IS NULL  -- in-store orders
GROUP BY c.id, c.first_name, c.last_name
ORDER BY order_count DESC
LIMIT 5;

-- get all customer orders
SELECT
    c.id AS customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.telephone,
    o.id AS order_id,
    o.created_at AS order_date,
    o.status,
    o.pick_up,

    -- Billing address
    ba.line1 AS billing_line1,
    ba.line2 AS billing_line2,
    ba.city AS billing_city,
    ba.state AS billing_state,
    ba.zip_code AS billing_zip,

    -- Shipping address
    sa.id AS shipping_address_id,
    sa.line1 AS shipping_line1,
    sa.line2 AS shipping_line2,
    sa.city AS shipping_city,
    sa.state AS shipping_state,
    sa.zip_code AS shipping_zip

FROM customers c
         JOIN orders o ON c.id = o.customer_id
         LEFT JOIN addresses ba ON o.billing_address_id = ba.id
         LEFT JOIN order_shipping_addresses osa ON o.id = osa.order_id
         LEFT JOIN addresses sa ON osa.address_id = sa.id

WHERE c.email = 'arthur.dent@galaxy.com'
   OR c.telephone = '555-0101'

ORDER BY o.created_at DESC;