from typing import Any

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert

from base.repository import PgRepository
from user.models import User


class UserRepository(PgRepository):
    model = User

    async def add_user(self, values: dict[str, str]) -> User:
        insert_stmt = insert(self.model).returning(self.model)
        user_pk = await self.session.execute(insert_stmt, values)
        return user_pk.scalar_one()

    async def update_user(self, values: dict[str, Any]):
        update_stmt = update(self.model).values(**values)
        await self.session.execute(update_stmt)

    async def foo(self, values: list[dict[str, str]]):
        res = await self.session.execute(insert(self.model).returning(self.model), values)
        print(res.scalars())
