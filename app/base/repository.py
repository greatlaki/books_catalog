from typing import Any, Generic, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from base.models import Base
from base.uow import SessionUnitOfWork, UnitOfWork
from database.uow import PgUow

TBase = TypeVar('TBase', bound=Base)
TUow = TypeVar('TUow', bound=UnitOfWork)


class Repository(object):
    uow: TUow
    DefaultUnitOfWork: type[TUow]

    def __init__(self, uow: TUow | None = None, **kwargs: Any) -> None:
        self.uow = uow or self.DefaultUnitOfWork(**kwargs)

    async def __aenter__(self) -> 'Repository':
        await self.uow.aenter()
        return self

    async def __aexit__(self, *args, **kwargs) -> bool:
        await self.uow.aexit(*args, **kwargs)
        return False


class SaSessionRepository(Repository):
    DefaultUnitOfWork = SessionUnitOfWork

    @property
    def session(self) -> AsyncSession:
        return self.uow.session


class CrudMixin(Generic[TBase]):
    model: type[TBase]

    @property
    def session(self) -> AsyncSession: ...

    async def find_one(self, **filter_by: Any):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def edit_one(self, pk: int, **data: Any) -> TBase:
        stmt = update(self.model).values(**data).filter_by(id=pk).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_one(self, pk: int):
        stmt = delete(self.model).filter_by(id=pk)
        await self.session.execute(stmt)


class PgRepository(SaSessionRepository, CrudMixin[TBase]):
    model: type[TBase]
    DefaultUnitOfWork = PgUow
