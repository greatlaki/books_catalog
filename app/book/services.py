from datetime import date, timedelta

from fastapi import HTTPException, status

from pg.models import Book
from pg.repositories.reserve_repository import ReserveRepository


async def check_booking_dates(target_book: Book | None, start_booking: date, end_booking: date):
    if target_book is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The book does not exist')

    async with ReserveRepository() as repository:
        reserved_book = await repository.get_reserved_book(target_book.id, start_booking, end_booking)

    if reserved_book is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Book is already reserved for the selected dates'
        )

    if start_booking <= date.today() - timedelta(days=1) or end_booking <= date.today() - timedelta(days=1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dates cannot be in past')

    if start_booking + timedelta(days=30) < end_booking:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You cannot book more than a month')

    if start_booking > end_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='The end of the booking must be later than the beginning'
        )

    if end_booking <= date.today() + timedelta(2):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The reserve must be more than two days')


async def cancel_reserve_background():
    async with ReserveRepository() as repository:
        await repository.cancel_books_reserve()
