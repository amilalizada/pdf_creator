from fastapi import APIRouter

from app.router import router as pdf_router

router = APIRouter()

router.include_router(pdf_router)

