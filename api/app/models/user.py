from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from api.app.models.base import Base, CreatedAtMixin


class User(Base, CreatedAtMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
