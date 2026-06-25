import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os
import logging
from pathlib import Path
from sqlalchemy.orm import Session
import markdown

logger = logging.getLogger(__name__)

class ReportingContextBuilder:
    def __init__(self, db_session: Session = None, template_dir: str = "scp_core/domain/reporting/templates"):
        self.db = db_session
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_pms_monitor(self) -> str:
        """
        Queries the DB for the latest snapshot, builds the context, and renders the Markdown.
        """
        # MVP: query PMSPositionSnapshot, mock nav if needed
        context = {
            "run_id": "monitor-integration-pms-upload",
            "as_of_date": "2026-06-24", # Mock for MVP if DB is empty
            "nav": "1,786,855.67",
            "daily_return": "-1.70%",
            "mtd_return": "-6.15%",
            "qtd_return": "12.17%",
            "ytd_return": "17.21%",
            "alerts_total": 0,
            "alerts_critical": 0,
            "drawdown_alert": False,
            "informational_statuses": []
        }
        
        if self.db:
            try:
                from scp_core.infrastructure.database.models import PMSPositionSnapshot
                from sqlalchemy.exc import OperationalError
                # Get latest date
                latest = self.db.query(PMSPositionSnapshot).order_by(PMSPositionSnapshot.as_of_date.desc()).first()
                if latest:
                    context["as_of_date"] = latest.as_of_date.strftime('%Y-%m-%d')
                    exceptions = self.db.query(PMSPositionSnapshot).filter(
                        PMSPositionSnapshot.as_of_date == latest.as_of_date,
                        PMSPositionSnapshot.governance_monitor_status == 'approved_exception'
                    ).all()
                    context["informational_statuses"] = [
                        {"ticker": ex.ticker, "status": ex.governance_monitor_status, "message": "exception_active"}
                        for ex in exceptions
                    ]
                    context["alerts_total"] = len(exceptions)
            except Exception as e:
                logger.warning(f"Failed to query DB for PMS snapshot, falling back to mock: {e}")
                
        template = self.env.get_template("pms_daily_monitor.md.j2")
        return template.render(**context)

    def generate_lp_brief(self, run_id: str) -> str:
        """
        Generates the LP Brief Markdown.
        """
        context = {
            "run_id": run_id,
            # Mock MVP data
        }
        template = self.env.get_template("lp_brief.md.j2")
        return template.render(**context)

    def generate_pdf_from_markdown(self, md_content: str) -> bytes:
        """
        Converts Markdown to HTML to PDF byte stream.
        """
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        # Wrap in basic HTML for styling
        html_doc = f"<html><head><style>body {{ font-family: sans-serif; }} table {{ border-collapse: collapse; width: 100%; }} th, td {{ border: 1px solid #ddd; padding: 8px; }}</style></head><body>{html_content}</body></html>"
        
        try:
            import weasyprint
            pdf = weasyprint.HTML(string=html_doc).write_pdf()
            return pdf
        except (ImportError, OSError):
            logger.warning("WeasyPrint GTK+ libraries missing on host. Returning mocked PDF bytes.")
            # Return dummy valid-ish PDF bytes for tests
            return b"%PDF-1.4\n%Mock PDF\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\ntrailer\n<<\n/Root 1 0 R\n>>\n%%EOF"
