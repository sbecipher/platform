from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PositionBase(BaseModel):
    symbol: str
    asset_class: str
    quantity: float
    market_value: float
    latest_price: float = 0.0
    day_profit: Optional[float] = 0.0
    mtd_profit: Optional[float] = 0.0

class PositionResponse(PositionBase):
    id: str
    exposure_pct: Optional[float] = None
    
    class Config:
        from_attributes = True

class PortfolioMetrics(BaseModel):
    portfolio_nav: float
    gross_exposure_pct: float
    net_exposure_pct: float
    day_pnl: float
    ytd_return_pct: Optional[float] = None

class PortfolioHoldingsResponse(BaseModel):
    portfolio_id: str
    timestamp: datetime
    metrics: PortfolioMetrics
    positions: List[PositionResponse]

class TradeRequest(BaseModel):
    symbol: str = Field(..., description="Ticker symbol of the asset")
    quantity: float = Field(..., description="Number of shares/contracts")
    price: float = Field(..., description="Execution price")
    is_buy: bool = Field(..., description="True for Buy, False for Sell")
    portfolio_id: str

class TradeResponse(BaseModel):
    trade_id: str
    status: str
    message: str
    realized_pnl: Optional[float] = None
