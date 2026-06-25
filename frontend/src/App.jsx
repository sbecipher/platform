import { useEffect, useState } from 'react';
import Papa from 'papaparse';
import { 
  LayoutDashboard, 
  Briefcase, 
  ShieldAlert, 
  BarChart3, 
  FileText, 
  Search,
  Settings,
  Bell,
  Sun,
  Moon,
  Monitor,
  Upload
} from 'lucide-react';
import './App.css';

const xDevHoldings = [
  { symbol: 'IE', quantity: '29,022', value: '$547,645', pnl: '+$188,566', exposure: '7.31%', isPositive: true },
  { symbol: 'UEC', quantity: '37,219', value: '$599,225', pnl: '+$283,819', exposure: '8.00%', isPositive: true },
  { symbol: 'AA', quantity: '30,324', value: '$1,763,643', pnl: '+$580,386', exposure: '23.54%', isPositive: true },
  { symbol: 'AMR', quantity: '3,780', value: '$789,112', pnl: '+$162,684', exposure: '10.53%', isPositive: true },
  { symbol: 'BTU', quantity: '37,460', value: '$1,311,474', pnl: '+$385,032', exposure: '17.50%', isPositive: true },
  { symbol: 'CDE', quantity: '62,778', value: '$1,302,643', pnl: '+$478,684', exposure: '17.39%', isPositive: true },
  { symbol: 'CLF', quantity: '82,492', value: '$1,198,608', pnl: '+$264,023', exposure: '16.00%', isPositive: true },
  { symbol: 'URG', quantity: '-1,982', value: '-$3,270', pnl: '-$652', exposure: '-0.04%', isPositive: false },
  { symbol: 'USAR', quantity: '-40,109', value: '-$943,764', pnl: '-$291,886', exposure: '-12.60%', isPositive: false }
];

const PortfolioHoldings = ({ data }) => {
  return (
    <div className="glass-panel" style={{ padding: '24px', height: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h2 style={{ fontWeight: 600 }}>Portfolio Holdings</h2>
        <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{data.length} Positions</span>
      </div>
      <div className="modern-table-container" style={{ overflowX: 'auto', maxHeight: 'calc(100% - 40px)' }}>
        <table className="modern-table">
          <thead style={{ position: 'sticky', top: 0, backgroundColor: 'var(--bg-panel)', zIndex: 1 }}>
            <tr>
              <th>Symbol</th>
              <th>Quantity</th>
              <th>Market Value</th>
              <th>Unrealized PnL</th>
              <th>Exposure (NAV)</th>
            </tr>
          </thead>
          <tbody>
            {data.map((pos, i) => (
              <tr key={i}>
                <td style={{ fontWeight: 500 }}>{pos.symbol}</td>
                <td>{pos.quantity}</td>
                <td>{pos.value}</td>
                <td className={pos.isPositive ? "text-positive" : "text-negative"}>{pos.pnl}</td>
                <td>{pos.exposure}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const ComplianceDashboard = ({ data }) => {
  const warnings = data.filter(pos => {
    const exp = parseFloat(pos.exposure.replace(/[^0-9.-]+/g,""));
    return exp > 10 || exp < -10;
  });

  return (
    <div className="glass-panel" style={{ padding: '24px', height: '100%' }}>
      <h2 style={{ marginBottom: '16px', fontWeight: 600, color: 'var(--status-warning)' }}>Pre-Trade Warnings</h2>
      {warnings.length === 0 ? (
        <p style={{ color: 'var(--text-secondary)' }}>No compliance violations detected.</p>
      ) : (
        warnings.map((w, i) => (
          <div key={i} style={{ padding: '16px', borderLeft: '4px solid var(--status-warning)', backgroundColor: 'var(--bg-secondary)', borderRadius: '0 8px 8px 0', marginBottom: '16px' }}>
            <strong>Warning: Single Position Limit Violation</strong>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Position {w.symbol} exceeds 10% NAV limit (Current Exposure: {w.exposure}).
            </p>
          </div>
        ))
      )}
    </div>
  );
};

const PortfolioModeling = ({ data }) => {
  const [showOrders, setShowOrders] = useState(false);
  const [showCash, setShowCash] = useState(false);
  const targetWeight = data.length > 0 ? (100 / data.length) : 0;

  return (
    <div className="glass-panel" style={{ padding: '24px', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <h2 style={{ marginBottom: '16px', fontWeight: 600 }}>Modeling & Rebalancing</h2>
      <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
        <button className="btn-primary" onClick={() => { setShowOrders(true); setShowCash(false); }}>Generate Equal-Weight Orders</button>
        <button className="btn-primary" style={{ backgroundColor: 'var(--bg-secondary)', color: 'var(--text-primary)' }} onClick={() => { setShowCash(true); setShowOrders(false); }}>View T+N Cash Forecast</button>
      </div>

      <div style={{ display: 'flex', gap: '24px', flex: 1, minHeight: 0 }}>
        {/* Main exposures table */}
        <div className="modern-table-container" style={{ flex: 1, overflowX: 'auto' }}>
          <table className="modern-table">
            <thead style={{ position: 'sticky', top: 0, backgroundColor: 'var(--bg-panel)', zIndex: 1 }}>
              <tr>
                <th>Symbol</th>
                <th>Current Exposure</th>
                <th>Target Exposure</th>
                <th>Drift</th>
              </tr>
            </thead>
            <tbody>
              {data.map((pos, i) => {
                const currentExp = parseFloat(pos.exposure.replace(/[^0-9.-]+/g,"")) || 0;
                const drift = currentExp - targetWeight;
                return (
                  <tr key={i}>
                    <td style={{ fontWeight: 500 }}>{pos.symbol}</td>
                    <td>{pos.exposure}</td>
                    <td>{targetWeight.toFixed(2)}%</td>
                    <td style={{ color: Math.abs(drift) > 5 ? 'var(--status-warning)' : 'inherit' }}>
                      {drift > 0 ? '+' : ''}{drift.toFixed(2)}%
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>

        {/* Dynamic Action Results Panel */}
        {(showOrders || showCash) && (
          <div style={{ width: '350px', backgroundColor: 'var(--bg-secondary)', padding: '16px', borderRadius: '8px', overflowY: 'auto' }}>
            {showOrders && (
              <>
                <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '12px' }}>Generated Orders</h3>
                {data.map((pos, i) => {
                  const currentExp = parseFloat(pos.exposure.replace(/[^0-9.-]+/g,"")) || 0;
                  const drift = currentExp - targetWeight;
                  if (Math.abs(drift) < 0.5) return null;
                  const action = drift > 0 ? 'SELL' : 'BUY';
                  return (
                    <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid var(--border-color)' }}>
                      <span style={{ fontWeight: 500 }}>{pos.symbol}</span>
                      <span style={{ color: action === 'BUY' ? 'var(--status-positive)' : 'var(--status-negative)' }}>{action} to Target</span>
                    </div>
                  );
                })}
              </>
            )}
            {showCash && (
              <>
                <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '12px' }}>T+N Cash Forecast</h3>
                <div style={{ padding: '8px 0', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between' }}>
                  <span>T+1 (Tomorrow)</span>
                  <span style={{ color: 'var(--status-positive)' }}>+$125,000</span>
                </div>
                <div style={{ padding: '8px 0', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between' }}>
                  <span>T+2</span>
                  <span style={{ color: 'var(--status-negative)' }}>-$45,200</span>
                </div>
                <div style={{ padding: '8px 0', display: 'flex', justifyContent: 'space-between', fontWeight: 'bold' }}>
                  <span>Net Projected Cash</span>
                  <span>+$79,800</span>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

const DashboardView = ({ data }) => {
  const totalAum = data.reduce((acc, pos) => acc + parseFloat(pos.value.replace(/[^0-9.-]+/g,"") || 0), 0);
  const totalPnl = data.reduce((acc, pos) => acc + parseFloat(pos.pnl.replace(/[^0-9.-]+/g,"") || 0), 0);
  const netExposure = data.reduce((acc, pos) => acc + parseFloat(pos.exposure.replace(/[^0-9.-]+/g,"") || 0), 0);
  
  const sortedByPnl = [...data].sort((a, b) => parseFloat(b.pnl.replace(/[^0-9.-]+/g,"") || 0) - parseFloat(a.pnl.replace(/[^0-9.-]+/g,"") || 0));
  const topWinner = sortedByPnl.length > 0 && parseFloat(sortedByPnl[0].pnl.replace(/[^0-9.-]+/g,"")) > 0 ? sortedByPnl[0] : { symbol: 'N/A', pnl: '$0' };
  const topLoser = sortedByPnl.length > 0 && parseFloat(sortedByPnl[sortedByPnl.length - 1].pnl.replace(/[^0-9.-]+/g,"")) < 0 ? sortedByPnl[sortedByPnl.length - 1] : { symbol: 'N/A', pnl: '$0' };

  return (
    <div className="glass-panel" style={{ padding: '24px', height: '100%', overflowY: 'auto' }}>
      <h2 style={{ marginBottom: '16px', fontWeight: 600 }}>Executive Dashboard</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
        <div style={{ padding: '16px', backgroundColor: 'var(--bg-secondary)', borderRadius: '8px' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Total AUM</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>${totalAum.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
        </div>
        <div style={{ padding: '16px', backgroundColor: 'var(--bg-secondary)', borderRadius: '8px' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Unrealized PnL</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: totalPnl >= 0 ? 'var(--status-positive)' : 'var(--status-negative)' }}>
            {totalPnl >= 0 ? '+' : '-'}${Math.abs(totalPnl).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}
          </div>
        </div>
        <div style={{ padding: '16px', backgroundColor: 'var(--bg-secondary)', borderRadius: '8px' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Net Exposure</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{netExposure.toFixed(2)}%</div>
        </div>
        <div style={{ padding: '16px', backgroundColor: 'var(--bg-secondary)', borderRadius: '8px' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Total Positions</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{data.length}</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
        <div style={{ padding: '20px', backgroundColor: 'var(--bg-secondary)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '16px', color: 'var(--text-secondary)' }}>Performance Extremes</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '12px', borderBottom: '1px solid var(--border-color)' }}>
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Top Winner</div>
                <div style={{ fontWeight: 600 }}>{topWinner.symbol}</div>
              </div>
              <div style={{ color: 'var(--status-positive)', fontWeight: 'bold' }}>{topWinner.pnl}</div>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Top Loser</div>
                <div style={{ fontWeight: 600 }}>{topLoser.symbol}</div>
              </div>
              <div style={{ color: 'var(--status-negative)', fontWeight: 'bold' }}>{topLoser.pnl}</div>
            </div>
          </div>
        </div>

        <div style={{ padding: '20px', backgroundColor: 'var(--bg-secondary)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '16px', color: 'var(--text-secondary)' }}>Exposure Concentration</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {data.slice(0, 3).map((pos, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{ width: '60px', fontWeight: 500 }}>{pos.symbol}</div>
                <div style={{ flex: 1, height: '8px', backgroundColor: 'var(--bg-panel)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: Math.abs(parseFloat(pos.exposure.replace(/[^0-9.-]+/g,""))) + '%', height: '100%', backgroundColor: 'var(--accent-color)', borderRadius: '4px' }}></div>
                </div>
                <div style={{ width: '60px', textAlign: 'right', fontSize: '0.875rem' }}>{pos.exposure}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const ReportsView = ({ data }) => {
  const downloadReport = (type) => {
    let reportData = [];
    let filename = "";

    if (type === 'pnl') {
      reportData = data.map(pos => ({
        Symbol: pos.symbol,
        'Market Value': pos.value,
        'Unrealized PnL': pos.pnl
      }));
      filename = "pnl_summary_export.csv";
    } else if (type === 'exposure') {
      reportData = data.map(pos => ({
        Symbol: pos.symbol,
        Quantity: pos.quantity,
        'Exposure (NAV)': pos.exposure
      }));
      filename = "regulatory_exposure_ucits.csv";
    }

    const csv = Papa.unparse(reportData);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', height: '100%' }}>
      <h2 style={{ marginBottom: '16px', fontWeight: 600 }}>Reports & Analytics</h2>
      <div style={{ padding: '16px', backgroundColor: 'var(--bg-secondary)', borderRadius: '8px', marginBottom: '16px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>End of Day PnL Summary</span>
          <button className="btn-primary" style={{ padding: '4px 12px', fontSize: '0.875rem' }} onClick={() => downloadReport('pnl')}>Download PnL Report</button>
        </div>
      </div>
      <div style={{ padding: '16px', backgroundColor: 'var(--bg-secondary)', borderRadius: '8px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>Regulatory Exposure (UCITS)</span>
          <button className="btn-primary" style={{ padding: '4px 12px', fontSize: '0.875rem' }} onClick={() => downloadReport('exposure')}>Download Exposure Report</button>
        </div>
      </div>
    </div>
  );
};

function App() {
  const [activeView, setActiveView] = useState('portfolio');
  const [themePreference, setThemePreference] = useState('system');
  const [holdings, setHoldings] = useState(xDevHoldings);

  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    if (themePreference === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    } else {
      root.classList.add(themePreference);
    }
  }, [themePreference]);

  const handleFileUpload = (e) => {
    if (e.target.files.length > 0) {
      const file = e.target.files[0];
      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: function(results) {
          const parsedHoldings = results.data
            .filter(row => row['COMPANY SYMBOL'] && row['COMPANY SYMBOL'].trim() !== '')
            .map(row => {
              const pnlStr = (row['UNREALIZED PL'] || '0').replace(/["',]/g, '');
              const pnlVal = parseFloat(pnlStr) || 0;
              const valStr = (row['VALUE LOCAL CURRENCY'] || '0').replace(/["']/g, '');
              const isPositive = pnlVal >= 0;
              return {
                symbol: row['COMPANY SYMBOL'],
                quantity: (row['TOTAL QUANTITY'] || '0').replace(/["']/g, ''),
                value: valStr.startsWith('-') ? `-$${valStr.substring(1)}` : `$${valStr}`,
                pnl: (isPositive ? '+$' : '-$') + Math.abs(pnlVal).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}),
                exposure: row['Exposure PCT NAV'] || '0.00 %',
                isPositive: isPositive
              };
            });
          setHoldings(parsedHoldings);
          alert(`Successfully loaded ${parsedHoldings.length} positions from ${file.name}`);
        }
      });
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      <aside className="glass-panel" style={{ width: '250px', borderRight: '1px solid var(--border-glass)', borderRadius: 0, display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '24px', borderBottom: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'linear-gradient(135deg, var(--accent-color), #8b5cf6)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold' }}>S</div>
          <h1 style={{ fontSize: '1.25rem', fontWeight: 700, letterSpacing: '-0.5px' }}>Sbecipher</h1>
        </div>
        
        <nav style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
          <NavItem icon={<Briefcase size={20} />} label="Portfolios" active={activeView === 'portfolio'} onClick={() => setActiveView('portfolio')} />
          <NavItem icon={<BarChart3 size={20} />} label="Modeling" active={activeView === 'modeling'} onClick={() => setActiveView('modeling')} />
          <NavItem icon={<ShieldAlert size={20} />} label="Compliance" active={activeView === 'compliance'} onClick={() => setActiveView('compliance')} />
          <NavItem icon={<LayoutDashboard size={20} />} label="Dashboard" active={activeView === 'dashboard'} onClick={() => setActiveView('dashboard')} />
          <NavItem icon={<FileText size={20} />} label="Reports" active={activeView === 'reports'} onClick={() => setActiveView('reports')} />
        </nav>

        <div style={{ padding: '16px', borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'center', gap: '12px' }}>
          <button onClick={() => setThemePreference('light')} style={{ background: 'none', border: 'none', cursor: 'pointer', color: themePreference === 'light' ? 'var(--accent-color)' : 'var(--text-secondary)' }}><Sun size={18} /></button>
          <button onClick={() => setThemePreference('system')} style={{ background: 'none', border: 'none', cursor: 'pointer', color: themePreference === 'system' ? 'var(--accent-color)' : 'var(--text-secondary)' }}><Monitor size={18} /></button>
          <button onClick={() => setThemePreference('dark')} style={{ background: 'none', border: 'none', cursor: 'pointer', color: themePreference === 'dark' ? 'var(--accent-color)' : 'var(--text-secondary)' }}><Moon size={18} /></button>
        </div>
      </aside>

      <main style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <header className="glass-panel" style={{ height: '70px', borderRadius: 0, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 24px', borderBottom: '1px solid var(--border-glass)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <select style={{ background: 'var(--bg-secondary)', color: 'var(--text-primary)', border: '1px solid var(--border-color)', padding: '8px 16px', borderRadius: '6px', outline: 'none' }}>
              <option>Uploaded CSV Portfolio</option>
              <option>xDevelopment Portfolio</option>
              <option>Global Macro Fund</option>
            </select>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', padding: '8px 16px', borderRadius: '6px', border: '1px dashed var(--border-color)', color: 'var(--text-secondary)' }}>
              <Upload size={16} />
              <span style={{ fontSize: '0.875rem' }}>Upload CSV</span>
              <input type="file" accept=".csv" style={{ display: 'none' }} onChange={handleFileUpload} />
            </label>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ position: 'relative' }}>
              <Search size={16} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }} />
              <input type="text" placeholder="Search securities..." style={{ background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', padding: '8px 12px 8px 36px', borderRadius: '20px', color: 'var(--text-primary)', outline: 'none', width: '250px' }} />
            </div>
            <button className="btn-primary">Execute Orders</button>
            <Bell size={20} style={{ color: 'var(--text-secondary)', cursor: 'pointer' }} />
            <Settings size={20} style={{ color: 'var(--text-secondary)', cursor: 'pointer' }} />
          </div>
        </header>

        <div style={{ flex: 1, padding: '24px', overflowY: 'auto' }}>
          {activeView === 'portfolio' && <PortfolioHoldings data={holdings} />}
          {activeView === 'compliance' && <ComplianceDashboard data={holdings} />}
          {activeView === 'modeling' && <PortfolioModeling data={holdings} />}
          {activeView === 'dashboard' && <DashboardView data={holdings} />}
          {activeView === 'reports' && <ReportsView data={holdings} />}
        </div>
        
        <footer className="glass-panel" style={{ height: '40px', borderRadius: 0, borderTop: '1px solid var(--border-glass)', display: 'flex', alignItems: 'center', padding: '0 24px', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--status-positive)' }}></span>
            WebSocket connected: /ws/portfolio/1
          </div>
          <div style={{ marginLeft: 'auto' }}>
            Last updated: {new Date().toLocaleTimeString()}
          </div>
        </footer>
      </main>

    </div>
  );
}

const NavItem = ({ icon, label, active, onClick }) => {
  return (
    <div 
      onClick={onClick}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        padding: '10px 12px',
        borderRadius: '8px',
        cursor: 'pointer',
        background: active ? 'var(--accent-color)' : 'transparent',
        color: active ? '#fff' : 'var(--text-secondary)',
        fontWeight: active ? 600 : 400,
        transition: 'background 0.2s, color 0.2s'
      }}
    >
      {icon}
      <span>{label}</span>
    </div>
  );
};

export default App;
