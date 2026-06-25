from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from scp_core.domain.modeling.rebalance import RebalancingEngine
from scp_core.api.dependencies.auth import get_current_user
from fastapi import Depends

router = APIRouter(prefix="/api/modeling", tags=["Modeling"])

engine = RebalancingEngine()

class RebalanceRequest(BaseModel):
    portfolio: List[Dict[str, Any]]
    target_weights: Dict[str, float]

@router.post("/rebalance")
def generate_rebalance_orders(payload: RebalanceRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Analyzes the current portfolio against target weights and generates whole-share orders.
    """
    orders = engine.generate_target_orders(payload.portfolio, payload.target_weights)
    return {"status": "SUCCESS", "orders": orders}
