from aiohttp import web

from infra.http.controllers.health_http_controller import HealthHttpController
from infra.http.controllers.customer_http_controller import CustomerHttpController
from infra.http.controllers.invoice_http_controller import InvoiceHttpController
from app.use_cases.billing_use_case import BillingUseCase
from app.use_cases.calculate_invoices_use_case import CalculateInvoicesUseCase


def setup_http_routes(
    app: web.Application,
    billing_use_case: BillingUseCase,
    calculate_invoices_use_case: CalculateInvoicesUseCase,
) -> None:
    health_http_controller = HealthHttpController()
    customer_http_controller = CustomerHttpController(billing_use_case)
    invoice_http_controller = InvoiceHttpController(calculate_invoices_use_case)
    
    app.router.add_get("/health", health_http_controller.get_health)
    app.router.add_post("/billing/{customer_id}", customer_http_controller.process_billing)
    app.router.add_post("/invoices/calculate", invoice_http_controller.calculate)


__all__ = ["setup_http_routes"]