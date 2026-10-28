class CustomerNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__("Customer not found")


class InvalidCustomerIdError(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid customer_id")


class InvalidRequestError(Exception):
    pass


__all__ = ["CustomerNotFoundError", "InvalidCustomerIdError", "InvalidRequestError"]

