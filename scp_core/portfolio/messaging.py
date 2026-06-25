from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
from ..models.enums import OrderStatusEnum, OrderSideEnum


@dataclass
class TradeLeg:
    symbol: str
    side: OrderSideEnum
    currency: str
    quantity: float
    filled_quantity: float
    leg_allocs: Dict[str, float] = field(default_factory=dict)
    settle_date: Optional[datetime] = None
    last_price: float = 0.0


@dataclass
class ExecutionReport:
    """
    Ported from SerializableExecReport.cs.
    Represents a FIX Execution Report (MsgType=8).
    """

    exec_id: str
    order_id: str
    exec_trans_type: str  # e.g., 'New', 'Cancel', 'Correct'
    exec_type: str  # e.g., 'Fill', 'Partial Fill', 'Rejected'
    order_status: OrderStatusEnum

    symbol: str
    side: OrderSideEnum

    order_quantity: float
    filled_quantity: float
    leaves_quantity: float

    last_price: float = 0.0
    last_quantity: float = 0.0
    avg_price: float = 0.0

    broker_id: str = ""
    account: str = ""
    currency: str = ""
    settle_currency: str = ""

    transact_time: Optional[datetime] = None
    trade_date: Optional[datetime] = None
    settle_date: Optional[datetime] = None

    commission: float = 0.0
    net_money: float = 0.0
    gross_trade_amt: float = 0.0
    accrued_interest_amt: float = 0.0

    text: str = ""  # FIX Tag 58 (Reject reason or notes)

    legs: List[TradeLeg] = field(default_factory=list)


@dataclass
class CancelReject:
    """
    Ported from SerializableCancelReject.cs.
    Represents a FIX Order Cancel Reject (MsgType=9).
    """

    order_id: str
    cl_ord_id: str
    orig_cl_ord_id: str
    order_status: OrderStatusEnum
    cxl_rej_response_to: str  # 'Cancel', 'Replace'
    cxl_rej_reason: int  # FIX Tag 102
    text: str = ""
    transact_time: Optional[datetime] = None


@dataclass
class AllocationAck:
    """
    Ported from SerializableAllocationACK.cs
    Represents a FIX Allocation Instruction ACK (MsgType=P).
    """

    alloc_id: str
    trade_date: datetime
    transact_time: datetime
    alloc_status: int  # FIX Tag 87
    alloc_rej_code: Optional[int] = None
    text: str = ""
