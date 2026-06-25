from typing import List, Dict, Any
from datetime import datetime, timedelta
from .interfaces import ISecurityType, ISecurity


class CashSecurity(ISecurity):
    """
    Instance of a cash position. Ported from CashData.cs.
    """

    def __init__(self, currency: str, settle_currency: str = "USD"):
        self.currency = currency
        self._settle_currency = settle_currency

    @property
    def security_id(self) -> str:
        return f"CASH {self.currency}"

    @property
    def settle_currency(self) -> str:
        return self._settle_currency

    @settle_currency.setter
    def settle_currency(self, val: str):
        self._settle_currency = val

    def get_average_price_dec_places(self) -> int:
        return 15

    def get_long_short(self, trade_date: datetime, price: float) -> int:
        return 0

    def calculate_effective_trade_price(self, price: float, market_convention: bool, fx_rate: float) -> float:
        """
        Ported from CalculateEffectiveTradePrice.
        Assuming 'fx_rate' is provided by the pricing engine context.
        """
        if market_convention:
            # Replaces host.ConvertFromFXConvention
            return price / fx_rate if fx_rate else price
        return price

    def get_settle_date(self, trade_date: datetime, days_to_settle: int, is_settlement_day_func) -> datetime:
        """
        Ported from GetSettleDate.
        is_settlement_day_func is a callable resolving calendar holidays.
        """
        if days_to_settle == 0:
            return trade_date

        current_date = trade_date
        while days_to_settle > 0:
            current_date += timedelta(days=1)
            # Resolve against calendars
            flag_currency = is_settlement_day_func(current_date, self.currency)
            flag_settle = is_settlement_day_func(current_date, self._settle_currency)

            if (
                days_to_settle > 1
                and (self.currency == "USD" or flag_currency)
                and (self._settle_currency == "USD" or flag_settle)
            ) or (days_to_settle == 1 and flag_currency and flag_settle):
                days_to_settle -= 1

        return current_date


class CashType(ISecurityType):
    """
    Auto-ported from CashPlugin
    """

    @property
    def type_id(self) -> int:
        return 0

    @property
    def type_name(self) -> str:
        return "Cash"

    @property
    def description(self) -> str:
        return "Cash balance"

    @property
    def build_version(self) -> str:
        return "1.0.0"

    @property
    def default_pricing_model(self) -> str:
        return "Default"

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
        return [{"name": "Text", "type": "DataType.Text"}]

    def get_market_data_ids(self) -> List[str]:
        return ["FX_ID"]

    def get_new_security(self, currency: str) -> ISecurity:
        return CashSecurity(currency=currency)
