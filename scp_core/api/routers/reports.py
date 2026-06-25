from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Depends, Response
import shutil
import os
import tempfile
from sqlalchemy.orm import Session
from scp_core.infrastructure.storage.artifact_store import ArtifactStore
from scp_core.feeds.pms_ingestion import PMSIngestionEngine
from scp_core.infrastructure.database.session import get_db
from scp_core.domain.reporting.context_builder import ReportingContextBuilder

router = APIRouter(prefix="/api/reports", tags=["reports"])
artifact_store = ArtifactStore()

@router.post("/runs/ingest")
async def ingest_run(run_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Ingests a ZIP file containing the output artifacts of a quant diligence run.
    """
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Must be a ZIP file.")
        
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
        
    try:
        run_root = artifact_store.store_run_archive(run_id, tmp_path)
        return {"status": "success", "run_id": run_id, "run_root": run_root}
    finally:
        os.unlink(tmp_path)

@router.post("/pms/upload")
async def upload_pms_snapshot(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Uploads the daily pms_upload_positions.csv snapshot and triggers ingestion.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Must be a CSV file.")
        
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
        
    try:
        engine = PMSIngestionEngine(db_session=db)
        success, result = engine.ingest_csv(tmp_path)
        if not success:
            raise HTTPException(status_code=500, detail=f"Ingestion failed: {result}")
        return {"status": "success", "rows_processed": result}
    finally:
        os.unlink(tmp_path)

@router.get("/pms/daily")
async def generate_daily_pms_monitor(db: Session = Depends(get_db)):
    """
    Generates the daily PMS markdown report.
    """
    builder = ReportingContextBuilder(db_session=db)
    markdown = builder.generate_pms_monitor()
    return {
        "status": "success",
        "markdown_content": markdown
    }

@router.get("/pms/daily/pdf")
async def generate_daily_pms_monitor_pdf(db: Session = Depends(get_db)):
    """
    Generates the daily PMS report as a downloadable PDF.
    """
    builder = ReportingContextBuilder(db_session=db)
    markdown = builder.generate_pms_monitor()
    pdf_bytes = builder.generate_pdf_from_markdown(markdown)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=pms_daily_monitor.pdf"})

@router.get("/{run_id}/markdown")
async def generate_lp_diligence_brief(run_id: str, db: Session = Depends(get_db)):
    """
    Generates the LP Due-Diligence brief based on the given run_id.
    """
    builder = ReportingContextBuilder(db_session=db)
    markdown = builder.generate_lp_brief(run_id)
    return {
        "status": "success",
        "markdown_content": markdown
    }

@router.get("/{run_id}/pdf")
async def generate_lp_diligence_brief_pdf(run_id: str, db: Session = Depends(get_db)):
    """
    Generates the LP Due-Diligence brief as a downloadable PDF.
    """
    builder = ReportingContextBuilder(db_session=db)
    markdown = builder.generate_lp_brief(run_id)
    pdf_bytes = builder.generate_pdf_from_markdown(markdown)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=lp_brief_{run_id}.pdf"})
