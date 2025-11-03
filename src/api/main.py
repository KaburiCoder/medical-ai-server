from fastapi import APIRouter
from src.api import medical

api_router = APIRouter()
api_router.include_router(medical.router)
