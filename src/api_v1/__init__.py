from fastapi import APIRouter

from src.api_v1.auth.router import router as auth_router
from src.api_v1.tickets.router import router as tickets_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(tickets_router, prefix="/tickets")

