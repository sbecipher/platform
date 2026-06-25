from typing import List, Dict, Any


class PnlCalculator:
    """
    Calculates portfolio-level Daily and Month-to-Date (MTD) PnL metrics.
    """

    @staticmethod
    def calculate_daily_pnl(positions: List[Dict[str, Any]]) -> float:
        """
        Sum of Day Profit for all positions.
        """
        return sum(pos.get("day_profit", 0.0) for pos in positions)

    @staticmethod
    def calculate_mtd_pnl(positions: List[Dict[str, Any]]) -> float:
        """
        Sum of MTD Profit for all positions.
        """
        return sum(pos.get("mtd_profit", 0.0) for pos in positions)

    @staticmethod
    def calculate_pnl_bps(pnl_amount: float, portfolio_nav: float) -> float:
        """
        Convert a PnL absolute amount to Basis Points (BPS) of the Portfolio NAV.
        """
        if portfolio_nav <= 0:
            return 0.0
        return (pnl_amount / portfolio_nav) * 10000.0
