from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class SystemUserSchema(BaseSchema):
    id: UUID
    username: str
    role: str

class FundSchema(BaseSchema):
    id: UUID
    name: str
    base_currency: str

class InstrumentSchema(BaseSchema):
    sec_id: str
    asset_class: str
    multiplier: float

class TaxLotSchema(BaseSchema):
    id: UUID
    position_id: UUID
    quantity: float
    cost_basis: float
    acquire_date: date

class PositionSchema(BaseSchema):
    id: UUID
    portfolio_id: UUID
    sec_id: str
    total_quantity: float
    average_cost: float
    tax_lots: Optional[List[TaxLotSchema]] = []

class OrderSchema(BaseSchema):
    id: UUID
    portfolio_id: UUID
    sec_id: str
    side: str
    quantity: float
    status: str

class ExecutionSchema(BaseSchema):
    id: UUID
    order_id: UUID
    fill_quantity: float
    fill_price: float
    fill_time: datetime

class PortfolioSchema(BaseSchema):
    id: UUID
    fund_id: UUID
    manager_id: Optional[UUID] = None
    strategy_name: str
    positions: Optional[List[PositionSchema]] = []
    orders: Optional[List[OrderSchema]] = []
