from infra.database.repositories.customer_repository import CustomerRepository
import json

class BillingUseCase:
    def __init__(self, customer_repository: CustomerRepository) -> None:
        self.customer_repository = customer_repository

    async def execute(self, customer_id: str) -> dict:
        customer = await self.customer_repository.find_by_id(customer_id)

        if not customer:
            raise Exception("Customer not found")

        address_data = customer.get("endereco_cobranca", {})
        address_data = json.loads(address_data)
        bills = address_data.get("billingHistory", [])

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
            "customer_id": str(customer.get("cd_cliente")),
            "name": customer.get("nome"),
            "metrics": {
                "invoices_processed": len(bills),
                "total_paid": f"{total_paid:.2f}",
                "total_due_with_interest": f"{total_debt:.2f}"
            }
        }


__all__ = ["BillingUseCase"]