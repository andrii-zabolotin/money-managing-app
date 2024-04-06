from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)


class User(SQLAlchemyBaseUserTable[int], Base):
    username: Mapped[str] = mapped_column(nullable=False)


class Currency(Base):
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class Account(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    note: Mapped[str]
    summ: Mapped[float] = mapped_column(default=0)
    is_savings_account: Mapped[bool] = mapped_column(default=0)
    image_url: Mapped[str]
    fk_currency_id: Mapped[int] = mapped_column(ForeignKey('currency.id'), nullable=False)
    fk_user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)


class SavingsAccount(Base):
    target: Mapped[float] = mapped_column(nullable=False)
    fk_account_id: Mapped[int] = mapped_column(ForeignKey('account.id'), nullable=False)


class Category(Base):
    name: Mapped[str] = mapped_column(nullable=False, unique=False)
    image_url: Mapped[str]
    fk_currency_id: Mapped[int] = mapped_column(ForeignKey('currency.id'), nullable=False)
    fk_user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)


class SubCategory(Base):
    name: Mapped[str] = mapped_column(nullable=False, unique=False)
    fk_category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False)
