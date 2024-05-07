from abc import ABC, abstractmethod
from typing import Type

from src.database import SessionLocal
from src.repositories.account import AccountRepository
from src.repositories.category import CategoryRepository
from src.repositories.currency import CurrencyRepository
from src.repositories.operation import OperationRepository
from src.repositories.savings_account import SavingsAccountRepository
from src.repositories.sub_category import SubCategoryRepository


class IUnitOfWork(ABC):
    account: Type[AccountRepository]
    category: Type[CategoryRepository]
    currency: Type[CurrencyRepository]
    operation: Type[OperationRepository]
    savings_account: Type[SavingsAccountRepository]
    sub_category: Type[SubCategoryRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = SessionLocal

    async def __aenter__(self):
        self.session = self.session_factory()

        self.account = AccountRepository(self.session)
        self.category = CategoryRepository(self.session)
        self.currency = CurrencyRepository(self.session)
        self.operation = OperationRepository(self.session)
        self.savings_account = SavingsAccountRepository(self.session)
        self.sub_category = SubCategoryRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
