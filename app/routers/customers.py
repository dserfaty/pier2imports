from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import AfterValidator
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import customer_service
import traceback
from app.models.exceptions import InvalidId, EntityNotFound
from app.config.logger import get_logger
from app.validation.validation_utils import validate_uuid

router = APIRouter(prefix="/customers", tags=["customers"])
logger = get_logger(__name__, log_level='INFO')


@router.get("/{cid}")
async def get_customer(
        cid: Annotated[str, Path(title='The id of the customer to get'), AfterValidator(validate_uuid)],
        db: Session = Depends(get_db)):
    try:
        logger.warning("Getting customer with id %s", cid)
        if not cid:
            raise HTTPException(status_code=400, detail="Invalid customer id")

        customer = customer_service.get_customer_by_id(db, _id=cid)
        if customer is not None:
            return customer
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except ValueError:
        raise HTTPException(status_code=404, detail="Customer not found")
    except EntityNotFound:
        raise HTTPException(status_code=404, detail="Customer not found")
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid customer id")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="An Unexpected error occurred - See logs for details")
