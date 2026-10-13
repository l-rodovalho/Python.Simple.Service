from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
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
