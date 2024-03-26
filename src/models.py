from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)


class User(SQLAlchemyBaseUserTable[int], Base):
    username: Mapped[str] = mapped_column(nullable=False)
