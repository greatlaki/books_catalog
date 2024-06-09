from base.uow import SessionUnitOfWork
from database import engines


class PgUow(SessionUnitOfWork):
    def __init__(self):
        super().__init__(engines.pg_async_session_maker)
