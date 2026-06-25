import csv
import os
from datetime import datetime
import pandas as pd
import numpy as np

# Adjust imports to include Equity
from scp_core.pricing.options import OptionsSecurity
from scp_core.pricing.irswap import IRSwapSecurity
# Assuming EquitySecurity was implemented as part of Phase 3 Equity Implementation
import sys

# Optional mock class if actual EquitySecurity isn't fully accessible in path yet
class MockEquitySecurity:
    def __init__(self, security_id, quantity):
        self.security_id = security_id
        self.quantity = quantity
        
    def get_market_value(self, current_price: float) -> float:
        return self.quantity * current_price

def evaluate_pipeline(filepath: str):
    print(f"--- 1. Reading Real Portfolio from CSV: {filepath} ---")
    
    # Read CSV, handle thousands separators in numbers
    df = pd.read_csv(filepath, thousands=',')
    
    # Clean up column names and strings
    df.columns = df.columns.str.strip()
    df['SECURITY TYPE'] = df['SECURITY TYPE'].str.strip()
    df['SECURITY'] = df['SECURITY'].str.strip()
    
    print(f"Loaded {len(df)} positions.")
    print(df[['SECURITY', 'SECURITY TYPE', 'TOTAL QUANTITY', 'CLOSING PRICE', 'VALUE']].head().to_string())
    print("\n")
    
    print("--- 2. Executing Pricing Logic per Asset Class ---")
    
    portfolio_value = 0.0
    equity_assets = []
    equity_quantities = []
    
    for idx, row in df.iterrows():
        sec_id = str(row['SECURITY'])
        asset_class = str(row['SECURITY TYPE'])
        
        # Parse quantity safely
        try:
            qty_str = str(row['TOTAL QUANTITY']).replace(',', '')
            quantity = float(qty_str)
        except ValueError:
            quantity = 0.0
            
        try:
            closing_price = float(row['CLOSING PRICE'])
        except ValueError:
            closing_price = 0.0

        if asset_class == "Stock":
            # Instantiate Equity Pricing
            equity = MockEquitySecurity(security_id=sec_id, quantity=quantity)
            
            position_value = equity.get_market_value(closing_price)
            portfolio_value += position_value
            
            equity_assets.append(sec_id)
            equity_quantities.append(position_value) # Using value as proxy for weight later
            
        elif asset_class == "Cash":
            portfolio_value += quantity

    print(f"Total Portfolio Value Evaluated: ${portfolio_value:,.2f}\n")
    
    print("--- 3. Running Vectorized Risk Analytics (Pandas/Numpy) ---")
    from scp_core.analytics.risk import RiskAnalytics
    risk_engine = RiskAnalytics(confidence_interval=0.99)
    
    # We will simulate risk on the Equity assets we parsed
    if len(equity_assets) > 0:
        print(f"Simulating Risk for {len(equity_assets)} Equity positions...")
        np.random.seed(42)
        # Simulate historical returns for the parsed assets (1000 days)
        mock_returns = np.random.normal(0.0005, 0.02, (1000, len(equity_assets)))
        returns_df = pd.DataFrame(mock_returns, columns=equity_assets)
        
        # Calculate weights based on position value
        total_eq_value = sum(abs(v) for v in equity_quantities)
        weights = np.array([abs(v)/total_eq_value for v in equity_quantities])
        
        var_99 = risk_engine.calculate_historical_var(returns_df, weights)
        print(f"Daily Historical VaR (99%): {var_99 * 100:.2f}%")
        
        # Monte Carlo Stress Test
        print("Running 10,000 Monte Carlo Simulations...")
        cov_matrix = returns_df.cov().values
        current_prices = np.ones(len(equity_assets)) * 100.0 # Base 100 for simulation
        
        simulations = risk_engine.run_monte_carlo_stress_test(current_prices, cov_matrix, num_simulations=10000)
        print(f"Monte Carlo Output Shape: {simulations.shape} (Assets x Paths)")
    else:
        print("No Equity assets found to simulate risk.")
        
    print("\n--- Pipeline Evaluation Complete! ---")

if __name__ == "__main__":
    csv_path = r"C:\Users\JRodriguezGoldstein\Documents\antigravity\xDevelopment-portfolio.csv"
    evaluate_pipeline(csv_path)
