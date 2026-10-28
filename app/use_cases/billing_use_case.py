import re
from typing import Optional, Protocol

from app.errors import CustomerNotFoundError, InvalidCustomerIdError

_UUID_PATTERN = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")


class CustomerRepositoryPort(Protocol):
    async def find_by_id(self, customer_id: str) -> Optional[dict]: ...


class BillingUseCase:
    def __init__(self, customer_repository: CustomerRepositoryPort) -> None:
        self.customer_repository = customer_repository

    async def execute(self, customer_id: str) -> dict:
        if type(customer_id) is not str or _UUID_PATTERN.fullmatch(customer_id) is None:
            raise InvalidCustomerIdError()

        customer = await self.customer_repository.find_by_id(customer_id)

        if customer is None:
            raise CustomerNotFoundError()

        bills = customer["bills"]

        total_debt = 0.0
        total_paid = 0.0

        for bill in bills:
            if bill.get("paid"):
                total_paid += float(bill.get("amount", 0.0))
                continue

            amount = float(bill.get("amount", 0.0))
            days_overdue = 30
            daily_rate = 0.0033

            total_debt_with_interest = amount * ((1 + daily_rate) ** days_overdue)

            total_debt += abs(total_debt_with_interest)

        return {
            "customer_id": customer["customer_id"],
            "name": customer["name"],
            "metrics": {
                "invoices_processed": len(bills),
                "total_paid": f"{total_paid:.2f}",
                "total_due_with_interest": f"{total_debt:.2f}"
            }
        }


__all__ = ["BillingUseCase", "CustomerRepositoryPort"]