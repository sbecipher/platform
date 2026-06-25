import pandas as pd
from datetime import datetime
from scp_core.store.db import SessionLocal, engine
from scp_core.store.models import Base, PortfolioDB, PortfolioAllocationDB, WorkingOrderDB


def ingest_portfolio_csv(filepath: str, portfolio_name: str, base_currency: str = "USD"):
    """
    Parses a legacy Sbecipher format CSV and ingests it into the new Postgres database schema.
    """
    print(f"[{datetime.now().isoformat()}] Ingesting {filepath} into portfolio '{portfolio_name}'")

    # Initialize the database schema if it doesn't exist (useful for testing)
    Base.metadata.create_all(bind=engine)

    # Read CSV
    df = pd.read_csv(filepath, thousands=",")
    df.columns = df.columns.str.strip()

    db = SessionLocal()
    try:
        # Check if portfolio exists, else create it
        portfolio = db.query(PortfolioDB).filter_by(name=portfolio_name).first()
        if not portfolio:
            portfolio = PortfolioDB(name=portfolio_name, base_currency=base_currency, created_at=datetime.now())
            db.add(portfolio)
            db.commit()
            db.refresh(portfolio)
            print(f"Created new Portfolio: {portfolio.name} (ID: {portfolio.id})")
        else:
            print(f"Found existing Portfolio: {portfolio.name} (ID: {portfolio.id})")

        added_count = 0

        for idx, row in df.iterrows():
            sec_id = str(row["SECURITY"]).strip()

            # Skip empty rows
            if not sec_id or sec_id == "nan":
                continue

            try:
                qty_str = str(row["TOTAL QUANTITY"]).replace(",", "")
                quantity = float(qty_str)
            except ValueError:
                quantity = 0.0

            # Create a WorkingOrder entry as a dummy for the position origin
            order = WorkingOrderDB(
                security_sn=sec_id,
                order_quantity=quantity,
                filled_quantity=quantity,
                is_live=False,  # It's already filled/historical
                trade_date=datetime.now(),
            )
            db.add(order)
            db.flush()  # Get the order ID

            # Map the filled order directly to the Portfolio
            allocation = PortfolioAllocationDB(
                working_order_id=order.id,
                portfolio_id=portfolio.id,
                pre_allocation=quantity,
                filled_allocation=quantity,
                include=True,
            )
            db.add(allocation)
            added_count += 1

        db.commit()
        print(f"Successfully ingested {added_count} positions into Portfolio '{portfolio_name}'.")

    except Exception as e:
        db.rollback()
        print(f"Error during ingestion: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python ingestion.py <path_to_csv> <portfolio_name>")
    else:
        csv_path = sys.argv[1]
        p_name = sys.argv[2]
        ingest_portfolio_csv(csv_path, p_name)
