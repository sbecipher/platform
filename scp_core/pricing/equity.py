from typing import List, Dict, Any
from .interfaces import ISecurityType, ISecurity


class EquitySecurity(ISecurity):
    """
    Instance of an Equity/Stock position.
    Handles standard pricing, P&L, and dividend adjustments.
    """

    def __init__(self, security_id: str, currency: str = "USD", multiplier: float = 1.0, beta: float = 1.0):
        self._security_id = security_id
        self.currency = currency
        self.multiplier = multiplier
        self.beta = beta

    @property
    def security_id(self) -> str:
        return self._security_id

    def get_market_value(self, quantity: float, current_price: float, fx_rate: float = 1.0) -> float:
        """
        Calculates the live market value in base currency.
        """
        return quantity * current_price * self.multiplier * fx_rate

    def get_unrealized_pnl(
        self, quantity: float, average_cost: float, current_price: float, fx_rate: float = 1.0
    ) -> float:
        """
        Calculates the unrealized profit/loss.
        """
        return (current_price - average_cost) * quantity * self.multiplier * fx_rate

    def get_realized_pnl(
        self, quantity_sold: float, average_cost: float, execution_price: float, fx_rate: float = 1.0
    ) -> float:
        """
        Calculates the realized profit/loss from a sale.
        """
        return (execution_price - average_cost) * quantity_sold * self.multiplier * fx_rate

    def get_beta_adjusted_exposure(self, quantity: float, current_price: float, fx_rate: float = 1.0) -> float:
        """
        Calculates the risk-adjusted exposure using Beta.
        """
        mv = self.get_market_value(quantity, current_price, fx_rate)
        return mv * self.beta

    def apply_dividend(self, quantity: float, dividend_per_share: float, fx_rate: float = 1.0) -> float:
        """
        Calculates total cash received from a dividend payout.
        """
        return quantity * dividend_per_share * fx_rate


class EquityType(ISecurityType):
    """
    Standard Equities and Stocks.
    Equivalent to Sbecipher GeneralSecurityPlugin / SecurityPlugin.
    """

    @property
    def type_id(self) -> int:
        return 1

    @property
    def type_name(self) -> str:
        return "Equity"

    @property
    def description(self) -> str:
        return "Common Stock and Equities"

    @property
    def build_version(self) -> str:
        return "1.0.0"

    @property
    def default_pricing_model(self) -> str:
        return "DefaultEquityPricing"

    @property
    def contract_size(self) -> float:
        return 1.0

    @property
    def quote_size(self) -> float:
        return 1.0

    @property
    def is_fx_security(self) -> bool:
        return False

    def get_column_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "Market_Value", "type": "DataType.Double"},
            {"name": "Unrealized_PnL", "type": "DataType.Double"},
            {"name": "Realized_PnL", "type": "DataType.Double"},
            {"name": "Beta_Exposure", "type": "DataType.Double"},
        ]

    def get_market_data_ids(self) -> List[str]:
        return ["Price", "Beta", "DividendYield"]

    def get_new_security(self, **kwargs) -> ISecurity:
        return EquitySecurity(**kwargs)
