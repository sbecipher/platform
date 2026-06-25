from typing import List, Dict, Any
from datetime import datetime, timedelta


class CashModeler:
    """
    Forecasts cash impact of proposed trades considering settlement periods.
    """

    def __init__(self, current_cash: float, settlement_rules: Dict[str, int] = None):
        self.current_cash = current_cash
        self.settlement_rules = settlement_rules or {}

    def _get_t_plus(self, asset_class: str) -> int:
        return self.settlement_rules.get(asset_class, 2)  # Default T+2

    def forecast_cash_impact(self, orders: List[Dict[str, Any]], trade_date: datetime) -> Dict[datetime, float]:
        """
        Calculates projected cash balances over time based on settlement dates.
        """
        # Daily deltas
        cash_deltas = {}

        for order in orders:
            # Assuming 'asset_class' might be injected or known, default to 2
            t_plus = self._get_t_plus(order.get("asset_class", "Equity"))
            settle_date = trade_date + timedelta(days=t_plus)

            # In a real system, you'd account for weekends/holidays
            # For simplicity, just adding calendar days here

            side_multiplier = -1 if order["side"] == "BUY" else 1
            impact = order.get("estimated_value", 0) * side_multiplier

            date_key = settle_date.date()
            if date_key not in cash_deltas:
                cash_deltas[date_key] = 0.0
            cash_deltas[date_key] += impact

        # Cumulative forecast
        forecast = {}
        sorted_dates = sorted(list(cash_deltas.keys()))
        running_cash = self.current_cash

        forecast[trade_date.date()] = running_cash

        for d in sorted_dates:
            running_cash += cash_deltas[d]
            forecast[d] = running_cash

        return forecast
