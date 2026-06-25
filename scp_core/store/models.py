from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .db import Base
from ..models.enums import OrderTimeInForce, OrderAction, CommissionCalcType, OrdersSettlementTypeEnum


class AccountAllocationDB(Base):
    __tablename__ = "account_allocations"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_allocation_id = Column(Integer, ForeignKey("portfolio_allocations.id"))
    account_id = Column(Integer, index=True)
    account_name = Column(String(255))
    pre_allocation = Column(Float, default=0.0)
    filled_allocation = Column(Float, default=0.0)
    todays_allocation = Column(Float, default=0.0)
    include = Column(Boolean, default=True)

    portfolio_allocation = relationship("PortfolioAllocationDB", back_populates="account_allocations")


class PortfolioAllocationDB(Base):
    __tablename__ = "portfolio_allocations"

    id = Column(Integer, primary_key=True, index=True)
    working_order_id = Column(Integer, ForeignKey("working_orders.id"))
    portfolio_id = Column(Integer, index=True)
    pre_allocation = Column(Float, default=0.0)
    filled_allocation = Column(Float, default=0.0)
    todays_allocation = Column(Float, default=0.0)
    include = Column(Boolean, default=True)

    working_order = relationship("WorkingOrderDB", back_populates="allocations")
    account_allocations = relationship("AccountAllocationDB", back_populates="portfolio_allocation")


class WorkingOrderDB(Base):
    __tablename__ = "working_orders"

    id = Column(Integer, primary_key=True, index=True)
    security_sn = Column(String(255), index=True)
    order_quantity = Column(Float, nullable=False)
    filled_quantity = Column(Float, default=0.0)
    average_price = Column(Float, default=0.0)
    trade_date = Column(DateTime, nullable=True)
    settle_date = Column(DateTime, nullable=True)
    time_in_force = Column(SQLEnum(OrderTimeInForce), default=OrderTimeInForce.DAY)
    executing_broker = Column(String(255), default="")
    auto_order_type = Column(SQLEnum(OrderAction), default=OrderAction.BUY)
    trader = Column(String(255), default="")
    status = Column(Integer, default=0)
    commission_type = Column(SQLEnum(CommissionCalcType), default=CommissionCalcType.PER_SHARE)
    display_commission = Column(Float, default=0.0)
    notes = Column(String(1024), default="")
    settlement_type = Column(SQLEnum(OrdersSettlementTypeEnum), default=OrdersSettlementTypeEnum.REGULAR)
    is_live = Column(Boolean, default=False)

    allocations = relationship("PortfolioAllocationDB", back_populates="working_order")


class PortfolioDB(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    base_currency = Column(String(3), default="USD")
    created_at = Column(DateTime, default=None)  # Normally func.now()

    snapshots = relationship("PortfolioSnapshotDB", back_populates="portfolio")


class PortfolioSnapshotDB(Base):
    """
    Stores End-of-Day (EOD) metrics to track performance history.
    """

    __tablename__ = "portfolio_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    snapshot_date = Column(DateTime, nullable=False, index=True)

    total_nav = Column(Float, nullable=False)
    daily_pnl = Column(Float, default=0.0)
    daily_return_pct = Column(Float, default=0.0)
    var_99 = Column(Float, default=0.0)

    portfolio = relationship("PortfolioDB", back_populates="snapshots")
