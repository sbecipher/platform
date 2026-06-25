import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PMSIngestionEngine:
    def __init__(self, db_session=None):
        self.db = db_session

    def ingest_csv(self, file_path: str):
        """
        Reads the pms_upload_positions.csv and syncs it with PMSPositionSnapshot
        """
        logger.info(f"Ingesting PMS snapshot from {file_path}")
        try:
            df = pd.read_csv(file_path)
            
            # If we have a DB session, we clear the old snapshot for this date and insert
            if self.db:
                from scp_core.infrastructure.database.models import PMSPositionSnapshot
                
                # We assume all rows in the CSV have the same as_of_date
                if not df.empty:
                    snapshot_date_str = df.iloc[0]['as_of_date']
                    snapshot_date = datetime.strptime(str(snapshot_date_str), '%Y-%m-%d').date()
                    
                    # Delete old snapshot for this date
                    self.db.query(PMSPositionSnapshot).filter(PMSPositionSnapshot.as_of_date == snapshot_date).delete()
                    
                    for _, row in df.iterrows():
                        snapshot = PMSPositionSnapshot(
                            ticker=row['ticker'],
                            as_of_date=datetime.strptime(str(row['as_of_date']), '%Y-%m-%d').date(),
                            current_weight=float(row['current_weight']),
                            current_notional_usd=float(row['current_notional_usd']),
                            latest_price=float(row['latest_price']),
                            implementation_gap=float(row['implementation_gap']),
                            band_status=row['band_status'],
                            daily_return=float(row['daily_return']),
                            daily_return_contribution=float(row['daily_return_contribution']),
                            governance_monitor_status=row['governance_monitor_status']
                        )
                        self.db.add(snapshot)
                    self.db.commit()
                
            logger.info(f"Successfully processed {len(df)} rows from PMS feed.")
            return True, len(df)
            
        except Exception as e:
            logger.error(f"Failed to ingest PMS feed: {str(e)}")
            return False, str(e)

if __name__ == "__main__":
    # Test script locally
    engine = PMSIngestionEngine()
    engine.ingest_csv("pms_upload_positions.csv")
