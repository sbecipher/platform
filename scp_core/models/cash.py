from dataclasses import dataclass


@dataclass
class CashModeling:
    """
    Represents the modeled state of a cash position during portfolio optimization.
    Translated from PortLib.CashModeling
    """

    security_sn: str
    currency: str
    portfolio_qtty: float
    portfolio_base_ccy: float
    portfolio_percent_nav: float
    add_rem_qtty: float = 0.0
    add_rem_base_ccy: float = 0.0
    add_rem_percent_nav: float = 0.0
    target_qtty: float = 0.0
    secc_to_basc: float = 1.0  # Exchange rate to base currency

    @property
    def target_base_ccy(self) -> float:
        return self.target_qtty * self.secc_to_basc

    def aggregate(self, other: "CashModeling"):
        """Aggregates another cash modeling instance of the same currency into this one."""
        if self.currency == other.currency:
            self.portfolio_qtty += other.portfolio_qtty
            self.portfolio_base_ccy += other.portfolio_base_ccy
            self.portfolio_percent_nav += other.portfolio_percent_nav
            self.target_qtty = self.portfolio_qtty
