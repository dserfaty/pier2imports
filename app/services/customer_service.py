from sqlalchemy.orm import Session
from app.models.dao import Customer
from app.models.dto import CustomerOut
from uuid import UUID
from app.models.exceptions import InvalidId, EntityNotFound
from app.config.logger import get_logger

logger = get_logger(__name__, log_level='DEBUG')


def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()


def get_customer_by_id(db: Session, _id: str) -> CustomerOut:
    try:
        _uuid = UUID(_id)
        result: Customer = db.query(Customer).filter(Customer.id == _uuid).first()
        if result is not None:
            logger.debug("returning %s", result)
            return CustomerOut.model_validate(result.__dict__, strict=False)
        else:
            logger.debug("customer not found")
            raise EntityNotFound

    except ValueError as e:
        raise InvalidId(e)
