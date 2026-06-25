from typing import Dict, Any, List

class ComplianceEngine:
    def __init__(self):
        # Configurable compliance thresholds
        self.SINGLE_STOCK_LIMIT_PCT = 10.0

    def evaluate_pre_trade(self, proposed_order: Dict[str, Any], current_portfolio: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Mathematically merges the proposed order with the current portfolio state 
        to check if the new position exceeds the Single Stock Concentration limit.
        """
        symbol = proposed_order.get("symbol")
        qty = float(proposed_order.get("quantity", 0))
        price = float(proposed_order.get("price", 0))
        side = proposed_order.get("side", "BUY")

        # In a real system, current_portfolio comes from the database IBOR.
        # Here we simulate the logic.
        
        total_aum = sum([float(str(p.get("value", "0")).replace('$', '').replace(',', '')) for p in current_portfolio])
        if total_aum == 0:
            total_aum = 1000000.0 # fallback

        # Calculate proposed trade value
        trade_value = qty * price
        
        # Find existing position
        existing_pos = next((p for p in current_portfolio if p.get("symbol") == symbol), None)
        current_val = float(str(existing_pos.get("value", "0")).replace('$', '').replace(',', '')) if existing_pos else 0.0

        if side == "BUY":
            new_val = current_val + trade_value
        elif side == "SELL":
            new_val = current_val - trade_value
        else:
            new_val = current_val + trade_value # Short

        # Calculate new exposure
        new_exposure_pct = (new_val / (total_aum + trade_value)) * 100

        if abs(new_exposure_pct) > self.SINGLE_STOCK_LIMIT_PCT:
            return {
                "status": "FAIL",
                "reason": f"Order violates {self.SINGLE_STOCK_LIMIT_PCT}% concentration limit. New exposure would be {new_exposure_pct:.2f}%."
            }
        
        return {
            "status": "PASS",
            "reason": "Order passes all compliance rules."
        }
