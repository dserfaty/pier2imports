import uuid
from sqlalchemy import (
    Column, String, Boolean, ForeignKey, Integer, Numeric, Table,
    CheckConstraint, DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Association tables
customer_addresses = Table(
    "customer_addresses", Base.metadata,
    Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id", ondelete="RESTRICT"), primary_key=True),
    Column("address_id", UUID(as_uuid=True), ForeignKey("addresses.id", ondelete="RESTRICT"), primary_key=True),
    Column("address_type", String(10), nullable=False),
    CheckConstraint("address_type IN ('billing', 'shipping')", name="check_address_type")
)

order_shipping_addresses = Table(
    "order_shipping_addresses", Base.metadata,
    Column("order_id", UUID(as_uuid=True), ForeignKey("orders.id", ondelete="RESTRICT"), primary_key=True),
    Column("address_id", UUID(as_uuid=True), ForeignKey("addresses.id", ondelete="RESTRICT"), primary_key=True),
)


# Models
class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    email = Column(String(255), unique=True, nullable=False)
    telephone = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="customer")
    addresses = relationship("Address", secondary=customer_addresses, back_populates="customers")

    def __repr__(self):
        return f"<Customer(id={self.id}, email={self.email}), telephone={self.telephone})>"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    line1 = Column(String(255), nullable=False)
    line2 = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    customers = relationship("Customer", secondary=customer_addresses, back_populates="addresses")


class Store(Base):
    __tablename__ = "store"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id", ondelete="RESTRICT"))
    created_at = Column(DateTime, default=datetime.utcnow)

    address = relationship("Address")
    orders = relationship("Order", back_populates="store")


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="RESTRICT"))
    billing_address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id", ondelete="RESTRICT"))
    store_id = Column(UUID(as_uuid=True), ForeignKey("store.id", ondelete="RESTRICT"))
    pick_up = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(15), CheckConstraint("status IN ('pending', 'in_progress', 'completed', 'cancelled')"))

    customer = relationship("Customer", back_populates="orders")
    store = relationship("Store", back_populates="orders")
    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    shipping_addresses = relationship("Address", secondary=order_shipping_addresses)
    items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order(id={self.id}, customer_id={self.customer_id}, items={self.items})>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="RESTRICT"))
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
