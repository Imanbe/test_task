from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from api.app.api.v1.deps import get_user_service
from api.app.core import UserAlreadyExistsError, UserNotFoundError
from api.app.schemas.user import PaginatedUserResponse, UserCreate, UserResponse
from api.app.services import UserService

router = APIRouter()


@router.get("/", response_model=PaginatedUserResponse)
async def get_users(
    cursor: int | None = Query(None, ge=1, description="ID последнего пользователя"),
    limit: int = Query(100, ge=1, le=100),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_users_paginated(cursor=cursor, limit=limit)


@router.post("/", response_model=UserResponse)
async def create_user(
    payload: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    try:
        return await user_service.create_user(payload)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int = Path(..., ge=1),
    user_service: UserService = Depends(get_user_service),
):
    try:
        await user_service.delete_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
