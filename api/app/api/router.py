from fastapi import APIRouter

from api.app.api.v1 import users_router

router = APIRouter(prefix="/v1")

router.include_router(users_router, prefix="/users", tags=["Users"])
