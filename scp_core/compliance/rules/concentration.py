from typing import Dict, Any, Tuple
from scp_core.compliance.engine import ComplianceRule


class SingleIssuerRestrictionRule(ComplianceRule):
    def __init__(self, max_exposure_pct: float = 5.0):
        self.max_exposure_pct = max_exposure_pct

    @property
    def rule_name(self) -> str:
        return "Single Issuer Concentration"

    @property
    def rule_description(self) -> str:
        return f"Ensures that exposure to a single issuer does not exceed {self.max_exposure_pct}% of NAV."

    def evaluate(self, trade: Dict[str, Any], portfolio: Dict[str, Any]) -> Tuple[bool, str]:
        issuer = trade.get("issuer", None)
        if not issuer:
            return True, ""

        nav = portfolio.get("nav", 0.0)
        if nav == 0:
            return True, ""

        positions = portfolio.get("positions", [])

        # Calculate current exposure to this issuer
        current_issuer_exposure = 0.0
        for pos in positions:
            if pos.get("issuer") == issuer:
                current_issuer_exposure += pos.get("value", 0)

        # Add proposed trade
        trade_value = trade.get("quantity", 0) * trade.get("price", 0)
        projected_exposure = current_issuer_exposure + trade_value

        projected_pct = (projected_exposure / nav) * 100.0

        if projected_pct > self.max_exposure_pct:
            return (
                False,
                f"Projected exposure to issuer {issuer} ({projected_pct:.2f}%) exceeds limit of {self.max_exposure_pct}%.",
            )

        return True, ""


class SectorExposureRule(ComplianceRule):
    def __init__(self, sector: str, max_exposure_pct: float):
        self.sector = sector
        self.max_exposure_pct = max_exposure_pct

    @property
    def rule_name(self) -> str:
        return f"Sector Exposure ({self.sector})"

    @property
    def rule_description(self) -> str:
        return f"Ensures that exposure to the {self.sector} sector does not exceed {self.max_exposure_pct}% of NAV."

    def evaluate(self, trade: Dict[str, Any], portfolio: Dict[str, Any]) -> Tuple[bool, str]:
        trade_sector = trade.get("sector", None)
        if trade_sector != self.sector:
            return True, ""

        nav = portfolio.get("nav", 0.0)
        if nav == 0:
            return True, ""

        positions = portfolio.get("positions", [])

        current_sector_exposure = 0.0
        for pos in positions:
            if pos.get("sector") == self.sector:
                current_sector_exposure += pos.get("value", 0)

        trade_value = trade.get("quantity", 0) * trade.get("price", 0)
        projected_exposure = current_sector_exposure + trade_value

        projected_pct = (projected_exposure / nav) * 100.0

        if projected_pct > self.max_exposure_pct:
            return (
                False,
                f"Projected exposure to sector {self.sector} ({projected_pct:.2f}%) exceeds limit of {self.max_exposure_pct}%.",
            )

        return True, ""
