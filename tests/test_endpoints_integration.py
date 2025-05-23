from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

'''
Some simple integration tests for the api endpoints
In the interest of time since this is just a demo, running the integration tests require an actual postgres
database to run. Instead, we should normally rely on some in memory database such as H2 but
making it work is beyond the scope of this exercise.
This will make the test fail if the data in the database is changed.
'''


def test_get_customer():
    response = client.get("/customers/11111111-1111-1111-1111-111111111111")
    assert response.status_code == 200
    json = response.json()
    assert json["id"] == "11111111-1111-1111-1111-111111111111"
    assert json["email"] == "arthur.dent@galaxy.com"
    assert json["first_name"] == "Arthur"
    assert json["last_name"] == "Dent"
    assert json["telephone"] == "555-0101"
    assert json["created_at"] is not None


def test_get_orders():
    response = client.get("/orders?customer_contact=555-0101")
    assert response.status_code == 200
    json = response.json()
    assert json["id"] == "11111111-1111-1111-1111-111111111111"
    assert json["email"] == "arthur.dent@galaxy.com"
    assert json["first_name"] == "Arthur"
    assert json["last_name"] == "Dent"
    assert json["telephone"] == "555-0101"
    assert json["created_at"] is not None
    orders = json.get("orders")
    assert len(orders) == 2

    order0 = orders[0]
    assert order0["id"] == "99999999-9999-9999-9999-999999999902"
    assert order0["status"] == "completed"
    assert order0["pick_up"] is False
    billing0 = order0["billing_address"]
    assert billing0 is not None
    shipping0 = order0["shipping_addresses"]
    assert shipping0 is not None
    assert len(shipping0) == 2

    order1 = orders[1]
    assert order1["id"] == "99999999-9999-9999-9999-999999999901"
    assert order1["status"] == "completed"
    assert order1["pick_up"] is True
    billing1 = order1["billing_address"]
    assert billing1 is not None
    shipping1 = order1["shipping_addresses"]
    assert shipping1 is not None
    assert len(shipping1) == 0


def test_get_orders_stats_by_billing_zip():
    response = client.get("/orders/stats/counts/by_billing_zip")
    assert response.status_code == 200
    json = response.json()
    counts = json["counts"]
    assert counts is not None
    assert len(counts) == 4
    assert counts[0]["zip_code"] == "94121"
    assert counts[0]["count"] == 3


def test_get_orders_stats_by_shipping_zip():
    response = client.get("/orders/stats/counts/by_shipping_zip")
    assert response.status_code == 200
    json = response.json()
    counts = json["counts"]
    assert counts is not None
    assert len(counts) == 3
    assert counts[0]["zip_code"] == "94121"
    assert counts[0]["count"] == 3


def test_get_orders_stats_in_store_purchases_by_hour():
    response = client.get("/orders/stats/in_store_purchases/by_hour")
    assert response.status_code == 200
    json = response.json()
    counts = json["counts"]
    assert counts is not None
    assert len(counts) == 3
    assert counts[0]["hour"] == 13
    assert counts[0]["count"] == 2


def test_get_orders_stats_top_in_store_users():
    response = client.get("/orders/stats/top_in_store_users")
    assert response.status_code == 200
    json = response.json()
    counts = json["counts"]
    assert counts is not None
    assert len(counts) == 3
    assert counts[0]["id"] == "55555555-5555-5555-5555-555555555555"
    assert counts[0]["first_name"] == "Marvin"
    assert counts[0]["last_name"] == "Paranoid"
    assert counts[0]["orders"] == 2
