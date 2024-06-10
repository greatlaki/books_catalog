import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from base.utils import verify_and_update
from pg.repositories.entity_repository import EntityRepository
from pg.repositories.user_repository import User

security = HTTPBasic()

logger = logging.getLogger('app')


class DatabaseUser:
    async def current_user_dependency(
        self, credentials: Annotated[HTTPBasicCredentials, Depends(security)]
    ) -> User | None:
        async with EntityRepository(User) as repository:
            user = await repository.find_one(email=credentials.username)

            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

            verified, updated_password_hash = verify_and_update(credentials.password, user.hashed_password)
            if not verified:
                return None

            if updated_password_hash is not None:
                await repository.edit_one(pk=user.id, **{'hashed_password': updated_password_hash})

        return user

    def current_user(self):
        return self.current_user_dependency


core_user = DatabaseUser()

current_active_user = core_user.current_user()
CurrentActiveUserDep = Annotated[User, Depends(current_active_user)]
