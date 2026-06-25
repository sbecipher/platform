from typing import List, Dict, Any


class ExposureCalculator:
    """
    Calculates portfolio exposure metrics including regulatory netting (UCITS, AIFMD).
    """

    @staticmethod
    def calculate_gross_exposure(positions: List[Dict[str, Any]]) -> float:
        """
        Gross Exposure = Sum of absolute market values of all positions.
        """
        return sum(abs(pos.get("market_value", 0.0)) for pos in positions)

    @staticmethod
    def calculate_net_exposure(positions: List[Dict[str, Any]]) -> float:
        """
        Net Exposure = Sum of market values of all positions (Longs - Shorts).
        """
        return sum(pos.get("market_value", 0.0) for pos in positions)

    @staticmethod
    def calculate_ucits_global_exposure(positions: List[Dict[str, Any]], portfolio_nav: float) -> float:
        """
        UCITS Global Exposure (Commitment Approach).
        Converts derivatives to equivalent underlying positions and applies netting and hedging rules.
        """
        if portfolio_nav <= 0:
            return 0.0

        total_commitment = 0.0

        # Simplified Commitment logic:
        # In full UCITS rules, opposite positions in the exact same underlying can be netted.
        # This proxy assumes pre-netted equivalent market values.
        for pos in positions:
            asset_class = pos.get("asset_class", "").lower()
            if asset_class in ["option", "future", "swap", "cfd", "cds"]:
                # Derivatives use their delta-adjusted or notional commitment
                commitment = pos.get("notional_value", 0.0) * pos.get("delta", 1.0)
                total_commitment += abs(commitment)
            else:
                # Cash securities do not typically generate incremental UCITS global exposure
                # unless they embed a derivative, but we assume pure cash here.
                pass

        return (total_commitment / portfolio_nav) * 100.0

    @staticmethod
    def calculate_aifmd_gross_exposure(positions: List[Dict[str, Any]], portfolio_nav: float) -> float:
        """
        AIFMD Gross Method: Sum of absolute values of all positions (cash and derivative equivalents),
        excluding cash and cash equivalents.
        """
        if portfolio_nav <= 0:
            return 0.0

        aifmd_gross = 0.0
        for pos in positions:
            asset_class = pos.get("asset_class", "").lower()
            if "cash" in asset_class:
                continue

            if asset_class in ["option", "future", "swap", "cfd", "cds"]:
                val = abs(pos.get("notional_value", 0.0) * pos.get("delta", 1.0))
            else:
                val = abs(pos.get("market_value", 0.0))

            aifmd_gross += val

        return (aifmd_gross / portfolio_nav) * 100.0

    @staticmethod
    def calculate_aifmd_commitment_exposure(positions: List[Dict[str, Any]], portfolio_nav: float) -> float:
        """
        AIFMD Commitment Method: Similar to Gross but allows for netting and hedging.
        This simplified version assumes input 'positions' are already grouped and netted by underlying.
        """
        if portfolio_nav <= 0:
            return 0.0

        # Proxy: net exposure of netted positions + non-cash absolute
        # A fully accurate AIFMD commitment requires exact hedge pairing logic.
        netted_sum = 0.0
        for pos in positions:
            asset_class = pos.get("asset_class", "").lower()
            if "cash" in asset_class:
                continue

            if asset_class in ["option", "future", "swap", "cfd", "cds"]:
                val = pos.get("notional_value", 0.0) * pos.get("delta", 1.0)
            else:
                val = pos.get("market_value", 0.0)

            netted_sum += abs(val)  # If positions are pre-netted by underlying

        return (netted_sum / portfolio_nav) * 100.0
