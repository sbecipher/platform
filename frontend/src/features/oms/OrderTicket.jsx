import React, { useState } from 'react';
import { useWorkspaceStore } from '../../store/workspaceStore';

export const OrderTicket = () => {
  const holdings = useWorkspaceStore(state => state.holdings);
  
  const [symbol, setSymbol] = useState('');
  const [side, setSide] = useState('BUY');
  const [quantity, setQuantity] = useState('');
  const [price, setPrice] = useState('');
  const [broker, setBroker] = useState('NYFIX');
  
  const [complianceStatus, setComplianceStatus] = useState(null);
  const [routingStatus, setRoutingStatus] = useState(null);

  const handleSimulate = async () => {
    if (!symbol || !quantity || !price) {
      setComplianceStatus({ status: 'FAIL', reason: 'Please fill out symbol, quantity, and price.' });
      return;
    }
    
    try {
      const response = await fetch('http://localhost:8000/api/compliance/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          order: { symbol, side, quantity: parseFloat(quantity), price: parseFloat(price) },
          portfolio: holdings
        })
      });
      const result = await response.json();
      setComplianceStatus(result);
      setRoutingStatus(null);
    } catch (err) {
      console.error(err);
      setComplianceStatus({ status: 'FAIL', reason: 'API connection error.' });
    }
  };

  const handleRoute = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/oms/route', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol, side, quantity: parseFloat(quantity), price: parseFloat(price), order_type: 'LIMIT', broker
        })
      });
      const result = await response.json();
      setRoutingStatus(result);
    } catch (err) {
      console.error(err);
      setRoutingStatus({ message: 'Routing failed due to API error.' });
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', height: '100%', width: '100%', boxSizing: 'border-box' }}>
      <h2 style={{ fontWeight: 600, margin: 0, marginBottom: '16px' }}>Execution Ticket</h2>
      
      {complianceStatus && (
        <div style={{ padding: '12px', marginBottom: '16px', borderRadius: '4px', backgroundColor: complianceStatus.status === 'PASS' ? 'rgba(34, 197, 94, 0.1)' : 'rgba(239, 68, 68, 0.1)', border: `1px solid ${complianceStatus.status === 'PASS' ? 'var(--status-positive)' : 'var(--status-negative)'}` }}>
          <strong style={{ color: complianceStatus.status === 'PASS' ? 'var(--status-positive)' : 'var(--status-negative)' }}>{complianceStatus.status}</strong>
          <p style={{ margin: '4px 0 0 0', fontSize: '0.875rem' }}>{complianceStatus.reason}</p>
        </div>
      )}

      {routingStatus && (
        <div style={{ padding: '12px', marginBottom: '16px', borderRadius: '4px', backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid var(--accent-color)' }}>
          <strong style={{ color: 'var(--accent-color)' }}>ROUTED</strong>
          <p style={{ margin: '4px 0 0 0', fontSize: '0.875rem' }}>{routingStatus.message}</p>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div style={{ display: 'flex', gap: '12px' }}>
          <div style={{ flex: 1 }}>
            <label style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Symbol</label>
            <input type="text" value={symbol} onChange={e => setSymbol(e.target.value.toUpperCase())} placeholder="e.g. AAPL" style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
          </div>
          <div style={{ flex: 1 }}>
            <label style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Side</label>
            <select value={side} onChange={e => setSide(e.target.value)} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>
              <option>BUY</option>
              <option>SELL</option>
              <option>SHORT</option>
            </select>
          </div>
        </div>
        
        <div style={{ display: 'flex', gap: '12px' }}>
          <div style={{ flex: 1 }}>
            <label style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Quantity</label>
            <input type="number" value={quantity} onChange={e => setQuantity(e.target.value)} onBlur={handleSimulate} placeholder="0" style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
          </div>
          <div style={{ flex: 1 }}>
            <label style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Type</label>
            <select style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>
              <option>LIMIT</option>
              <option>MARKET</option>
            </select>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <div style={{ flex: 1 }}>
            <label style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Price</label>
            <input type="number" value={price} onChange={e => setPrice(e.target.value)} onBlur={handleSimulate} placeholder="0.00" style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
          </div>
          <div style={{ flex: 1 }}>
            <label style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Broker</label>
            <select value={broker} onChange={e => setBroker(e.target.value)} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>
              <option>NYFIX</option>
              <option>Oppenheimer</option>
            </select>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '12px', marginTop: '16px' }}>
          <button className="btn-primary" onClick={handleSimulate} style={{ flex: 1, backgroundColor: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>Simulate</button>
          <button className="btn-primary" onClick={handleRoute} disabled={complianceStatus?.status !== 'PASS'} style={{ flex: 1, opacity: complianceStatus?.status !== 'PASS' ? 0.5 : 1 }}>Route Order</button>
        </div>
      </div>
    </div>
  );
};
