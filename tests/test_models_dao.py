import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.dao import Base, Customer, Address, Store, Order, OrderItem

DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def session():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_customer(session):
    customer = Customer(
        email="john@example.com",
        telephone="1234567890",
        first_name="John",
        last_name="Doe"
    )
    session.add(customer)
    session.commit()
    assert customer.id is not None


def test_create_address(session):
    address = Address(
        line1="123 Elm St",
        line2="Unit 4",
        city="Springfield",
        state="CA",
        zip_code="90210"
    )
    session.add(address)
    session.commit()
    assert address.id is not None


def test_create_store_with_address(session):
    address = Address(
        line1="1 Main St",
        line2="Suite 100",
        city="Townsville",
        state="NY",
        zip_code="10001"
    )
    session.add(address)
    session.commit()

    store = Store(name="Main Store", address_id=address.id)
    session.add(store)
    session.commit()

    assert store.id is not None
    assert store.address.zip_code == "10001"


def test_create_order_with_items(session):
    # Setup Customer and Address
    customer = Customer(
        email="jane@example.com",
        telephone="9876543210",
        first_name="Jane",
        last_name="Smith"
    )
    address = Address(
        line1="456 Oak St",
        line2="Apt 3",
        city="Riverdale",
        state="TX",
        zip_code="73301"
    )
    session.add_all([customer, address])
    session.commit()

    order = Order(
        customer_id=customer.id,
        billing_address_id=address.id,
        pick_up=True,
        status="pending"
    )
    item1 = OrderItem(
        order=order,
        product_name="Desk",
        quantity=1,
        unit_price=199.99
    )
    item2 = OrderItem(
        order=order,
        product_name="Chair",
        quantity=2,
        unit_price=89.99
    )

    session.add(order)
    session.commit()

    assert order.id is not None
    assert len(order.items) == 2
    assert order.items[0].product_name == "Desk"
