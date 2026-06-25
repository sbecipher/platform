from .interfaces import ISecurityType, ISecurity
from typing import List, Dict, Any
from datetime import datetime
import math


class IRSwapSecurity(ISecurity):
    """
    Instance of an Interest Rate Swap (IRSwap).
    Implements Fixed vs Floating leg present value discounting.
    """

    def __init__(
        self,
        security_id: str,
        notional: float,
        fixed_rate: float,
        start_date: datetime,
        end_date: datetime,
        payment_freq: int = 2,
        currency: str = "USD",
    ):
        self._security_id = security_id
        self.notional = notional
        self.fixed_rate = fixed_rate
        self.start_date = start_date
        self.end_date = end_date
        self.payment_freq = payment_freq
        self.currency = currency

    @property
    def security_id(self) -> str:
        return self._security_id

    def _years_to_maturity(self, settle_date: datetime) -> float:
        days = (self.end_date - settle_date).days
        return max(days / 365.25, 0.0)

    def get_fixed_leg_pv(self, settle_date: datetime, discount_rate: float) -> float:
        """
        Present Value of the fixed leg cash flows.
        """
        t = self._years_to_maturity(settle_date)
        if t <= 0:
            return 0.0

        periods = int(t * self.payment_freq)
        dt = 1.0 / self.payment_freq
        pv = 0.0

        for i in range(1, periods + 1):
            time_to_payment = i * dt
            cash_flow = self.notional * self.fixed_rate * dt
            pv += cash_flow * math.exp(-discount_rate * time_to_payment)

        return pv

    def get_floating_leg_pv(self, settle_date: datetime, forward_rates: List[float], discount_rate: float) -> float:
        """
        Present Value of the floating leg cash flows.
        Assume we have a list of projected forward rates for each period.
        """
        t = self._years_to_maturity(settle_date)
        if t <= 0:
            return 0.0

        periods = int(t * self.payment_freq)
        dt = 1.0 / self.payment_freq
        pv = 0.0

        for i in range(min(periods, len(forward_rates))):
            time_to_payment = (i + 1) * dt
            # The floating cash flow is driven by the forward rate
            cash_flow = self.notional * forward_rates[i] * dt
            pv += cash_flow * math.exp(-discount_rate * time_to_payment)

        return pv

    def get_net_present_value(
        self, settle_date: datetime, discount_rate: float, forward_rates: List[float], is_payer: bool = True
    ) -> float:
        """
        Net Present Value (NPV) of the swap.
        Payer pays fixed, receives floating. Receiver pays floating, receives fixed.
        """
        pv_fixed = self.get_fixed_leg_pv(settle_date, discount_rate)
        pv_float = self.get_floating_leg_pv(settle_date, forward_rates, discount_rate)

        if is_payer:
            return pv_float - pv_fixed
        else:
            return pv_fixed - pv_float


class IRSwapType(ISecurityType):
    """
    Interest Rate Swaps.
    """

    @property
    def type_id(self) -> int:
        return 4

    @property
    def type_name(self) -> str:
        return "IRSwap"

    @property
    def description(self) -> str:
        return "Interest Rate Swap Valuation"

    @property
    def build_version(self) -> str:
        return "1.0.0"

    @property
    def default_pricing_model(self) -> str:
        return "DiscountedCashFlow"

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
            {"name": "NPV", "type": "DataType.Double"},
            {"name": "Fixed_Leg_PV", "type": "DataType.Double"},
            {"name": "Float_Leg_PV", "type": "DataType.Double"},
        ]

    def get_market_data_ids(self) -> List[str]:
        return ["DiscountRate", "ForwardCurve"]

    def get_new_security(self, **kwargs) -> ISecurity:
        return IRSwapSecurity(**kwargs)
