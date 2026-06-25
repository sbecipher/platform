from enum import Enum
from typing import Dict, Any

class OrderStatus(Enum):
    PENDING = "PENDING"
    ROUTED = "ROUTED"
    PARTIAL = "PARTIAL"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    CANCELED = "CANCELED"

class OMSStateMachine:
    def __init__(self):
        # In a real system, this interacts with the database to update the order state.
        pass

    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new order in PENDING state."""
        order_data["status"] = OrderStatus.PENDING.value
        return order_data

    def route_order(self, order_id: str, broker: str) -> str:
        """
        Routes the order to a broker (NYFIX or Oppenheimer via QuickFIX wrapper).
        Transitions PENDING -> ROUTED.
        """
        # Simulate QuickFIX routing
        print(f"Routing order {order_id} to {broker} via FIX...")
        return OrderStatus.ROUTED.value

    def process_execution_report(self, order_id: str, filled_qty: float, total_qty: float) -> str:
        """
        Processes FIX execution reports.
        Transitions ROUTED -> PARTIAL or FILLED based on quantity.
        """
        if filled_qty >= total_qty:
            return OrderStatus.FILLED.value
        elif filled_qty > 0:
            return OrderStatus.PARTIAL.value
        return OrderStatus.ROUTED.value
