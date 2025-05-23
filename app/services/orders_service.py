from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func, desc, asc
from app.models.dao import Customer, Order, Address, order_shipping_addresses
from app.config.logger import get_logger
from app.models.dto import AllOrdersOut, AddressOut, OrderOut, OrderCountsByZipOut, OrderCountByZipOut, \
    OrderCountsByHourOut, OrderCountByHourOut, CustomerOrderCountOut, CustomerOrderCountsOut
from app.models.exceptions import EntityNotFound

logger = get_logger(__name__, log_level='DEBUG')


def get_customer_orders_by_email_or_telephone(db: Session, customer_contact: str) -> AllOrdersOut:
    customer = db.query(Customer).filter(
        or_(Customer.email == customer_contact, Customer.telephone == customer_contact)
    ).first()

    if not customer:
        logger.debug("customer not found")
        raise EntityNotFound

    orders = (
        db.query(Order)
        .options(
            joinedload(Order.billing_address),
            joinedload(Order.shipping_addresses)
        )
        .filter(Order.customer_id == customer.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    history = []
    for order in orders:
        billing_address = order.billing_address
        billing = AddressOut(
            id=billing_address.id,
            line1=billing_address.line1,
            line2=billing_address.line2,
            city=billing_address.city,
            state=billing_address.state,
            zip_code=billing_address.zip_code,
            created_at=billing_address.created_at,
        ) if billing_address else None

        shipping = [
            AddressOut(
                id=addr.id,
                line1=addr.line1,
                line2=addr.line2,
                city=addr.city,
                state=addr.state,
                zip_code=addr.zip_code,
                created_at=addr.created_at,
            ) for addr in order.shipping_addresses]

        history.append(OrderOut(
            id=order.id,
            store_id=order.store_id,
            status=order.status,
            pick_up=order.pick_up,
            created_at=order.created_at,
            billing_address=billing,
            shipping_addresses=shipping)
        )

    result = AllOrdersOut(id=customer.id,
                          email=customer.email,
                          telephone=customer.telephone,
                          first_name=customer.first_name,
                          last_name=customer.last_name,
                          created_at=customer.created_at,
                          orders=history)

    logger.debug("result: %s", result)

    return result


def get_order_counts_by_billing_zip(db: Session, ascending: bool = False, limit: int = 10) -> OrderCountsByZipOut:
    query = (
        db.query(Address.zip_code, func.count(Order.id).label("order_count"))
        .join(Order, Order.billing_address_id == Address.id)
        .group_by(Address.zip_code)
        .order_by(asc("order_count") if ascending else desc("order_count"))
        .limit(limit)
    )
    query_result = query.all()
    counts = [OrderCountByZipOut(zip_code=row.zip_code, count=row.order_count) for row in query_result]
    logger.debug("result: %s", query_result)
    logger.debug("counts: %s", counts)
    return OrderCountsByZipOut(counts=counts)


def get_order_counts_by_shipping_zip(db: Session, ascending: bool = False, limit: int = 10) -> OrderCountsByZipOut:
    query = (
        db.query(Address.zip_code, func.count(func.distinct(Order.id)).label("order_count"))
        .join(order_shipping_addresses, Address.id == order_shipping_addresses.c.address_id)
        .join(Order, Order.id == order_shipping_addresses.c.order_id)
        .group_by(Address.zip_code)
        .order_by(asc("order_count") if ascending else desc("order_count"))
        .limit(limit)
    )
    query_result = query.all()
    counts = [OrderCountByZipOut(zip_code=row.zip_code, count=row.order_count) for row in query_result]
    logger.debug("result: %s", query_result)
    logger.debug("counts: %s", counts)
    return OrderCountsByZipOut(counts=counts)


def get_in_store_orders_by_hour(db: Session, ascending: bool = False) -> OrderCountsByHourOut:
    hour = func.extract('hour', Order.created_at).label('hour')
    order_count = func.count(Order.id).label('order_count')

    query = (
        db.query(hour, order_count)
        .outerjoin(order_shipping_addresses, Order.id == order_shipping_addresses.c.order_id)
        .filter(order_shipping_addresses.c.order_id == None)  # in-store orders
        .group_by(hour)
        .order_by(asc("order_count") if ascending else desc("order_count"))
    )

    query_result = query.all()
    logger.debug("counts: %s", query_result)
    counts = [OrderCountByHourOut(hour=row.hour, count=row.order_count) for row in query_result]
    return OrderCountsByHourOut(counts=counts)


def get_top_in_store_users(db: Session, limit: int = 5) -> CustomerOrderCountsOut:
    order_count = func.count(Order.id).label("order_count")

    query = (
        db.query(
            Customer.id,
            Customer.first_name,
            Customer.last_name,
            order_count
        )
        .join(Order, Order.customer_id == Customer.id)
        .outerjoin(order_shipping_addresses, Order.id == order_shipping_addresses.c.order_id)
        .filter(order_shipping_addresses.c.order_id == None)  # In-store orders
        .group_by(Customer.id, Customer.first_name, Customer.last_name)
        .order_by(desc(order_count))
        .limit(limit)
    )

    query_result = query.all()
    counts = [CustomerOrderCountOut(
        id=row.id,
        first_name=row.first_name,
        last_name=row.last_name,
        orders=row.order_count
    ) for row in query_result]

    logger.debug("result: %s", query_result)
    logger.debug("counts: %s", counts)
    return CustomerOrderCountsOut(counts=counts)
