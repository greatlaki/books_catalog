from sqlalchemy import String
from sqlalchemy.orm import relationship

from base.models import Base, Mapped, mapped_column
from book.models import Book


class User(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column(String(length=320), server_default='')
    last_name: Mapped[str] = mapped_column(String(length=320), server_default='')
    avatar: Mapped[str] = mapped_column(server_default='')

    books: Mapped[list[Book]] = relationship(back_populates='author')
