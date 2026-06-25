from typing import Dict, Any, Tuple
from scp_core.compliance.engine import ComplianceRule
import logging

logger = logging.getLogger(__name__)

class FundamentalExceptionRule(ComplianceRule):
    @property
    def rule_name(self) -> str:
        return "Fundamental Exception Limit"

    @property
    def rule_description(self) -> str:
        return "Enforces pm_exception_max ceilings when is_negative_nopat is flagged."

    def evaluate(self, trade: Dict[str, Any], portfolio: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Evaluates the trade against fundamental exceptions.
        Assumes portfolio contains a 'target_allocations' dictionary keyed by ticker,
        and 'current_weights' keyed by ticker.
        """
        ticker = trade.get('ticker')
        side = trade.get('side', '').upper()
        trade_weight = trade.get('trade_weight_impact', 0.0) # Assumes weight impact is calculated
        
        if side != 'BUY':
            return True, ""
            
        current_weight = portfolio.get('current_weights', {}).get(ticker, 0.0)
        target_allocation = portfolio.get('target_allocations', {}).get(ticker, {})
        
        is_negative_nopat = target_allocation.get('is_negative_nopat', False)
        pm_exception_max = target_allocation.get('pm_exception_max', None)
        
        if is_negative_nopat and pm_exception_max is not None:
            projected_weight = current_weight + trade_weight
            if projected_weight > pm_exception_max:
                return False, f"Trade would breach exception max of {pm_exception_max:.4f} for negative NOPAT asset {ticker}. Projected: {projected_weight:.4f}"
                
        return True, ""
