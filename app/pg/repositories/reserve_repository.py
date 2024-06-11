from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from base.repository import PgRepository
from pg.models import Reserve


class ReserveRepository(PgRepository):
    model = Reserve

    async def reserve_book(self, data: dict[str, int | datetime]):
        stmt = insert(self.model).returning(self.model)
        reserve = await self.session.execute(stmt, data)
        return reserve.scalar_one_or_none()

    async def get_reserved_book(self, book_id: int, start_booking: date, end_booking: date) -> int | None:
        stmt = (
            select(self.model.id)
            .where(self.model.book_id == book_id)
            .where(self.model.booked_at <= end_booking)
            .where(self.model.due_date >= start_booking)
        )
        reserved_book = await self.session.execute(stmt)
        return reserved_book.scalar_one_or_none()
