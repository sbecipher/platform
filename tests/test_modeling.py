import pytest
from datetime import datetime
from scp_core.portfolio.modeling.allocator import PortfolioAllocator
from scp_core.portfolio.modeling.rebalance import RebalanceEngine
from scp_core.portfolio.modeling.cash_modeling import CashModeler

@pytest.fixture
def base_portfolio():
    return {
        'nav': 100000.0,
        'positions': [
            {'symbol': 'AAPL', 'quantity': 100, 'value': 15000.0},
            {'symbol': 'MSFT', 'quantity': 50, 'value': 15000.0}
        ]
    }

def test_portfolio_allocator_by_nav(base_portfolio):
    allocator = PortfolioAllocator(base_portfolio)
    
    targets = {
        'AAPL': 20.0,  # Target 20% = $20,000 (diff = +$5,000)
        'MSFT': 10.0,  # Target 10% = $10,000 (diff = -$5,000)
        'GOOG': 5.0    # Target 5%  = $5,000  (diff = +$5,000)
    }
    
    result = allocator.calculate_target_by_nav_pct(targets)
    
    assert result['AAPL']['diff_value'] == 5000.0
    assert result['MSFT']['diff_value'] == -5000.0
    assert result['GOOG']['diff_value'] == 5000.0

def test_rebalance_engine():
    current_prices = {
        'AAPL': 150.0,
        'MSFT': 300.0,
        'GOOG': 1000.0
    }
    
    engine = RebalanceEngine(current_prices)
    
    adjustments = {
        'AAPL': {'diff_value': 4500.0},
        'MSFT': {'diff_value': -3000.0},
        'GOOG': {'diff_value': 5000.0}
    }
    
    orders = engine.generate_orders(adjustments)
    
    # AAPL: 4500 / 150 = 30 shares BUY
    # MSFT: -3000 / 300 = 10 shares SELL
    # GOOG: 5000 / 1000 = 5 shares BUY
    
    assert len(orders) == 3
    for order in orders:
        if order['symbol'] == 'AAPL':
            assert order['side'] == 'BUY'
            assert order['quantity'] == 30
        elif order['symbol'] == 'MSFT':
            assert order['side'] == 'SELL'
            assert order['quantity'] == 10

def test_cash_modeling():
    orders = [
        {'symbol': 'AAPL', 'side': 'BUY', 'estimated_value': 5000.0, 'asset_class': 'Equity'},
        {'symbol': 'MSFT', 'side': 'SELL', 'estimated_value': 3000.0, 'asset_class': 'Equity'}
    ]
    
    trade_date = datetime(2026, 6, 25)
    modeler = CashModeler(current_cash=20000.0)
    
    forecast = modeler.forecast_cash_impact(orders, trade_date)
    
    # Settle date should be trade_date + 2 days = June 27
    settle_date = trade_date.date()
    from datetime import timedelta
    t_plus_2 = (trade_date + timedelta(days=2)).date()
    
    # Initially cash is 20,000
    assert forecast[trade_date.date()] == 20000.0
    
    # On T+2, net impact is -5000 + 3000 = -2000. Cash becomes 18,000
    assert forecast[t_plus_2] == 18000.0
