from fastapi import APIRouter, Depends
from typing import Annotated
from ..config.settings import Settings, get_settings


router = APIRouter(prefix="", tags=["root"])


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/health")
async def get_health(settings: Annotated[Settings, Depends(get_settings)]):
    return {"name": f"{settings.app_name}", "version": f"{settings.version}"}
