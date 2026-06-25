import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scp_core.store.db import Base
from scp_core.store.models import WorkingOrderDB, PortfolioAllocationDB, AccountAllocationDB
from scp_core.models.enums import OrderAction


@pytest.fixture
def db_session():
    # Use an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_working_order_db(db_session):
    order = WorkingOrderDB(security_sn="MSFT US", order_quantity=50.0, auto_order_type=OrderAction.BUY)
    db_session.add(order)
    db_session.commit()

    saved_order = db_session.query(WorkingOrderDB).filter_by(security_sn="MSFT US").first()
    assert saved_order is not None
    assert saved_order.order_quantity == 50.0
    assert saved_order.auto_order_type == OrderAction.BUY


def test_order_allocation_relationship(db_session):
    order = WorkingOrderDB(security_sn="GOOG US", order_quantity=200.0)
    alloc = PortfolioAllocationDB(portfolio_id=1, pre_allocation=200.0)

    acc_alloc = AccountAllocationDB(account_id=101, account_name="Main Fund", pre_allocation=200.0)

    alloc.account_allocations.append(acc_alloc)
    order.allocations.append(alloc)

    db_session.add(order)
    db_session.commit()

    saved_order = db_session.query(WorkingOrderDB).filter_by(security_sn="GOOG US").first()
    assert saved_order is not None
    assert len(saved_order.allocations) == 1

    saved_alloc = saved_order.allocations[0]
    assert saved_alloc.portfolio_id == 1
    assert len(saved_alloc.account_allocations) == 1

    saved_acc_alloc = saved_alloc.account_allocations[0]
    assert saved_acc_alloc.account_name == "Main Fund"
