-- noinspection SqlNoDataSourceInspectionForFile

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS pyway, customers, addresses, store, customer_addresses, orders, order_shipping_addresses, order_items;

CREATE TABLE customers
(
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email      VARCHAR(255) UNIQUE NOT NULL,
    telephone  VARCHAR(20) UNIQUE  NOT NULL,
    first_name VARCHAR(100)        NOT NULL,
    last_name  VARCHAR(100)        NOT NULL,
    created_at TIMESTAMP        DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE addresses
(
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    line1      VARCHAR(255) NOT NULL,
    line2      VARCHAR(255) NOT NULL,
    city       VARCHAR(100) NOT NULL,
    state      VARCHAR(2)   NOT NULL,
    zip_code   VARCHAR(10)  NOT NULL,
    created_at TIMESTAMP        DEFAULT CURRENT_TIMESTAMP
);

-- CREATE INDEX idx_addresses_zip_code ON addresses (zip_code);

CREATE TABLE store
(
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name       VARCHAR(100) UNIQUE NOT NULL,
    address_id UUID REFERENCES addresses (id) ON DELETE RESTRICT,
    created_at TIMESTAMP        DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customer_addresses
(
    customer_id  UUID REFERENCES customers (id) ON DELETE RESTRICT,
    address_id   UUID REFERENCES addresses (id) ON DELETE RESTRICT,
    address_type VARCHAR(10) CHECK (address_type IN ('billing', 'shipping')), -- could use a postgres enum instead
    PRIMARY KEY (customer_id, address_id, address_type)
);

CREATE TABLE orders
(
    id                 UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id        UUID REFERENCES customers (id) ON DELETE RESTRICT,
    billing_address_id UUID REFERENCES addresses (id) ON DELETE RESTRICT,
    store_id           UUID REFERENCES store (id) ON DELETE RESTRICT,
    pick_up            boolean DEFAULT true,
    created_at         TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,
    status             VARCHAR(15) CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled'))
);

CREATE TABLE order_shipping_addresses
(
    order_id   UUID REFERENCES orders (id) ON DELETE RESTRICT,
    address_id UUID REFERENCES addresses (id) ON DELETE RESTRICT,
    PRIMARY KEY (order_id, address_id)
);

CREATE TABLE order_items
(
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id     UUID REFERENCES orders (id) ON DELETE RESTRICT,
    product_name VARCHAR(255)   NOT NULL,
    quantity     INT            NOT NULL,
    unit_price   NUMERIC(10, 2) NOT NULL
);
