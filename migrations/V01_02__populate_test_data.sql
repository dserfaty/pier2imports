-- Customers
INSERT INTO customers (id, email, telephone, first_name, last_name)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'arthur.dent@galaxy.com', '555-0101', 'Arthur', 'Dent'),
    ('22222222-2222-2222-2222-222222222222', 'ford.prefect@galaxy.com', '555-0102', 'Ford', 'Prefect'),
    ('33333333-3333-3333-3333-333333333333', 'zaphod@beeblebrox.com', '555-0103', 'Zaphod', 'Beeblebrox'),
    ('44444444-4444-4444-4444-444444444444', 'trillian@galaxy.com', '555-0104', 'Tricia', 'McMillan'),
    ('55555555-5555-5555-5555-555555555555', 'marvin@robots.org', '555-0105', 'Marvin', 'Paranoid');

-- Addresses
INSERT INTO addresses (id, line1, line2, city, state, zip_code)
VALUES
    ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', '42 Galaxy Way', 'Flat 5A', 'Douglasville', 'GA', '30135'),
    ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', '12 Magrathea Rd', 'Suite 101', 'Babelton', 'TX', '73301'),
    ('aaaaaaa3-aaaa-aaaa-aaaa-aaaaaaaaaaa3', '9 Heart of Gold Blvd', 'Pod 2', 'Betelgeuse', 'NY', '10001'),
    ('aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa4', '7 Infinite Improbability Dr', 'Unit 9', 'Frogstar', 'CA', '90001'),
    ('aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa5', '26 End of the Universe Plaza', '', 'End of the Universe', 'CA', '94121');

-- Store
INSERT INTO store (id, name, address_id)
VALUES
    ('dddddddd-dddd-dddd-dddd-dddddddddd01', 'Milliways Store', 'aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa4');

-- Customer Addresses
INSERT INTO customer_addresses (customer_id, address_id, address_type)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'billing'),
    ('11111111-1111-1111-1111-111111111111', 'aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 'shipping'),
    ('22222222-2222-2222-2222-222222222222', 'aaaaaaa3-aaaa-aaaa-aaaa-aaaaaaaaaaa3', 'billing'),
    ('33333333-3333-3333-3333-333333333333', 'aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 'shipping'),
    ('55555555-5555-5555-5555-555555555555', 'aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa5', 'billing'),
    ('55555555-5555-5555-5555-555555555555', 'aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa5', 'shipping');

-- Orders
INSERT INTO orders (id, customer_id, billing_address_id, store_id, pick_up, status, created_at)
VALUES
    ('99999999-9999-9999-9999-999999999901', '11111111-1111-1111-1111-111111111111', 'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'dddddddd-dddd-dddd-dddd-dddddddddd01', true, 'completed', '2025-01-05 09:00:00+00'),
    ('99999999-9999-9999-9999-999999999902', '11111111-1111-1111-1111-111111111111', 'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'dddddddd-dddd-dddd-dddd-dddddddddd01', false, 'completed', '2025-02-05 10:00:00+00'),
    ('99999999-9999-9999-9999-999999999903', '22222222-2222-2222-2222-222222222222', 'aaaaaaa3-aaaa-aaaa-aaaa-aaaaaaaaaaa3', 'dddddddd-dddd-dddd-dddd-dddddddddd01', true, 'completed', '2025-02-05 13:00:00+00'),
    ('99999999-9999-9999-9999-999999999904', '55555555-5555-5555-5555-555555555555', 'aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa4', 'dddddddd-dddd-dddd-dddd-dddddddddd01', true, 'completed', '2025-04-05 13:10:00+00'),
    ('99999999-9999-9999-9999-999999999905', '55555555-5555-5555-5555-555555555555', 'aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa5', 'dddddddd-dddd-dddd-dddd-dddddddddd01', false, 'completed', '2025-04-05 13:50:00+00'),
    ('99999999-9999-9999-9999-999999999906', '55555555-5555-5555-5555-555555555555', 'aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa5', 'dddddddd-dddd-dddd-dddd-dddddddddd01', false, 'completed', '2025-04-05 23:00:00+00'),
    ('99999999-9999-9999-9999-999999999907', '55555555-5555-5555-5555-555555555555', 'aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa5', 'dddddddd-dddd-dddd-dddd-dddddddddd01', false, 'completed', '2025-05-05 22:00:00+00'),
    ('99999999-9999-9999-9999-999999999908', '55555555-5555-5555-5555-555555555555', 'aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa4', 'dddddddd-dddd-dddd-dddd-dddddddddd01', true, 'completed', '2025-05-05 22:05:00+00');

-- TODO: more in store orders

-- Order Shipping Addresses
INSERT INTO order_shipping_addresses (order_id, address_id)
VALUES
    ('99999999-9999-9999-9999-999999999902', 'aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2'),
    ('99999999-9999-9999-9999-999999999902', 'aaaaaaa3-aaaa-aaaa-aaaa-aaaaaaaaaaa3'),
    ('99999999-9999-9999-9999-999999999905', 'aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa5'),
    ('99999999-9999-9999-9999-999999999906', 'aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa5'),
    ('99999999-9999-9999-9999-999999999907', 'aaaaaaa4-aaaa-aaaa-aaaa-aaaaaaaaaaa5');

-- Order Items
INSERT INTO order_items (id, order_id, product_name, quantity, unit_price)
VALUES
    (uuid_generate_v4(), '99999999-9999-9999-9999-999999999901', 'Pan Galactic Sofa', 1, 999.99),
    (uuid_generate_v4(), '99999999-9999-9999-9999-999999999902', 'Towel Rack', 1, 42.00),
    (uuid_generate_v4(), '99999999-9999-9999-9999-999999999902', 'Tea Maker', 2, 75.00),
    (uuid_generate_v4(), '99999999-9999-9999-9999-999999999903', 'Holographic Table', 1, 1288.88),
    (uuid_generate_v4(), '99999999-9999-9999-9999-999999999904', 'Sirius Cybernetics Chair', 1, 799.00),
    (uuid_generate_v4(), '99999999-9999-9999-9999-999999999905', 'Towel (Basic)', 1, 15.95),
    (uuid_generate_v4(), '99999999-9999-9999-9999-999999999906', 'Fish (Babel Type)', 2, 249.90),
    (uuid_generate_v4(), '99999999-9999-9999-9999-999999999907', 'Discombobulator', 1, 199.95),
    (uuid_generate_v4(), '99999999-9999-9999-9999-999999999907', 'Galactic Encyclopedia', 1, 999.95),
    (uuid_generate_v4(), '99999999-9999-9999-9999-999999999908', 'Imperial Blaster', 1, 2999.95);
