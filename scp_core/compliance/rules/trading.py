from typing import Dict, Any, Tuple
from scp_core.compliance.engine import ComplianceRule


class WashSaleRule(ComplianceRule):
    def __init__(self, days_window: int = 30):
        self.days_window = days_window

    @property
    def rule_name(self) -> str:
        return "Wash Sale Restriction"

    @property
    def rule_description(self) -> str:
        return f"Prevents purchasing a security that was sold at a loss within the last {self.days_window} days."

    def evaluate(self, trade: Dict[str, Any], portfolio: Dict[str, Any]) -> Tuple[bool, str]:
        if trade.get("quantity", 0) <= 0:
            return True, ""

        symbol = trade.get("symbol")
        recent_sales = portfolio.get("recent_sales", [])

        for sale in recent_sales:
            if sale.get("symbol") == symbol:
                days_since = sale.get("days_since", 0)
                is_loss = sale.get("is_loss", False)
                if days_since <= self.days_window and is_loss:
                    return (
                        False,
                        f"Wash Sale violation: {symbol} was sold at a loss {days_since} days ago (limit {self.days_window} days).",
                    )

        return True, ""


class NoShortSellingRule(ComplianceRule):
    @property
    def rule_name(self) -> str:
        return "No Short Selling"

    @property
    def rule_description(self) -> str:
        return "Prohibits any short selling. All sell orders must be covered by existing long positions."

    def evaluate(self, trade: Dict[str, Any], portfolio: Dict[str, Any]) -> Tuple[bool, str]:
        if trade.get("quantity", 0) >= 0:
            return True, ""

        symbol = trade.get("symbol")
        positions = portfolio.get("positions", [])

        current_quantity = 0.0
        for pos in positions:
            if pos.get("symbol") == symbol:
                current_quantity += pos.get("quantity", 0)

        if current_quantity + trade.get("quantity", 0) < 0:
            return (
                False,
                f"Short selling prohibited: Attempting to sell {-trade.get('quantity')} of {symbol} but only own {current_quantity}.",
            )

        return True, ""


class MaxOrderQuantityRule(ComplianceRule):
    def __init__(self, max_quantity: float):
        self.max_quantity = max_quantity

    @property
    def rule_name(self) -> str:
        return "Max Order Quantity"

    @property
    def rule_description(self) -> str:
        return f"Ensures no single order exceeds {self.max_quantity} units."

    def evaluate(self, trade: Dict[str, Any], portfolio: Dict[str, Any]) -> Tuple[bool, str]:
        quantity = abs(trade.get("quantity", 0))
        if quantity > self.max_quantity:
            return False, f"Order quantity {quantity} exceeds maximum allowed {self.max_quantity}."

        return True, ""
