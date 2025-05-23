from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services import orders_service
from app.database import get_db
import traceback
from app.models.exceptions import InvalidId, EntityNotFound
from app.config.logger import get_logger

router = APIRouter(prefix="/orders", tags=["orders"])
logger = get_logger(__name__, log_level='INFO')


@router.get("")
async def get_orders(customer_contact: str, db: Session = Depends(get_db)):
    try:
        orders = orders_service.get_customer_orders_by_email_or_telephone(db, customer_contact=customer_contact)
        if orders is not None:
            return orders
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except ValueError as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=404, detail="Customer not found")
    except EntityNotFound:
        raise HTTPException(status_code=404, detail="Customer not found")
    except InvalidId as e:
        raise HTTPException(status_code=400, detail="Invalid customer id")
    except HTTPException as e:
        raise e
    except Exception:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="An Unexpected error occurred - See logs for details")


@router.get("/stats/counts/by_billing_zip")
async def get_orders_count_by_billing_zip(ascending: bool = Query(False),
                                          limit: int = Query(10, ge=1, le=20),
                                          db: Session = Depends(get_db)):
    try:
        return orders_service.get_order_counts_by_billing_zip(db, ascending, limit)
    except Exception:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="An Unexpected error occurred - See logs for details")


@router.get("/stats/counts/by_shipping_zip")
async def get_orders_count_by_shipping_zip(ascending: bool = Query(False),
                                           limit: int = Query(10, ge=1, le=20),
                                           db: Session = Depends(get_db)):
    try:
        return orders_service.get_order_counts_by_shipping_zip(db, ascending, limit)
    except Exception:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="An Unexpected error occurred - See logs for details")


@router.get("/stats/in_store_purchases/by_hour")
async def get_in_store_purchases_by_hour(ascending: bool = Query(False), db: Session = Depends(get_db)):
    try:
        return orders_service.get_in_store_orders_by_hour(db, ascending)
    except Exception:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="An Unexpected error occurred - See logs for details")


@router.get("/stats/top_in_store_users")
async def get_top_in_store_users(limit: int = Query(5, ge=5, le=10), db: Session = Depends(get_db)):
    try:
        return orders_service.get_top_in_store_users(db, limit)
    except Exception:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="An Unexpected error occurred - See logs for details")
