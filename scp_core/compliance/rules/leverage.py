from typing import Dict, Any, Tuple
from scp_core.compliance.engine import ComplianceRule


class MaxLeverageRule(ComplianceRule):
    def __init__(self, max_gross_leverage: float = 2.0):
        self.max_gross_leverage = max_gross_leverage

    @property
    def rule_name(self) -> str:
        return "Maximum Gross Leverage"

    @property
    def rule_description(self) -> str:
        return (
            f"Ensures the portfolio gross leverage (Gross Exposure / NAV) does not exceed {self.max_gross_leverage}x."
        )

    def evaluate(self, trade: Dict[str, Any], portfolio: Dict[str, Any]) -> Tuple[bool, str]:
        nav = portfolio.get("nav", 0.0)
        if nav == 0:
            return True, ""

        positions = portfolio.get("positions", [])

        # Calculate current gross exposure
        current_gross_exposure = 0.0
        for pos in positions:
            current_gross_exposure += abs(pos.get("value", 0))

        # Add proposed trade
        trade_value = abs(trade.get("quantity", 0) * trade.get("price", 0))
        projected_gross_exposure = current_gross_exposure + trade_value

        projected_leverage = projected_gross_exposure / nav

        if projected_leverage > self.max_gross_leverage:
            return (
                False,
                f"Projected gross leverage {projected_leverage:.2f}x exceeds maximum allowed {self.max_gross_leverage}x.",
            )

        return True, ""


class CashLimitRule(ComplianceRule):
    def __init__(self, min_cash_pct: float = 2.0):
        self.min_cash_pct = min_cash_pct

    @property
    def rule_name(self) -> str:
        return "Minimum Cash Limit"

    @property
    def rule_description(self) -> str:
        return f"Ensures the portfolio maintains a minimum cash balance of {self.min_cash_pct}% of NAV."

    def evaluate(self, trade: Dict[str, Any], portfolio: Dict[str, Any]) -> Tuple[bool, str]:
        nav = portfolio.get("nav", 0.0)
        if nav == 0:
            return True, ""

        current_cash = portfolio.get("cash", 0.0)

        # Calculate cash impact (buying reduces cash, selling increases it)
        trade_cash_impact = -(trade.get("quantity", 0) * trade.get("price", 0))

        projected_cash = current_cash + trade_cash_impact
        projected_cash_pct = (projected_cash / nav) * 100.0

        if projected_cash_pct < self.min_cash_pct:
            return (
                False,
                f"Projected cash balance {projected_cash_pct:.2f}% falls below required minimum {self.min_cash_pct}%.",
            )

        return True, ""
