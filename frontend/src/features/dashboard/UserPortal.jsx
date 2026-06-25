import React from 'react';
import { useAuthStore } from '../../store/authStore';

export const UserPortal = () => {
  const user = useAuthStore(state => state.user);

  return (
    <div className="glass-panel" style={{ padding: '24px', margin: '24px' }}>
      <h2 style={{ margin: 0, marginBottom: '24px' }}>User Portal: Welcome {user?.name || 'User'}</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '24px' }}>
        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem', color: 'var(--text-secondary)' }}>Total NAV</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>$1,000,000.00</div>
          <div style={{ color: 'var(--status-positive)', fontSize: '0.875rem' }}>+0.45% Today</div>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem', color: 'var(--text-secondary)' }}>Gross Exposure</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>$1,250,000</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>125.0% of NAV</div>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem', color: 'var(--text-secondary)' }}>Net Exposure</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>$850,000</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>85.0% of NAV</div>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem', color: 'var(--text-secondary)' }}>Portfolio Beta</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>0.85</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>vs S&P 500</div>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem', color: 'var(--text-secondary)' }}>Available Cash</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>$150,000</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>15.0% of NAV</div>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem', color: 'var(--text-secondary)' }}>Active Orders</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>3</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Pending Execution in NYFIX</div>
        </div>
      </div>
    </div>
  );
};
