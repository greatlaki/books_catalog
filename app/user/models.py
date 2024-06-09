from sqlalchemy import String

from base.models import Base, Mapped, mapped_column


class User(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column(String(length=320), server_default='')
    last_name: Mapped[str] = mapped_column(String(length=320), server_default='')
    avatar: Mapped[str] = mapped_column(server_default='')
