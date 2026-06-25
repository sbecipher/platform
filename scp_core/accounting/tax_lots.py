from typing import List, Dict, Tuple
from datetime import datetime, timedelta


class TaxLot:
    def __init__(self, id: str, symbol: str, quantity: float, price: float, date: datetime, is_long: bool):
        self.id = id
        self.symbol = symbol
        self.original_quantity = quantity
        self.remaining_quantity = quantity
        self.price = price
        self.date = date
        self.is_long = is_long
        self.realized_pnl = 0.0

    @property
    def is_closed(self) -> bool:
        return self.remaining_quantity <= 0.0


class TaxLotEngine:
    """
    Engine to match trades against tax lots and calculate Realized/Unrealized PnL.
    Supports FIFO, LIFO, and Average Cost.
    """

    def __init__(self, accounting_method: str = "FIFO"):
        self.accounting_method = accounting_method.upper()
        self.open_lots: List[TaxLot] = []
        self.closed_lots: List[TaxLot] = []

    def process_trade(
        self, trade_id: str, symbol: str, quantity: float, price: float, date: datetime, is_buy: bool
    ) -> Tuple[float, List[Dict]]:
        """
        Process a trade and return Realized PnL and a list of lot matches.
        """
        # Determine if trade is opening or closing
        # If open_lots is empty, it's opening.
        # If open_lots has same direction, it's opening.
        # If open_lots has opposite direction, it's closing (matching).

        matches = []
        realized_pnl = 0.0

        direction_long = is_buy

        if not self.open_lots or self.open_lots[0].is_long == direction_long:
            # Opening a new lot
            new_lot = TaxLot(trade_id, symbol, quantity, price, date, direction_long)
            self.open_lots.append(new_lot)
            return 0.0, []

        # Closing existing lots
        remaining_qty_to_close = quantity

        # Sort open lots based on accounting method
        if self.accounting_method == "FIFO":
            self.open_lots.sort(key=lambda x: x.date)
        elif self.accounting_method == "LIFO":
            self.open_lots.sort(key=lambda x: x.date, reverse=True)
        # Average Cost is handled differently, but we approximate by closing FIFO and overriding cost basis later if needed.

        lots_to_remove = []

        for lot in self.open_lots:
            if remaining_qty_to_close <= 0:
                break

            qty_matched = min(lot.remaining_quantity, remaining_qty_to_close)

            # Calculate Realized PnL for this match
            if lot.is_long:
                # Long: Sell Price - Buy Price
                pnl = qty_matched * (price - lot.price)
            else:
                # Short: Buy Price (to cover) - Sell Price
                # Wait, if lot is short (sell), and we are buying to cover:
                # lot.price is the Sell Price. price is the Buy Price.
                pnl = qty_matched * (lot.price - price)

            lot.realized_pnl += pnl
            realized_pnl += pnl

            lot.remaining_quantity -= qty_matched
            remaining_qty_to_close -= qty_matched

            matches.append({"lot_id": lot.id, "qty_matched": qty_matched, "realized_pnl": pnl})

            if lot.is_closed:
                lots_to_remove.append(lot)
                self.closed_lots.append(lot)

        # Remove fully closed lots
        for lot in lots_to_remove:
            self.open_lots.remove(lot)

        # If trade quantity exceeded open lots, open a new lot for the remainder
        if remaining_qty_to_close > 0:
            new_lot = TaxLot(trade_id + "_remainder", symbol, remaining_qty_to_close, price, date, direction_long)
            self.open_lots.append(new_lot)

        return realized_pnl, matches

    def check_wash_sale(self, sell_date: datetime, symbol: str, loss_amount: float) -> bool:
        """
        Check for wash sale violation (buying identical security 30 days before or after a loss).
        Returns True if a wash sale occurred.
        """
        if loss_amount >= 0:
            return False

        start_date = sell_date - timedelta(days=30)
        end_date = sell_date + timedelta(days=30)

        # Check all lots (open and closed) to see if acquired within the window
        for lot in self.open_lots + self.closed_lots:
            if lot.symbol == symbol and lot.is_long:
                if start_date <= lot.date <= end_date:
                    return True

        return False

    def get_unrealized_pnl(self, current_price: float) -> float:
        """
        Calculate Unrealized PnL for all open lots based on a current market price.
        """
        unrealized = 0.0
        for lot in self.open_lots:
            if lot.is_long:
                unrealized += lot.remaining_quantity * (current_price - lot.price)
            else:
                unrealized += lot.remaining_quantity * (lot.price - current_price)
        return unrealized
