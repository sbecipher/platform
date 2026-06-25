import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid
from contextlib import asynccontextmanager

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

# Enable CORS for the React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_data_router)
app.include_router(oms_router)
app.include_router(compliance_router)
app.include_router(modeling_router)
app.include_router(auth_router)

@app.get("/api/portfolio/{portfolio_id}", response_model=PortfolioHoldingsResponse, summary="Get Portfolio Holdings")
def get_portfolio(portfolio_id: str):
    """
    Returns the real-time holdings and aggregated metrics for the requested portfolio.
    This replaces the legacy `DashboardTable.cs` binding logic.
    """
    # Mocked Response matching the Pydantic schema
    return PortfolioHoldingsResponse(
        portfolio_id=portfolio_id,
        timestamp=datetime.utcnow(),
        metrics=PortfolioMetrics(
            portfolio_nav=1000000.0,
            gross_exposure_pct=110.5,
            net_exposure_pct=85.0,
            day_pnl=4500.0,
            ytd_return_pct=12.4
        ),
        positions=[
            PositionResponse(
                id=str(uuid.uuid4()),
                symbol="AAPL",
                asset_class="Equity",
                quantity=1500,
                market_value=225000.0,
                day_profit=1500.0,
                exposure_pct=22.5
            )
        ]
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
