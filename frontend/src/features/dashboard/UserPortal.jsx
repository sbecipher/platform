import React from 'react';
import { useAuthStore } from '../../store/authStore';
import { useWorkspaceStore } from '../../store/workspaceStore';

export const UserPortal = () => {
  const user = useAuthStore(state => state.user);
  const { metrics } = useWorkspaceStore();

  return (
    <div className="glass-panel" style={{ padding: '24px', margin: '24px' }}>
      <h2 style={{ margin: 0, marginBottom: '24px' }}>User Portal: Welcome {user?.name || 'User'}</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '24px' }}>
        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem', color: 'var(--text-secondary)' }}>Total NAV</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>{metrics.totalNav}</div>
          <div style={{ color: metrics.isDayPnlPositive ? 'var(--status-positive)' : 'var(--status-negative)', fontSize: '0.875rem' }}>{metrics.dayPnl} Today</div>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem', color: 'var(--text-secondary)' }}>Gross Exposure</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>{metrics.grossExposure}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>of NAV</div>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem', color: 'var(--text-secondary)' }}>Net Exposure</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>{metrics.netExposure}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>of NAV</div>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem', color: 'var(--text-secondary)' }}>Portfolio Beta</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>{metrics.portfolioBeta}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>vs S&P 500</div>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem', color: 'var(--text-secondary)' }}>Available Cash</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>{metrics.availableCash}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Remaining</div>
        </div>

        <div style={{ padding: '16px', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
          <h3 style={{ margin: 0, marginBottom: '12px', fontSize: '1rem', color: 'var(--text-secondary)' }}>Active Orders</h3>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>{metrics.activeOrders}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Pending Execution in NYFIX</div>
        </div>
      </div>
    </div>
  );
};
