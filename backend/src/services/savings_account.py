from src.schemas.savings_account import SavingsAccountCreate
from src.utils.unitofwork import IUnitOfWork


class SavingsAccountService:
    @classmethod
    async def add(cls, uow: IUnitOfWork, account_in: SavingsAccountCreate, user_id: int):
        async with uow:
            data_in = account_in.model_dump()

            account_values = data_in.pop("account")
            account = await uow.account.add(values=account_values, user_id=user_id)
            account.is_savings_account = True

            savings_values = data_in
            savings_values["fk_account_id"] = account.id
            savings_account = await uow.savings_account.add(values=savings_values)

            await uow.commit()
            return savings_account

    @classmethod
    async def delete(cls, uow: IUnitOfWork, object_id: int, user_id: int):
        async with uow:
            get_result = await uow.savings_account.get(model_object_id=object_id, user_id=user_id)
            account_id = get_result.fk_account_id
            if account_id:
                await uow.savings_account.delete(model_object_id=object_id)
                await uow.account.delete(model_object_id=account_id, user_id=user_id)
                await uow.commit()
