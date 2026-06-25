from celery import Celery
import os
from datetime import datetime
from .refinitiv_feed import RefinitivFeed

# Configure Celery using Redis as the broker and backend
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("scp_core_workers", broker=REDIS_URL, backend=REDIS_URL)

# Optional configuration settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    worker_concurrency=4,  # Process thousands of prices in parallel
)

from celery.schedules import crontab

# Configure Celery Beat to run a snapshot at 4:00 PM EST (21:00 UTC) every weekday
celery_app.conf.beat_schedule = {
    "daily-eod-snapshot": {
        "task": "execute_daily_snapshot",
        "schedule": crontab(hour=21, minute=0, day_of_week="1-5"),
        "args": (),
    },
}

# Global instance for the worker to reuse
_feed_client = None


def get_feed_client():
    global _feed_client
    if _feed_client is None:
        _feed_client = RefinitivFeed(session_name="celery_background_worker")
    return _feed_client


@celery_app.task(name="process_market_tick")
def process_market_tick(security_id: str, price: float, timestamp: str):
    """
    Asynchronously processes an incoming streaming price tick.
    Instead of blocking the main FastAPI thread, this worker:
    1. Grabs the tick from Redis
    2. Recalculates the specific Asset's P&L and Greeks
    3. Saves the updated values back to the PostgreSQL database
    """
    print(f"[{timestamp}] Processing tick for {security_id}: {price}")

    # In reality, this would fetch the PositionDB from SQLAlchemy,
    # invoke the proper Pricing logic (e.g. BlackScholes or Bond PVBP),
    # and update the database.

    # Example pseudo-code for the flow:
    # db = next(get_db())
    # position = db.query(PositionDB).filter_by(security_id=security_id).first()
    # position.current_market_value = security_model.get_market_value(position.quantity, price)
    # db.commit()

    return {"status": "success", "security_id": security_id, "processed_price": price}


@celery_app.task(name="execute_daily_snapshot")
def execute_daily_snapshot():
    """
    Cron job triggered at End-of-Day.
    Queries all Portfolios in the database, runs the full Risk and Pricing pipeline,
    and inserts a new row into PortfolioSnapshotDB for historical charting.
    """
    print(f"[{datetime.now().isoformat()}] Executing EOD Daily Snapshot...")
    # 1. db = next(get_db())
    # 2. portfolios = db.query(PortfolioDB).all()
    # 3. For each portfolio, grab positions, run RiskAnalytics.calculate_historical_var
    # 4. snapshot = PortfolioSnapshotDB(total_nav=..., var_99=...)
    # 5. db.add(snapshot); db.commit()
    return {"status": "success", "message": "EOD Snapshots recorded."}
