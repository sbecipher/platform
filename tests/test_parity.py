import pytest
from datetime import datetime
from scp_core.pricing.options import OptionsSecurity
from scp_core.pricing.irswap import IRSwapSecurity

def test_black_scholes_parity():
    """
    Tests the Python Black-Scholes implementation against known legacy values.
    """
    opt = OptionsSecurity(
        security_id="AAPL_CALL",
        strike=100.0,
        expiration_date=datetime(2027, 1, 1),
        option_type="Call"
    )
    
    # Assume settle date is exactly 1 year before expiration
    settle = datetime(2026, 1, 1)
    
    price = opt.get_black_scholes_price(
        settle_date=settle,
        spot_price=100.0,
        risk_free_rate=0.05,
        volatility=0.20,
        dividend_yield=0.0
    )
    
    # Known Black-Scholes value for S=100, K=100, T=1, r=0.05, vol=0.20 is ~10.4505
    assert round(price, 4) == 10.4505
    
    delta = opt.get_delta(settle, 100.0, 0.05, 0.20, 0.0)
    assert round(delta, 4) == 0.6368

def test_ir_swap_parity():
    """
    Tests the Python Fixed vs Float Discounting implementation.
    """
    swap = IRSwapSecurity(
        security_id="SWAP_1",
        notional=1_000_000,
        fixed_rate=0.05,
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2027, 1, 1),
        payment_freq=2 # Semi-annual
    )
    
    settle = datetime(2026, 1, 1)
    
    pv_fixed = swap.get_fixed_leg_pv(settle, discount_rate=0.04)
    
    # Cashflows: $25k in 0.5 years, $25k in 1.0 years. Discounted at 4%.
    # 25000 * e^(-0.04 * 0.5) + 25000 * e^(-0.04 * 1.0) = 24505.00 + 24019.73 = 48524.73
    assert round(pv_fixed, 2) == 48524.73
