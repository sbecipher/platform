from scp_core.models.allocation import PortfolioAllocation, AccountAllocation
from scp_core.models.order import WorkingOrder
from scp_core.models.cash import CashModeling
from scp_core.models.enums import OrderTimeInForce, OrderAction


def test_working_order_creation():
    order = WorkingOrder(
        order_id=1,
        security_sn="AAPL US",
        order_quantity=100.0,
        time_in_force=OrderTimeInForce.GTC,
        auto_order_type=OrderAction.BUY,
    )
    assert order.order_id == 1
    assert order.security_sn == "AAPL US"
    assert order.order_quantity == 100.0
    assert order.filled_quantity == 0.0
    assert order.time_in_force == OrderTimeInForce.GTC
    assert order.auto_order_type == OrderAction.BUY


def test_cash_modeling_aggregation():
    cash1 = CashModeling(
        security_sn="USD", currency="USD", portfolio_qtty=1000.0, portfolio_base_ccy=1000.0, portfolio_percent_nav=10.0
    )
    cash2 = CashModeling(
        security_sn="USD", currency="USD", portfolio_qtty=500.0, portfolio_base_ccy=500.0, portfolio_percent_nav=5.0
    )

    cash1.aggregate(cash2)
    assert cash1.portfolio_qtty == 1500.0
    assert cash1.portfolio_base_ccy == 1500.0
    assert cash1.portfolio_percent_nav == 15.0
    assert cash1.target_qtty == 1500.0


def test_portfolio_allocation():
    alloc = PortfolioAllocation(
        portfolio_id=10,
        pre_allocation=100.0,
        account_allocations=[
            AccountAllocation(account_id=1, account_name="Acc1", pre_allocation=50.0),
            AccountAllocation(account_id=2, account_name="Acc2", pre_allocation=50.0),
        ],
    )
    assert alloc.portfolio_id == 10
    assert len(alloc.account_allocations) == 2
    assert alloc.account_allocations[0].account_name == "Acc1"
