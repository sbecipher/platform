from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from scp_core.domain.compliance.engine import ComplianceEngine
from scp_core.api.dependencies.auth import get_current_user
from fastapi import Depends

router = APIRouter(prefix="/api/compliance", tags=["Compliance"])

compliance_engine = ComplianceEngine()

class ComplianceRequest(BaseModel):
    order: Dict[str, Any]
    portfolio: List[Dict[str, Any]]

@router.post("/simulate")
def simulate_compliance(payload: ComplianceRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Runs pre-trade compliance mathematically evaluating the new order against current holdings.
    """
    result = compliance_engine.evaluate_pre_trade(payload.order, payload.portfolio)
    return result
