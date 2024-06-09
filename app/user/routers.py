from typing import Any

from fastapi import APIRouter, HTTPException, status

from base.utils import get_hashed_password
from main.depends import CurrentActiveUserDep
from pg.repositories.user_repository import UserRepository
from user.schemas import UserCreateSchema, UserReadSchema, UserUpdate

user_router = APIRouter()


@user_router.post(
    '/register',
    response_model=UserReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register(user: UserCreateSchema) -> dict[str, Any]:
    async with UserRepository() as repository:
        existing_user = await repository.find_one(email=user.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

        encrypted_password = get_hashed_password(user.password)

        data = user.dict()
        data.pop('password')
        data['hashed_password'] = encrypted_password

        new_user = await repository.add_user(data)

        return {'id': new_user.id, 'email': new_user.email}


@user_router.post(
    '/login',
    status_code=status.HTTP_200_OK,
)
async def login(user: CurrentActiveUserDep) -> dict[str, Any]:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

    return {'id': user.id, 'user_email': user.email}


@user_router.get('/{user_id}', response_model=UserReadSchema, status_code=status.HTTP_200_OK)
async def get_profile(user_id: int, user: CurrentActiveUserDep):
    async with UserRepository() as repository:
        target_user = await repository.find_one(id=user_id)

    if target_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User was not find')

    return {
        'id': target_user.id,
        'email': target_user.email,
        'first_name': target_user.first_name,
        'last_name': target_user.last_name,
        'avatar': target_user.avatar,
    }


@user_router.patch('/{user_id}', response_model=UserReadSchema, status_code=status.HTTP_200_OK)
async def update_profile(user_id: int, data: UserUpdate, user: CurrentActiveUserDep) -> dict[str, Any]:
    async with UserRepository() as repository:
        user = await repository.edit_one(pk=user_id, **data.model_dump(exclude_none=True))
    return {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'avatar': user.avatar,
    }


@user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_profile(user_id: int, user: CurrentActiveUserDep):
    async with UserRepository() as repository:
        await repository.delete_one(pk=user_id)
    return {'status': True}
