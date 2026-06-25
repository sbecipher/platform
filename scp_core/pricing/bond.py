from typing import List, Dict, Any
from datetime import datetime
from .interfaces import ISecurityType, ISecurity


class BondSecurity(ISecurity):
    """
    Instance of a bond position. Ported from BondData.cs and BondsPricingModel.cs.
    Implements standard Fixed Income mathematical modeling.
    """

    def __init__(
        self,
        security_id: str,
        maturity_date: datetime,
        issue_date: datetime,
        coupon: float,
        coupon_freq: int,
        redemption: float = 100.0,
        currency: str = "USD",
    ):
        self._security_id = security_id
        self.maturity_date = maturity_date
        self.issue_date = issue_date
        self.coupon = coupon / 100.0 if coupon > 1 else coupon  # store as decimal
        self.coupon_freq = coupon_freq if coupon_freq > 0 else 2  # Default semi-annual
        self.redemption = redemption
        self.currency = currency

    @property
    def security_id(self) -> str:
        return self._security_id

    def _years_to_maturity(self, settle_date: datetime) -> float:
        days = (self.maturity_date - settle_date).days
        return days / 365.25

    def get_price_from_yield(self, settle_date: datetime, ytm: float) -> float:
        """
        Ported from Bonds.BondPrice. Calculates Present Value of cashflows.
        """
        if settle_date >= self.maturity_date:
            return self.redemption

        t = self._years_to_maturity(settle_date)
        periods = t * self.coupon_freq
        r = ytm / self.coupon_freq

        if r == 0:
            return self.redemption + (self.coupon * self.redemption * t)

        # Standard bond pricing formula
        pv_coupons = (self.coupon * self.redemption / self.coupon_freq) * (1 - (1 + r) ** (-periods)) / r
        pv_principal = self.redemption / (1 + r) ** periods

        return pv_coupons + pv_principal

    def get_yield_from_price(self, settle_date: datetime, price: float, tolerance=1e-6, max_iter=100) -> float:
        """
        Ported from Bonds.BondYield. Uses Newton-Raphson to solve for YTM.
        """
        if settle_date >= self.maturity_date:
            return 0.0

        # Initial guess (Current Yield)
        ytm = self.coupon if price == self.redemption else (self.coupon * self.redemption) / price

        for _ in range(max_iter):
            p_calc = self.get_price_from_yield(settle_date, ytm)
            diff = p_calc - price
            if abs(diff) < tolerance:
                return ytm

            # Approximate derivative
            p_up = self.get_price_from_yield(settle_date, ytm + 0.0001)
            p_down = self.get_price_from_yield(settle_date, ytm - 0.0001)
            derivative = (p_up - p_down) / 0.0002

            if derivative == 0:
                break
            ytm -= diff / derivative

        return ytm

    def get_current_yield(self, price: float) -> float:
        """
        Ported from PSCOutputValue.CURRENT_YIELD calculation in BondsPricingModel.cs
        """
        if price == 0:
            raise ValueError("Cannot calculate current yield with zero price.")
        return (self.coupon * self.redemption) / price

    def get_modified_duration(self, settle_date: datetime, ytm: float) -> float:
        """
        Ported from Bonds.BondModifiedDuration.
        """
        t = self._years_to_maturity(settle_date)
        periods = t * self.coupon_freq
        r = ytm / self.coupon_freq

        if r == 0:
            return t

        pv_coupons = (self.coupon * self.redemption / self.coupon_freq) * (1 - (1 + r) ** (-periods)) / r
        pv_principal = self.redemption / (1 + r) ** periods
        price = pv_coupons + pv_principal

        # Macaulay Duration approximation
        macaulay = (1 + r) / r - (1 + r + periods * (self.coupon / self.coupon_freq - r)) / (
            r * ((1 + r) ** periods - 1) + self.coupon / self.coupon_freq
        )

        modified_duration = macaulay / (1 + r)
        return modified_duration

    def get_pvbp(self, settle_date: datetime, ytm: float) -> float:
        """
        Ported from PSCOutputValue.PVBP calculation.
        Present Value of a Basis Point (CR01).
        """
        price_up = self.get_price_from_yield(settle_date, ytm + 0.0001)
        price_down = self.get_price_from_yield(settle_date, ytm - 0.0001)
        return (price_down - price_up) / 2.0


class BondType(ISecurityType):
    """
    Auto-ported from BondPlugin (BondType.cs)
    """

    @property
    def type_id(self) -> int:
        return 6

    @property
    def type_name(self) -> str:
        return "Bond"

    @property
    def description(self) -> str:
        return "Corporate and Government Bonds"

    @property
    def build_version(self) -> str:
        return "1.0.0"

    @property
    def default_pricing_model(self) -> str:
        return "PSC.PricingModel.Bonds"

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
            {"name": "Yield_To_Maturity", "type": "DataType.Double"},
            {"name": "Modified_Duration", "type": "DataType.Double"},
            {"name": "PVBP", "type": "DataType.Double"},
        ]

    def get_market_data_ids(self) -> List[str]:
        return ["Yield", "Price"]

    def get_new_security(self, **kwargs) -> ISecurity:
        return BondSecurity(**kwargs)
