import datetime

import pytest
from app.models.dto import AllOrdersOut
import uuid


def test_orders():
    orders_out = AllOrdersOut(
        id=uuid.uuid4(),
        email='test@test.com',
        telephone='1234567890',
        first_name='Test',
        last_name='User',
        created_at=datetime.datetime.now(datetime.UTC),
        orders=[]
    )
    assert orders_out is not None
