import React from 'react';

export const TradeBlotter = () => {
  const dummyOrders = [
    { id: 'ORD-001', symbol: 'AAPL', side: 'BUY', qty: 500, exec: 500, status: 'FILLED' },
    { id: 'ORD-002', symbol: 'TSLA', side: 'SELL', qty: 500, exec: 200, status: 'PARTIAL' },
  ];

  return (
    <div className="glass-panel" style={{ padding: '24px', height: '100%', width: '100%', boxSizing: 'border-box' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h2 style={{ fontWeight: 600, margin: 0 }}>Order Blotter (OMS)</h2>
      </div>
      <div className="modern-table-container" style={{ overflowX: 'auto', maxHeight: 'calc(100% - 40px)' }}>
        <table className="modern-table" style={{ width: '100%' }}>
          <thead style={{ position: 'sticky', top: 0, backgroundColor: 'var(--bg-panel)', zIndex: 1 }}>
            <tr>
              <th>Order ID</th>
              <th>Symbol</th>
              <th>Side</th>
              <th>Qty</th>
              <th>Exec</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {dummyOrders.map((ord, i) => (
              <tr key={i}>
                <td style={{ fontWeight: 500 }}>{ord.id}</td>
                <td>{ord.symbol}</td>
                <td style={{ color: ord.side === 'BUY' ? 'var(--status-positive)' : 'var(--status-negative)' }}>{ord.side}</td>
                <td>{ord.qty}</td>
                <td>{ord.exec}</td>
                <td style={{ color: ord.status === 'FILLED' ? 'var(--status-positive)' : 'var(--status-warning)' }}>{ord.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
