from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid

from scp_core.domain.execution.state_machine import OMSStateMachine
from scp_core.domain.compliance.engine import ComplianceEngine
from scp_core.api.dependencies.auth import get_current_user
from fastapi import Depends

router = APIRouter(prefix="/api/oms", tags=["OMS"])

oms_engine = OMSStateMachine()

class OrderPayload(BaseModel):
    symbol: str
    side: str
    quantity: float
    order_type: str
    price: float
    broker: str

@router.post("/route")
def route_order(payload: OrderPayload, current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Simulates routing an order via QuickFIX to NYFIX or Oppenheimer.
    """
    order_id = f"ORD-{str(uuid.uuid4())[:8]}"
    
    # 1. Create order in PENDING
    order_dict = oms_engine.create_order(payload.model_dump())
    
    # 2. Route order to broker
    new_status = oms_engine.route_order(order_id, payload.broker)
    order_dict["status"] = new_status
    order_dict["order_id"] = order_id
    
    return {
        "message": f"Order {order_id} successfully routed to {payload.broker}.",
        "order": order_dict
    }
