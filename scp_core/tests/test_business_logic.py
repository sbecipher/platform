import pandas as pd
import numpy as np
from datetime import datetime
from scp_core.analytics.performance import (
    calculate_cumulative_return,
    calculate_sharpe_ratio,
)
from scp_core.accounting.tax_lots import TaxLotEngine
from scp_core.compliance.pre_trade import PreTradeCompliance


def test_cumulative_return():
    returns = pd.Series([0.01, 0.02, -0.01, 0.015])
    # (1.01) * (1.02) * (0.99) * (1.015) - 1 = 0.03519647
    cum = calculate_cumulative_return(returns)
    assert np.isclose(cum, 0.03519647)


def test_sharpe_ratio():
    returns = pd.Series([0.01, 0.02, -0.01, 0.015, 0.005, -0.002])
    sharpe = calculate_sharpe_ratio(returns, risk_free_rate=0.0)
    assert sharpe > 0


def test_tax_lots_fifo():
    engine = TaxLotEngine(accounting_method="FIFO")
    # Buy 100 @ 10
    engine.process_trade("t1", "AAPL", 100, 10.0, datetime(2023, 1, 1), is_buy=True)
    # Buy 50 @ 12
    engine.process_trade("t2", "AAPL", 50, 12.0, datetime(2023, 1, 2), is_buy=True)

    # Sell 120 @ 15
    # Should close out t1 (100 @ 10) -> realized = 100 * (15 - 10) = 500
    # Should close 20 of t2 (20 @ 12) -> realized = 20 * (15 - 12) = 60
    # Total realized = 560
    pnl, matches = engine.process_trade("t3", "AAPL", 120, 15.0, datetime(2023, 1, 3), is_buy=False)

    assert pnl == 560.0
    assert len(engine.open_lots) == 1
    assert engine.open_lots[0].remaining_quantity == 30.0


def test_compliance_restricted_list():
    comp = PreTradeCompliance(restricted_list=["GME", "AMC"])
    is_valid, errors = comp.validate_trade("GME", 100, 50, 100000, 50)
    assert not is_valid
    assert "restricted list" in errors[0]


def test_compliance_margin():
    comp = PreTradeCompliance(restricted_list=[], max_position_size_pct=10.0)
    # Trade is $20k, NAV is $100k -> 20%
    is_valid, errors = comp.validate_trade("AAPL", 100, 200, 100000, 50)
    assert not is_valid
    assert "exceeds max single position limit" in errors[0]
