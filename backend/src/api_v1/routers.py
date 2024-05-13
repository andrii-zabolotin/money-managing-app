from src.api_v1.account import router as router_account
from src.api_v1.currency import router as router_currency
from src.api_v1.category import router as router_category
from src.api_v1.operation import router as router_operation
from src.api_v1.savings_account import router as router_savings_account
from backend.src.api_v1.sub_category import router as router_sub_category

all_routers = [
    router_account,
    router_currency,
    router_category,
    router_operation,
    router_savings_account,
    router_sub_category,
]
