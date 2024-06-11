from datetime import date

from sqlalchemy import DECIMAL, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from base.models import Base, Mapped, mapped_column


class Book(Base):
    __tablename__ = 'books'

    name: Mapped[str] = mapped_column(String(length=320), index=True, nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    page_count: Mapped[int] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.id', ondelete='CASCADE'), nullable=False)

    author: Mapped['User'] = relationship(back_populates='books')
    genres: Mapped[list['Genre']] = relationship(secondary='m2m_books_genres', back_populates='books')


class Reserve(Base):
    __tablename__ = 'reserves'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    booked_at: Mapped[date] = mapped_column()
    due_date: Mapped[date] = mapped_column()

    user: Mapped[int] = relationship('User')
    book: Mapped[int] = relationship('Book')


class M2MBookGenre(Base):
    __tablename__ = 'm2m_books_genres'

    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.id'))

    __table_args__ = (UniqueConstraint('book_id', 'genre_id'),)
