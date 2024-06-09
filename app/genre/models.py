from sqlalchemy.orm import relationship

from base.models import Base, Mapped, mapped_column


class Genre(Base):
    __tablename__ = 'genres'

    genre: Mapped[str] = mapped_column(nullable=False, unique=True)

    books: Mapped[list['Book']] = relationship(secondary='m2m_subjects_categories', back_populates='genres')
