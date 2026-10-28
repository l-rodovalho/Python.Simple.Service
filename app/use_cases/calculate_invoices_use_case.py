import math

from app.errors import InvalidRequestError

_BASE_DAILY_RATE = 0.0033
_TIER_DISCOUNT = (0.0, 0.02, 0.05, 0.10)
_TIER_RATE_MULT = (1.0, 0.9, 0.75, 0.6)


class CalculateInvoicesUseCase:
    def __init__(self, max_invoices: int) -> None:
        self.max_invoices = max_invoices

    def execute(self, invoices: list, rounds: int = 1) -> dict:
        if type(invoices) is not list or len(invoices) > self.max_invoices:
            raise InvalidRequestError(f"invoices must be an array with at most {self.max_invoices} items")
        if type(rounds) is float and rounds.is_integer():
            rounds = int(rounds)
        if type(rounds) is not int or rounds < 1 or rounds > 1000:
            raise InvalidRequestError("rounds must be an integer between 1 and 1000")

        total_paid = 0.0
        total_discount = 0.0
        total_due = 0.0

        for i, inv in enumerate(invoices):
            if type(inv) is not dict:
                raise InvalidRequestError(f"invoices[{i}] must be an object")
            amount = inv.get("amount")
            days = inv.get("days_overdue")
            paid = inv.get("paid")
            tier = inv.get("tier")
            if (type(amount) is not int and type(amount) is not float) or not math.isfinite(amount) or amount < 0:
                raise InvalidRequestError(f"invoices[{i}].amount must be a finite number >= 0")
            if type(days) is float and days.is_integer():
                days = int(days)
            if type(days) is not int or days < 0 or days > 365:
                raise InvalidRequestError(f"invoices[{i}].days_overdue must be an integer between 0 and 365")
            if type(paid) is not bool:
                raise InvalidRequestError(f"invoices[{i}].paid must be a boolean")
            if type(tier) is float and tier.is_integer():
                tier = int(tier)
            if type(tier) is not int or tier < 0 or tier > 3:
                raise InvalidRequestError(f"invoices[{i}].tier must be an integer between 0 and 3")

            if paid:
                discount = amount * _TIER_DISCOUNT[tier]
                total_discount += discount
                total_paid += amount - discount
                continue

            rate = _BASE_DAILY_RATE * _TIER_RATE_MULT[tier] * (1.0 + math.log1p(amount / 1000.0))
            acc = 0.0
            for r in range(rounds):
                d = days + (r % 7)
                factor = math.pow(1.0 + rate, d)
                decay = math.exp(-d / 90.0)
                interest = amount * (factor - 1.0) * (1.0 + 0.5 * decay)
                penalty = amount * 0.02 if d > 30 else 0.0
                acc += amount + interest + penalty
            total_due += acc / rounds

        return {
            "invoices_processed": len(invoices),
            "total_paid": f"{total_paid:.2f}",
            "total_discount": f"{total_discount:.2f}",
            "total_due_with_interest": f"{total_due:.2f}",
        }

