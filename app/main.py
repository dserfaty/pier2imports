from fastapi import FastAPI, Request, status
from .routers import root, orders, customers
from app.database import init_database, run_pyway_migrations
from .config.settings import get_settings
from fastapi.exceptions import RequestValidationError
from app.routers.error_handlers import validation_exception_handler

settings = get_settings()
run_pyway_migrations(settings=settings)
init_database(settings=settings)

app = FastAPI()

# Include routers
app.include_router(root.router)
app.include_router(orders.router)
app.include_router(customers.router)

# Custom Error handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# TODO:
#   - README instructions + explanations
