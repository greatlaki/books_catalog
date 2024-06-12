import logging
from typing import Any, Callable, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

TExc = TypeVar('TExc', bound=Exception)

logger = logging.getLogger('app')


class UnitOfWork(object):
    def __init__(self) -> None:
        pass

    async def __aenter__(self) -> 'UnitOfWork':
        await self.aenter()
        return self

    async def __aexit__(self, *args, **kwargs) -> bool:
        await self.aexit(*args, **kwargs)
        return False

    async def aenter(self):
        pass

    async def aexit(self, exc_type: type[TExc] | None, exc: TExc | None, traceback: Any | None):
        if exc_type is not None:
            logger.exception(f'error during executing query: {exc_type}: {exc}')
            raise exc


class SessionUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession] | None) -> None:
        super().__init__()
        self.session = None
        self.session_factory = session_factory

    async def aenter(self):
        await super().aenter()
        await self.make_session()

    async def aexit(self, exc_type: type[TExc] | None, exc: TExc | None, traceback: Any | None) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

        await self.close()

        await super().aexit(exc_type, exc, traceback)

    async def make_session(self) -> None:
        assert self.session is None
        assert self.session_factory is not None

        self.session = self.session_factory()

    async def commit(self) -> None:
        assert self.session is not None
        await self.session.commit()

    async def rollback(self) -> None:
        assert self.session is not None
        await self.session.rollback()

    async def close(self) -> None:
        assert self.session is not None

        await self.session.close()
        self.session = None
