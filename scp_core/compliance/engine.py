from typing import List, Dict, Any, Tuple
from abc import ABC, abstractmethod


class ComplianceRule(ABC):
    @property
    @abstractmethod
    def rule_name(self) -> str:
        pass

    @property
    @abstractmethod
    def rule_description(self) -> str:
        pass

    @abstractmethod
    def evaluate(self, trade: Dict[str, Any], portfolio: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Evaluates the trade against the current portfolio.
        Returns a tuple: (is_valid: bool, error_message: str)
        """


class ComplianceRulesEngine:
    def __init__(self):
        self.rules: List[ComplianceRule] = []

    def add_rule(self, rule: ComplianceRule):
        self.rules.append(rule)

    def validate_trade(self, trade: Dict[str, Any], portfolio: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Evaluates a trade against all registered rules.
        """
        errors = []
        is_valid = True

        for rule in self.rules:
            valid, err_msg = rule.evaluate(trade, portfolio)
            if not valid:
                is_valid = False
                if err_msg:
                    errors.append(f"{rule.rule_name} Violation: {err_msg}")

        return is_valid, errors
