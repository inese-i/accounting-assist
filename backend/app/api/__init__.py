from fastapi import APIRouter
from app.api.endpoints import accounts, bilanz

api_router = APIRouter()

# Include account routes
api_router.include_router(
    accounts.router, 
    prefix="/accounts", 
    tags=["accounts"]
)

# Include bilanz routes
api_router.include_router(
    bilanz.router,
    tags=["bilanz"]
)
