import React from 'react';
import { useAuthStore } from '../../store/authStore';

export const UserPortal = () => {
  const user = useAuthStore(state => state.user);

  return (
    <div className="glass-panel" style={{ padding: '24px', margin: '24px' }}>
      <h2 style={{ margin: 0, marginBottom: '24px' }}>User Portal: Welcome {user?.name || 'User'}</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem' }}>My Daily Metrics</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--status-positive)' }}>+$18,450</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Total Day PnL</div>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem' }}>Active Orders</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>3</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Pending Execution in NYFIX</div>
        </div>
      </div>
    </div>
  );
};
