import React from 'react';

export const AdminPortal = () => {
  return (
    <div className="glass-panel" style={{ padding: '24px', margin: '24px' }}>
      <h2 style={{ margin: 0, marginBottom: '24px', color: 'var(--accent-color)' }}>Admin Portal (System Settings)</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '24px' }}>
        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px' }}>Compliance Rules Engine</h3>
          <label style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Single Stock Limit (%)
            <input type="number" defaultValue={10} style={{ width: '60px', padding: '4px', background: 'var(--bg-panel)', border: '1px solid var(--border-color)', color: 'var(--text-primary)' }} />
          </label>
          <label style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Leverage Cap (Gross %)
            <input type="number" defaultValue={150} style={{ width: '60px', padding: '4px', background: 'var(--bg-panel)', border: '1px solid var(--border-color)', color: 'var(--text-primary)' }} />
          </label>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px' }}>FIX Routing Connections</h3>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            <span>NYFIX Network</span>
            <span style={{ color: 'var(--status-positive)' }}>CONNECTED</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            <span>Oppenheimer</span>
            <span style={{ color: 'var(--status-positive)' }}>CONNECTED</span>
          </div>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px' }}>User Management</h3>
          <button className="btn-primary" style={{ width: '100%', marginBottom: '8px' }}>Invite PM / Trader</button>
          <button className="btn-primary" style={{ width: '100%', background: 'transparent', border: '1px solid var(--border-color)', color: 'var(--text-primary)' }}>View Audit Logs</button>
        </div>
      </div>
    </div>
  );
};
