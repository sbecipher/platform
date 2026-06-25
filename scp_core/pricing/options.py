from .interfaces import ISecurityType, ISecurity
from typing import List, Dict, Any
from datetime import datetime
import math
import scipy.stats as si  # Requires scipy


class OptionsSecurity(ISecurity):
    """
    Instance of an Options position.
    Implements Black-Scholes-Merton option pricing and Greeks.
    """

    def __init__(
        self,
        security_id: str,
        strike: float,
        expiration_date: datetime,
        option_type: str = "Call",  # "Call" or "Put"
        contract_size: float = 100.0,
        currency: str = "USD",
    ):
        self._security_id = security_id
        self.strike = strike
        self.expiration_date = expiration_date
        self.option_type = option_type.capitalize()
        self.contract_size = contract_size
        self.currency = currency

    @property
    def security_id(self) -> str:
        return self._security_id

    def _time_to_maturity(self, settle_date: datetime) -> float:
        days = (self.expiration_date - settle_date).days
        return max(days / 365.25, 0.0001)  # Avoid division by zero

    def get_black_scholes_price(
        self,
        settle_date: datetime,
        spot_price: float,
        risk_free_rate: float,
        volatility: float,
        dividend_yield: float = 0.0,
    ) -> float:
        """
        Calculates theoretical price using Black-Scholes-Merton.
        """
        t = self._time_to_maturity(settle_date)
        d1 = (math.log(spot_price / self.strike) + (risk_free_rate - dividend_yield + 0.5 * volatility**2) * t) / (
            volatility * math.sqrt(t)
        )
        d2 = d1 - volatility * math.sqrt(t)

        if self.option_type == "Call":
            price = spot_price * math.exp(-dividend_yield * t) * si.norm.cdf(d1, 0.0, 1.0) - self.strike * math.exp(
                -risk_free_rate * t
            ) * si.norm.cdf(d2, 0.0, 1.0)
        elif self.option_type == "Put":
            price = self.strike * math.exp(-risk_free_rate * t) * si.norm.cdf(-d2, 0.0, 1.0) - spot_price * math.exp(
                -dividend_yield * t
            ) * si.norm.cdf(-d1, 0.0, 1.0)
        else:
            raise ValueError("Option type must be Call or Put")

        return price

    def get_delta(
        self,
        settle_date: datetime,
        spot_price: float,
        risk_free_rate: float,
        volatility: float,
        dividend_yield: float = 0.0,
    ) -> float:
        """
        Calculates Delta Greek.
        """
        t = self._time_to_maturity(settle_date)
        d1 = (math.log(spot_price / self.strike) + (risk_free_rate - dividend_yield + 0.5 * volatility**2) * t) / (
            volatility * math.sqrt(t)
        )

        if self.option_type == "Call":
            return math.exp(-dividend_yield * t) * si.norm.cdf(d1, 0.0, 1.0)
        else:
            return math.exp(-dividend_yield * t) * (si.norm.cdf(d1, 0.0, 1.0) - 1.0)

    def get_gamma(
        self,
        settle_date: datetime,
        spot_price: float,
        risk_free_rate: float,
        volatility: float,
        dividend_yield: float = 0.0,
    ) -> float:
        """
        Calculates Gamma Greek.
        """
        t = self._time_to_maturity(settle_date)
        d1 = (math.log(spot_price / self.strike) + (risk_free_rate - dividend_yield + 0.5 * volatility**2) * t) / (
            volatility * math.sqrt(t)
        )

        gamma = (math.exp(-dividend_yield * t) * si.norm.pdf(d1, 0.0, 1.0)) / (spot_price * volatility * math.sqrt(t))
        return gamma

    def get_vega(
        self,
        settle_date: datetime,
        spot_price: float,
        risk_free_rate: float,
        volatility: float,
        dividend_yield: float = 0.0,
    ) -> float:
        """
        Calculates Vega Greek (Value change per 1% change in vol).
        """
        t = self._time_to_maturity(settle_date)
        d1 = (math.log(spot_price / self.strike) + (risk_free_rate - dividend_yield + 0.5 * volatility**2) * t) / (
            volatility * math.sqrt(t)
        )

        vega = spot_price * math.exp(-dividend_yield * t) * si.norm.pdf(d1, 0.0, 1.0) * math.sqrt(t)
        return vega / 100.0  # Return per 1% change


class OptionsType(ISecurityType):
    """
    Standard Equity and Index Options.
    """

    @property
    def type_id(self) -> int:
        return 2

    @property
    def type_name(self) -> str:
        return "Options"

    @property
    def description(self) -> str:
        return "Derivative Options Pricing"

    @property
    def build_version(self) -> str:
        return "1.0.0"

    @property
    def default_pricing_model(self) -> str:
        return "BlackScholes"

    @property
    def contract_size(self) -> float:
        return 100.0

    @property
    def quote_size(self) -> float:
        return 1.0

    @property
    def is_fx_security(self) -> bool:
        return False

    def get_column_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "Theoretical_Price", "type": "DataType.Double"},
            {"name": "Delta", "type": "DataType.Double"},
            {"name": "Gamma", "type": "DataType.Double"},
            {"name": "Vega", "type": "DataType.Double"},
        ]

    def get_market_data_ids(self) -> List[str]:
        return ["SpotPrice", "ImpliedVolatility", "RiskFreeRate"]

    def get_new_security(self, **kwargs) -> ISecurity:
        return OptionsSecurity(**kwargs)
