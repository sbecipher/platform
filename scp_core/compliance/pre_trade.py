from typing import List, Tuple


class PreTradeCompliance:
    """
    Validates draft trades against portfolio limits and restricted lists before execution.
    """

    def __init__(
        self, restricted_list: List[str], max_gross_exposure_pct: float = 200.0, max_position_size_pct: float = 10.0
    ):
        self.restricted_list = [sym.upper() for sym in restricted_list]
        self.max_gross_exposure_pct = max_gross_exposure_pct
        self.max_position_size_pct = max_position_size_pct

    def validate_trade(
        self,
        symbol: str,
        quantity: float,
        price: float,
        current_portfolio_nav: float,
        current_gross_exposure_pct: float,
    ) -> Tuple[bool, List[str]]:
        """
        Validates a single draft trade. Returns (is_valid, list_of_errors).
        """
        errors = []
        is_valid = True

        sym_upper = symbol.upper()

        # 1. Restricted List Check
        if sym_upper in self.restricted_list:
            is_valid = False
            errors.append(f"Compliance Violation: Symbol {sym_upper} is on the restricted list.")

        # 2. Max Position Size Check
        trade_notional = abs(quantity * price)
        if current_portfolio_nav > 0:
            position_size_pct = (trade_notional / current_portfolio_nav) * 100.0
            if position_size_pct > self.max_position_size_pct:
                is_valid = False
                errors.append(
                    f"Margin Violation: Trade size ({position_size_pct:.2f}%) exceeds max single position limit of {self.max_position_size_pct}% NAV."
                )

            # 3. Max Gross Exposure Check
            projected_gross_exposure = current_gross_exposure_pct + position_size_pct
            if projected_gross_exposure > self.max_gross_exposure_pct:
                is_valid = False
                errors.append(
                    f"Margin Violation: Trade causes projected gross exposure ({projected_gross_exposure:.2f}%) to exceed limit of {self.max_gross_exposure_pct}%."
                )

        return is_valid, errors
