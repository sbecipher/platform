from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any
from .enums import OrderTimeInForce, OrderAction, CommissionCalcType, OrdersSettlementTypeEnum
from .allocation import PortfolioAllocation


@dataclass
class WorkingOrder:
    order_id: int
    security_sn: str
    order_quantity: float
    filled_quantity: float = 0.0
    average_price: float = 0.0
    trade_date: Optional[datetime] = None
    settle_date: Optional[datetime] = None
    time_in_force: OrderTimeInForce = OrderTimeInForce.DAY
    executing_broker: str = ""
    auto_order_type: OrderAction = OrderAction.BUY
    allocations: list[PortfolioAllocation] = field(default_factory=list)
    trader: str = ""
    status: int = 0
    commission_type: CommissionCalcType = CommissionCalcType.PER_SHARE
    display_commission: float = 0.0
    notes: str = ""
    settlement_type: OrdersSettlementTypeEnum = OrdersSettlementTypeEnum.REGULAR
    is_live: bool = False

    # Reference to the actual ISecurity plugin instance (from pricing layer)
    security: Optional[Any] = None
    # Reference to a TargetOrder if this order originated from a target
    target_order: Optional[Any] = None
