import pytest
from scp_core.compliance.engine import ComplianceRulesEngine
from scp_core.compliance.rules.esg import ESGRequirementRule, ESGPortfolioRequirementRule
from scp_core.compliance.rules.trading import WashSaleRule

@pytest.fixture
def base_portfolio():
    return {
        'nav': 100000.0,
        'cash': 20000.0,
        'positions': [
            {'symbol': 'AAPL', 'quantity': 100, 'value': 15000.0, 'esg_score': 65.0, 'sector': 'Technology'},
            {'symbol': 'MSFT', 'quantity': 50, 'value': 15000.0, 'esg_score': 70.0, 'sector': 'Technology'}
        ],
        'recent_sales': [
            {'symbol': 'TSLA', 'days_since': 15, 'is_loss': True}
        ]
    }

def test_esg_requirement_rule(base_portfolio):
    engine = ComplianceRulesEngine()
    engine.add_rule(ESGRequirementRule(min_esg_score=50.0))
    
    # Valid trade
    trade_valid = {'symbol': 'GOOG', 'quantity': 10, 'price': 100.0, 'esg_score': 60.0}
    is_valid, errs = engine.validate_trade(trade_valid, base_portfolio)
    assert is_valid
    
    # Invalid trade
    trade_invalid = {'symbol': 'BAD_CO', 'quantity': 10, 'price': 100.0, 'esg_score': 30.0}
    is_valid, errs = engine.validate_trade(trade_invalid, base_portfolio)
    assert not is_valid
    assert "ESG Requirement Violation" in errs[0]

def test_wash_sale_rule(base_portfolio):
    engine = ComplianceRulesEngine()
    engine.add_rule(WashSaleRule(days_window=30))
    
    # Invalid trade - TSLA was sold at a loss 15 days ago
    trade = {'symbol': 'TSLA', 'quantity': 10, 'price': 200.0}
    is_valid, errs = engine.validate_trade(trade, base_portfolio)
    assert not is_valid
    assert "Wash Sale Restriction Violation" in errs[0]
