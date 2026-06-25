import pandas as pd
import numpy as np
from typing import List, Dict, Any

class RebalancingEngine:
    def generate_target_orders(self, current_portfolio: List[Dict[str, Any]], target_weights: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Calculates drift between target weights and current weights, 
        generating exact buy/sell integer quantities.
        """
        if not current_portfolio:
            return []

        # Convert portfolio list of dicts to pandas DataFrame for vectorized math
        df = pd.DataFrame(current_portfolio)
        
        # Clean 'value' strings into floats
        if 'value' in df.columns and df['value'].dtype == 'O':
            df['value'] = df['value'].astype(str).str.replace('$', '').str.replace(',', '').astype(float)
        
        # Clean 'quantity' into floats
        if 'quantity' in df.columns and df['quantity'].dtype == 'O':
            df['quantity'] = df['quantity'].astype(str).str.replace(',', '').astype(float)

        # Infer current prices
        df['current_price'] = df['value'] / df['quantity'].replace({0: np.nan})
        
        # Calculate Total AUM
        total_aum = df['value'].sum()
        if total_aum == 0:
            total_aum = 1000000.0 # Mock fallback

        df['current_weight_pct'] = (df['value'] / total_aum) * 100.0

        orders = []

        for index, row in df.iterrows():
            sym = row['symbol']
            curr_wgt = row['current_weight_pct']
            curr_qty = row['quantity']
            curr_px = row['current_price']
            
            tgt_wgt = target_weights.get(sym, 0.0)
            drift = curr_wgt - tgt_wgt
            
            # If absolute drift is > 0.5%, generate a rebalancing order
            if abs(drift) > 0.5 and not pd.isna(curr_px) and curr_px > 0:
                tgt_value = total_aum * (tgt_wgt / 100.0)
                tgt_qty = int(tgt_value / curr_px)
                
                qty_diff = tgt_qty - int(curr_qty)
                
                if qty_diff != 0:
                    action = "BUY" if qty_diff > 0 else "SELL"
                    orders.append({
                        "symbol": sym,
                        "current_weight": round(curr_wgt, 2),
                        "target_weight": round(tgt_wgt, 2),
                        "drift": round(drift, 2),
                        "current_qty": int(curr_qty),
                        "target_qty": tgt_qty,
                        "action_required": f"{action} {abs(qty_diff)}",
                        "trade_value": round(abs(qty_diff) * curr_px, 2),
                        "post_weight": round(tgt_wgt, 2)
                    })
                    
        return orders
