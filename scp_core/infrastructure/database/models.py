import uuid
from sqlalchemy import Column, String, Float, ForeignKey, Date, DateTime, Boolean
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
    diligence_runs = relationship("DiligenceRun", back_populates="portfolio")

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

class DiligenceRun(Base):
    __tablename__ = 'diligence_run'
    run_id = Column(String, primary_key=True)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolio.id'))
    run_date = Column(DateTime)
    strategy_type = Column(String)
    status = Column(String)
    
    portfolio = relationship("Portfolio", back_populates="diligence_runs")
    artifacts = relationship("RunArtifact", back_populates="run")

class RunArtifact(Base):
    __tablename__ = 'run_artifact'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(String, ForeignKey('diligence_run.run_id'))
    source_key = Column(String)
    file_path = Column(String)
    file_type = Column(String)
    
    run = relationship("DiligenceRun", back_populates="artifacts")

class PMException(Base):
    __tablename__ = 'pm_exception'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker = Column(String)
    approved_min = Column(Float)
    approved_target = Column(Float)
    approved_cap = Column(Float)
    fiduciary_caveat = Column(String)
    is_active = Column(Boolean)

class TargetAllocation(Base):
    __tablename__ = 'target_allocation'
    ticker = Column(String(20), primary_key=True)
    target_weight = Column(Float, nullable=False)
    pm_exception_min = Column(Float, nullable=True)
    pm_exception_max = Column(Float, nullable=True)
    is_negative_nopat = Column(Boolean, default=False)
    caveat_text = Column(String, nullable=True)

class PMSPositionSnapshot(Base):
    __tablename__ = 'pms_position_snapshot'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker = Column(String(20))
    as_of_date = Column(Date)
    current_weight = Column(Float)
    implementation_gap = Column(Float)
    band_status = Column(String)
    daily_return = Column(Float)
    governance_monitor_status = Column(String)
