from typing import Dict, Any, Tuple
from scp_core.compliance.engine import ComplianceRule


class ESGRequirementRule(ComplianceRule):
    def __init__(self, min_esg_score: float = 50.0):
        self.min_esg_score = min_esg_score

    @property
    def rule_name(self) -> str:
        return "ESG Requirement"

    @property
    def rule_description(self) -> str:
        return f"Ensures that all purchased securities meet a minimum ESG score of {self.min_esg_score}."

    def evaluate(self, trade: Dict[str, Any], portfolio: Dict[str, Any]) -> Tuple[bool, str]:
        # If it's not a buy, it doesn't violate minimum score for purchasing
        if trade.get("quantity", 0) <= 0:
            return True, ""

        security_esg = trade.get("esg_score", None)
        if security_esg is None:
            # Depending on strictness, we might reject if ESG score is missing
            return False, f"Security {trade.get('symbol')} has no ESG score."

        if security_esg < self.min_esg_score:
            return (
                False,
                f"Security {trade.get('symbol')} ESG score {security_esg} is below the required {self.min_esg_score}.",
            )

        return True, ""


class ESGPortfolioRequirementRule(ComplianceRule):
    def __init__(self, min_portfolio_esg_score: float = 60.0):
        self.min_portfolio_esg_score = min_portfolio_esg_score

    @property
    def rule_name(self) -> str:
        return "ESG Portfolio Requirement"

    @property
    def rule_description(self) -> str:
        return f"Ensures that the portfolio's weighted average ESG score remains above {self.min_portfolio_esg_score} after the trade."

    def evaluate(self, trade: Dict[str, Any], portfolio: Dict[str, Any]) -> Tuple[bool, str]:
        positions = portfolio.get("positions", [])
        nav = portfolio.get("nav", 0.0)

        if nav == 0:
            return True, ""

        total_esg_weighted = 0.0
        total_weight = 0.0

        for pos in positions:
            pos_weight = pos.get("value", 0) / nav
            esg_score = pos.get("esg_score", 0)
            total_esg_weighted += pos_weight * esg_score
            total_weight += pos_weight

        # Add the proposed trade
        trade_value = trade.get("quantity", 0) * trade.get("price", 0)
        trade_weight = trade_value / nav
        trade_esg = trade.get("esg_score", 0)

        total_esg_weighted += trade_weight * trade_esg
        total_weight += trade_weight

        if total_weight > 0:
            projected_esg = total_esg_weighted / total_weight
            if projected_esg < self.min_portfolio_esg_score:
                return (
                    False,
                    f"Projected portfolio ESG score {projected_esg:.2f} is below required {self.min_portfolio_esg_score}.",
                )

        return True, ""
