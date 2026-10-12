from infra.database.connection import DatabaseConnection
from infra.database.repositories.customer_repository import CustomerRepository
from app.use_cases.billing_use_case import BillingUseCase

def make_billing_use_case() -> BillingUseCase:
    pool = DatabaseConnection.get_pool()
    customer_repository = CustomerRepository(pool=pool)
    return BillingUseCase(customer_repository=customer_repository)

__all__ = ["make_billing_use_case"]