from typing import Dict, Any


class PortfolioAllocator:
    """
    Computes target exposures and positions based on a model.
    Models can target percentage of NAV or Beta-adjusted exposure.
    """

    def __init__(self, portfolio: Dict[str, Any]):
        self.portfolio = portfolio
        self.nav = portfolio.get("nav", 0.0)
        self.positions = portfolio.get("positions", [])

    def calculate_target_by_nav_pct(self, targets: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """
        Given a dictionary of symbol -> target % of NAV,
        returns the target values in currency and the difference from current.
        """
        result = {}

        current_exposures = {pos["symbol"]: pos.get("value", 0.0) for pos in self.positions}

        for symbol, target_pct in targets.items():
            target_value = (target_pct / 100.0) * self.nav
            current_val = current_exposures.get(symbol, 0.0)

            result[symbol] = {
                "target_pct": target_pct,
                "target_value": target_value,
                "current_value": current_val,
                "diff_value": target_value - current_val,
            }

        return result

    def calculate_target_by_beta(
        self, target_beta: float, symbol_betas: Dict[str, float]
    ) -> Dict[str, Dict[str, float]]:
        """
        Given a target portfolio beta and the beta of each symbol, calculates necessary
        adjustments (simplified implementation that scales existing portfolio).
        """
        # Calculate current portfolio beta
        total_beta_weighted = 0.0
        current_exposures = {}

        for pos in self.positions:
            sym = pos.get("symbol")
            val = pos.get("value", 0.0)
            current_exposures[sym] = val
            weight = val / self.nav if self.nav > 0 else 0

            beta = symbol_betas.get(sym, 1.0)
            total_beta_weighted += weight * beta

        if total_beta_weighted == 0:
            scale_factor = 1.0
        else:
            scale_factor = target_beta / total_beta_weighted

        result = {}
        for sym, val in current_exposures.items():
            target_value = val * scale_factor
            result[sym] = {
                "target_value": target_value,
                "current_value": val,
                "diff_value": target_value - val,
                "assumed_beta": symbol_betas.get(sym, 1.0),
            }

        return result
