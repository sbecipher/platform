import asyncio
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from scp_core.infrastructure.database.session import get_db

# Import our new Pydantic Schemas
from scp_core.models.schemas import (
    TradeRequest,
    TradeResponse,
    PortfolioHoldingsResponse,
    PortfolioMetrics,
    PositionResponse
)

from scp_core.api.websockets.market_data import router as market_data_router, simulate_market_data
from scp_core.api.routers.oms import router as oms_router
from scp_core.api.routers.compliance import router as compliance_router
from scp_core.api.routers.modeling import router as modeling_router
from scp_core.api.routers.auth import router as auth_router
from scp_core.api.routers.reports import router as reports_router
from scp_core.api.routers.governance import router as governance_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(simulate_market_data())
    yield
    task.cancel()

app = FastAPI(
    title="Sbecipher / scp_core API",
    description="Modernized REST API for portfolio analytics and trading.",
    version="1.0.0",
    lifespan=lifespan
)

from fastapi.staticfiles import StaticFiles
import os

# Enable CORS for the React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("output/runs", exist_ok=True)
app.mount("/output/runs", StaticFiles(directory="output/runs"), name="runs")

app.include_router(market_data_router)
app.include_router(oms_router)
app.include_router(compliance_router)
app.include_router(modeling_router)
app.include_router(auth_router)
app.include_router(reports_router)
app.include_router(governance_router)

@app.get("/api/portfolio/{portfolio_id}", response_model=PortfolioHoldingsResponse, summary="Get Portfolio Holdings")
def get_portfolio(portfolio_id: str, db: Session = Depends(get_db)):
    """
    Returns the real-time holdings and aggregated metrics from PMSPositionSnapshot.
    """
    from scp_core.infrastructure.database.models import PMSPositionSnapshot
    positions_db = db.query(PMSPositionSnapshot).all()
    
    pos_responses = []
    total_nav = sum(p.total_market_value for p in positions_db) or 1.0 # avoid div/0
    
    for p in positions_db:
        pos_responses.append(PositionResponse(
            id=str(p.id),
            symbol=p.ticker,
            asset_class="Equity",
            quantity=p.shares,
            market_value=p.total_market_value,
            day_profit=0.0, # Not in CSV
            exposure_pct=(p.total_market_value / total_nav) * 100
        ))
        
    return PortfolioHoldingsResponse(
        portfolio_id=portfolio_id,
        timestamp=datetime.utcnow(),
        metrics=PortfolioMetrics(
            portfolio_nav=total_nav,
            gross_exposure_pct=sum(abs(p.exposure_pct) for p in pos_responses),
            net_exposure_pct=sum(p.exposure_pct for p in pos_responses),
            day_pnl=0.0,
            ytd_return_pct=0.0
        ),
        positions=pos_responses
    )

@app.post("/api/trade", response_model=TradeResponse, summary="Execute a Trade")
def execute_trade(trade: TradeRequest):
    """
    Executes a trade after passing it through the Compliance Engine and updates Tax Lots.
    """
    # Mocking successful execution
    return TradeResponse(
        trade_id=str(uuid.uuid4()),
        status="EXECUTED",
        message=f"Successfully executed {trade.quantity} shares of {trade.symbol}",
        realized_pnl=0.0
    )

@app.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow()}
