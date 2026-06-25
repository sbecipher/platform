import React, { useState } from 'react';
import { useWorkspaceStore } from '../../store/workspaceStore';

export const PortfolioModeling = () => {
  const holdings = useWorkspaceStore(state => state.holdings);
  const [targetWeights, setTargetWeights] = useState({
    'IE': 10, 'UEC': 10, 'AA': 20, 'AMR': 10, 'BTU': 10,
    'CDE': 15, 'CLF': 15, 'URG': 5, 'USAR': 5
  });
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleRebalance = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/modeling/rebalance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ portfolio: holdings, target_weights: targetWeights })
      });
      const data = await response.json();
      if (data.status === 'SUCCESS') {
        setOrders(data.orders);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', height: '100%', width: '100%', boxSizing: 'border-box', overflowY: 'auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h2 style={{ fontWeight: 600, margin: 0 }}>Portfolio Rebalancing Engine</h2>
        <button className="btn-primary" onClick={handleRebalance} disabled={loading}>
          {loading ? 'Calculating...' : 'Run Vectorized Engine'}
        </button>
      </div>

      <div style={{ display: 'flex', gap: '24px' }}>
        <div style={{ flex: 1 }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '12px' }}>Target Weights (%)</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
            {Object.entries(targetWeights).map(([sym, wgt]) => (
              <div key={sym} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ width: '40px', fontWeight: 500 }}>{sym}</span>
                <input 
                  type="number" 
                  value={wgt} 
                  onChange={e => setTargetWeights({ ...targetWeights, [sym]: parseFloat(e.target.value) || 0 })}
                  style={{ flex: 1, padding: '4px 8px', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}
                />
              </div>
            ))}
          </div>
        </div>
        
        <div style={{ flex: 2 }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '12px' }}>Generated Orders (Wholeshare)</h3>
          {orders.length === 0 ? (
            <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-secondary)', border: '1px dashed var(--border-color)', borderRadius: '8px' }}>
              No drift detected or engine not run.
            </div>
          ) : (
            <table className="modern-table" style={{ width: '100%' }}>
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Current Wgt</th>
                  <th>Target Wgt</th>
                  <th>Drift</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((ord, i) => (
                  <tr key={i}>
                    <td style={{ fontWeight: 600 }}>{ord.symbol}</td>
                    <td>{ord.current_weight}%</td>
                    <td>{ord.target_weight}%</td>
                    <td style={{ color: ord.drift > 0 ? 'var(--status-negative)' : 'var(--status-positive)' }}>{ord.drift}%</td>
                    <td>
                      <span style={{ padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 600, backgroundColor: ord.action_required.startsWith('BUY') ? 'rgba(34, 197, 94, 0.1)' : 'rgba(239, 68, 68, 0.1)', color: ord.action_required.startsWith('BUY') ? 'var(--status-positive)' : 'var(--status-negative)' }}>
                        {ord.action_required}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};
