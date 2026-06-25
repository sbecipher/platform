from typing import List, Dict, Any


class RebalanceEngine:
    """
    Takes target values from the allocator and converts them into
    executable order quantities based on current market prices.
    """

    def __init__(self, current_prices: Dict[str, float]):
        self.current_prices = current_prices

    def generate_orders(self, target_adjustments: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """
        Converts diff_values into order quantities.
        Returns a list of dicts: {'symbol': str, 'side': str, 'quantity': float, 'limit_price': float}
        """
        orders = []

        for symbol, data in target_adjustments.items():
            diff_value = data.get("diff_value", 0.0)

            if abs(diff_value) < 1.0:  # Skip immaterial adjustments
                continue

            price = self.current_prices.get(symbol)
            if not price or price <= 0:
                # Log error or raise
                continue

            qty_to_trade = diff_value / price

            # Simple rounding to whole shares
            qty_to_trade = round(qty_to_trade)

            if qty_to_trade == 0:
                continue

            side = "BUY" if qty_to_trade > 0 else "SELL"

            orders.append(
                {
                    "symbol": symbol,
                    "side": side,
                    "quantity": abs(qty_to_trade),
                    "limit_price": price,
                    "estimated_value": qty_to_trade * price,
                }
            )

        return orders
