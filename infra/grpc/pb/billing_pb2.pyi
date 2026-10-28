from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BillingRequest(_message.Message):
    __slots__ = ("customer_id",)
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    customer_id: str
    def __init__(self, customer_id: _Optional[str] = ...) -> None: ...

class BillingResponse(_message.Message):
    __slots__ = ("customer_id", "name", "metrics")
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    customer_id: str
    name: str
    metrics: Metrics
    def __init__(self, customer_id: _Optional[str] = ..., name: _Optional[str] = ..., metrics: _Optional[_Union[Metrics, _Mapping]] = ...) -> None: ...

class Metrics(_message.Message):
    __slots__ = ("invoices_processed", "total_paid", "total_due_with_interest")
    INVOICES_PROCESSED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PAID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DUE_WITH_INTEREST_FIELD_NUMBER: _ClassVar[int]
    invoices_processed: int
    total_paid: str
    total_due_with_interest: str
    def __init__(self, invoices_processed: _Optional[int] = ..., total_paid: _Optional[str] = ..., total_due_with_interest: _Optional[str] = ...) -> None: ...

class Invoice(_message.Message):
    __slots__ = ("amount", "days_overdue", "paid", "tier")
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    DAYS_OVERDUE_FIELD_NUMBER: _ClassVar[int]
    PAID_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    amount: float
    days_overdue: int
    paid: bool
    tier: int
    def __init__(self, amount: _Optional[float] = ..., days_overdue: _Optional[int] = ..., paid: _Optional[bool] = ..., tier: _Optional[int] = ...) -> None: ...

class CalculateInvoicesRequest(_message.Message):
    __slots__ = ("invoices", "rounds")
    INVOICES_FIELD_NUMBER: _ClassVar[int]
    ROUNDS_FIELD_NUMBER: _ClassVar[int]
    invoices: _containers.RepeatedCompositeFieldContainer[Invoice]
    rounds: int
    def __init__(self, invoices: _Optional[_Iterable[_Union[Invoice, _Mapping]]] = ..., rounds: _Optional[int] = ...) -> None: ...

class CalculateInvoicesResponse(_message.Message):
    __slots__ = ("invoices_processed", "total_paid", "total_discount", "total_due_with_interest")
    INVOICES_PROCESSED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PAID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DISCOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DUE_WITH_INTEREST_FIELD_NUMBER: _ClassVar[int]
    invoices_processed: int
    total_paid: str
    total_discount: str
    total_due_with_interest: str
    def __init__(self, invoices_processed: _Optional[int] = ..., total_paid: _Optional[str] = ..., total_discount: _Optional[str] = ..., total_due_with_interest: _Optional[str] = ...) -> None: ...
