from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field

from scp_core.infrastructure.database.session import get_db
from scp_core.infrastructure.database.models import PMException

router = APIRouter(prefix="/api/governance", tags=["governance"])

class PMExceptionCreate(BaseModel):
    ticker: str
    approved_min: float
    approved_target: float
    approved_cap: float
    fiduciary_caveat: str
    is_active: bool = True

class PMExceptionResponse(PMExceptionCreate):
    id: str

@router.get("/exceptions", response_model=List[PMExceptionResponse])
def get_exceptions(db: Session = Depends(get_db)):
    """Fetch all active PM Exceptions."""
    exceptions = db.query(PMException).filter(PMException.is_active == True).all()
    return [{"id": str(e.id), "ticker": e.ticker, "approved_min": e.approved_min, "approved_target": e.approved_target, "approved_cap": e.approved_cap, "fiduciary_caveat": e.fiduciary_caveat, "is_active": e.is_active} for e in exceptions]

@router.post("/exceptions", response_model=PMExceptionResponse)
def create_or_update_exception(exception: PMExceptionCreate, db: Session = Depends(get_db)):
    """Create a new PM exception or update existing active one for a ticker."""
    existing = db.query(PMException).filter(PMException.ticker == exception.ticker, PMException.is_active == True).first()
    
    if existing:
        existing.approved_min = exception.approved_min
        existing.approved_target = exception.approved_target
        existing.approved_cap = exception.approved_cap
        existing.fiduciary_caveat = exception.fiduciary_caveat
        existing.is_active = exception.is_active
        db.commit()
        db.refresh(existing)
        return {"id": str(existing.id), **exception.model_dump()}
    else:
        new_exception = PMException(**exception.model_dump())
        db.add(new_exception)
        db.commit()
        db.refresh(new_exception)
        return {"id": str(new_exception.id), **exception.model_dump()}

@router.delete("/exceptions/{ticker}")
def delete_exception(ticker: str, db: Session = Depends(get_db)):
    """Soft delete a PM exception by setting is_active = False"""
    existing = db.query(PMException).filter(PMException.ticker == ticker, PMException.is_active == True).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Active exception not found for this ticker")
    
    existing.is_active = False
    db.commit()
    return {"status": "success", "message": f"Exception for {ticker} deactivated"}
