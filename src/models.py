from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)


class User(SQLAlchemyBaseUserTable[int], Base):
    username: Mapped[str] = mapped_column(nullable=False)


class Currency(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    symbol: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)


class Account(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    note: Mapped[str] = mapped_column(nullable=True)
    summ: Mapped[float] = mapped_column(default=0)
    is_savings_account: Mapped[bool] = mapped_column(default=0)
    image_url: Mapped[str] = mapped_column(nullable=True)
    fk_currency_id: Mapped[int] = mapped_column(ForeignKey('currency.id'), nullable=False)
    fk_user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)


class SavingsAccount(Base):
    target: Mapped[float] = mapped_column(nullable=False)
    fk_account_id: Mapped[int] = mapped_column(ForeignKey('account.id'), nullable=False)


class Category(Base):
    name: Mapped[str] = mapped_column(nullable=False, unique=False)
    image_url: Mapped[str] = mapped_column(nullable=True)
    fk_currency_id: Mapped[int] = mapped_column(ForeignKey('currency.id'), nullable=False)
    fk_user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)


class SubCategory(Base):
    name: Mapped[str] = mapped_column(nullable=False, unique=False)
    fk_category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False)


class Operation(Base):
    summ: Mapped[float]
    time_date: Mapped[datetime] = mapped_column(default=datetime.now())
    type: Mapped[bool]
    note: Mapped[str] = mapped_column(nullable=True)
    fk_account_id: Mapped[int] = mapped_column(ForeignKey('account.id'), nullable=False)
    fk_category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False)
    fk_sub_category_id: Mapped[int] = mapped_column(ForeignKey('subcategory.id'), nullable=True)
    fk_user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
