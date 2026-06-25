import uuid
from sqlalchemy import Column, String, Float, ForeignKey, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class SystemUser(Base):
    __tablename__ = 'system_user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    role = Column(String)  # ADMIN or USER
    portfolios = relationship("Portfolio", back_populates="manager")

class Fund(Base):
    __tablename__ = 'fund'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    base_currency = Column(String)
    portfolios = relationship("Portfolio", back_populates="fund")

class Portfolio(Base):
    __tablename__ = 'portfolio'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey('fund.id'))
    manager_id = Column(UUID(as_uuid=True), ForeignKey('system_user.id'))
    strategy_name = Column(String)
    
    fund = relationship("Fund", back_populates="portfolios")
    manager = relationship("SystemUser", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio")
    orders = relationship("Order", back_populates="portfolio")

class Instrument(Base):
    __tablename__ = 'instrument'
    sec_id = Column(String, primary_key=True) # Ticker/ISIN/CUSIP
    asset_class = Column(String) # Equity/Bond/Option/Swap
    multiplier = Column(Float, default=1.0)
    
    positions = relationship("Position", back_populates="instrument")

class Position(Base):
    __tablename__ = 'position'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolio.id'))
    sec_id = Column(String, ForeignKey('instrument.sec_id'))
    total_quantity = Column(Float, default=0.0)
    average_cost = Column(Float, default=0.0)
    
    portfolio = relationship("Portfolio", back_populates="positions")
    instrument = relationship("Instrument", back_populates="positions")
    tax_lots = relationship("TaxLot", back_populates="position")

class TaxLot(Base):
    __tablename__ = 'tax_lot'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    position_id = Column(UUID(as_uuid=True), ForeignKey('position.id'))
    quantity = Column(Float)
    cost_basis = Column(Float)
    acquire_date = Column(Date)
    
    position = relationship("Position", back_populates="tax_lots")

class Order(Base):
    __tablename__ = 'order'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolio.id'))
    sec_id = Column(String, ForeignKey('instrument.sec_id'))
    side = Column(String) # BUY/SELL/SHORT
    quantity = Column(Float)
    status = Column(String) # PENDING/ROUTED/PARTIAL/FILLED
    
    portfolio = relationship("Portfolio", back_populates="orders")
    executions = relationship("Execution", back_populates="order")

class Execution(Base):
    __tablename__ = 'execution'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('order.id'))
    fill_quantity = Column(Float)
    fill_price = Column(Float)
    fill_time = Column(DateTime)
    
    order = relationship("Order", back_populates="executions")
