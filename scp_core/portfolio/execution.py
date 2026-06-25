from typing import Dict, List
from .messaging_auto import ExecutionReportDTO, CancelRejectDTO
from ..models.enums import OrderStatusEnum
from ..models.allocation import WorkingOrder


class OrderManager:
    """
    State machine ported from PortLib API.
    Handles the lifecycle of orders by consuming incoming FIX messages.
    """

    def __init__(self):
        self.active_orders: Dict[str, WorkingOrder] = {}
        self.execution_history: List[ExecutionReportDTO] = []

    def register_order(self, order: WorkingOrder):
        """Registers a new outbound working order."""
        self.active_orders[order.order_id] = order

    def process_execution_report(self, exec_report: ExecutionReportDTO) -> bool:
        """
        Consumes an execution report and updates internal state safely.
        Returns True if successful.
        """
        self.execution_history.append(exec_report)

        if exec_report.order_id not in self.active_orders:
            print(f"Warning: Received execution for unknown order {exec_report.order_id}")
            return False

        order = self.active_orders[exec_report.order_id]

        # State machine transition validation
        if order.status in [OrderStatusEnum.FILLED, OrderStatusEnum.CANCELED, OrderStatusEnum.REJECTED]:
            if exec_report.order_status not in [OrderStatusEnum.BUSTED, OrderStatusEnum.CORRECTED]:
                print(f"Error: Invalid transition. Order {order.order_id} is already terminal ({order.status}).")
                return False

        # Apply state changes
        order.status = exec_report.order_status
        order.filled_quantity = exec_report.filled_quantity
        order.leaves_quantity = exec_report.leaves_quantity

        if exec_report.last_price > 0:
            order.avg_price = exec_report.avg_price

        return True

    def process_cancel_reject(self, cancel_reject: CancelRejectDTO) -> bool:
        """
        Handles scenarios where a broker rejects our cancel request.
        """
        if cancel_reject.orig_cl_ord_id not in self.active_orders:
            return False

        order = self.active_orders[cancel_reject.orig_cl_ord_id]
        print(f"Cancel Reject received for order {order.order_id}: {cancel_reject.text}")

        # Typically the order reverts to its previous active state
        return True
