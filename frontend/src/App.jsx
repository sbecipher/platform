import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation, Navigate } from 'react-router-dom';
import { LayoutDashboard, Briefcase, Settings, Bell, Sun, Moon, Search, LogOut, FileText } from 'lucide-react';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { MainLayout } from './layouts/MainLayout';
import { Login } from './features/auth/Login';
import { AdminPortal } from './features/dashboard/AdminPortal';
import { UserPortal } from './features/dashboard/UserPortal';
import { LPStudio } from './features/reports/LPStudio';
import { useWorkspaceStore } from './store/workspaceStore';
import { useAuthStore } from './store/authStore';
import './App.css';

// Protected Route Wrapper
const ProtectedRoute = ({ children, requiredRole }) => {
  const { isAuthenticated, role } = useAuthStore();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  if (requiredRole && role !== requiredRole) {
    // If Admin is required but user is not admin, push to user portal
    return <Navigate to="/dashboard" replace />;
  }
  
  return children;
};

const Sidebar = () => {
  const location = useLocation();
  const { themePreference, setThemePreference } = useWorkspaceStore();
  const { logout, role } = useAuthStore();

  return (
    <aside className="glass-panel" style={{ width: '60px', borderRight: '1px solid var(--border-glass)', borderRadius: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '24px 0' }}>
      <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'linear-gradient(135deg, var(--accent-color), #8b5cf6)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold', marginBottom: '32px' }}>S</div>
      
      <nav style={{ display: 'flex', flexDirection: 'column', gap: '24px', flex: 1 }}>
        <Link to="/" style={{ color: location.pathname === '/' ? 'var(--accent-color)' : 'var(--text-secondary)' }}><Briefcase size={24} /></Link>
        <Link to="/dashboard" style={{ color: location.pathname === '/dashboard' ? 'var(--accent-color)' : 'var(--text-secondary)' }}><LayoutDashboard size={24} /></Link>
        <Link to="/reports" style={{ color: location.pathname === '/reports' ? 'var(--accent-color)' : 'var(--text-secondary)' }}><FileText size={24} /></Link>
        {role === 'ADMIN' && (
          <Link to="/admin" style={{ color: location.pathname === '/admin' ? 'var(--accent-color)' : 'var(--text-secondary)' }}><Settings size={24} /></Link>
        )}
      </nav>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <button onClick={() => setThemePreference(themePreference === 'dark' ? 'light' : 'dark')} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-secondary)' }}>
          {themePreference === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
        </button>
        <button onClick={logout} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-secondary)' }}>
          <LogOut size={20} />
        </button>
      </div>
    </aside>
  );
};

const Header = () => {
  const { user } = useAuthStore();
  
  return (
    <header className="glass-panel" style={{ height: '70px', borderRadius: 0, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 24px', borderBottom: '1px solid var(--border-glass)' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <h1 style={{ fontSize: '1.25rem', fontWeight: 700, margin: 0 }}>Sbecipher Terminal</h1>
      </div>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{ position: 'relative' }}>
          <Search size={16} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }} />
          <input type="text" placeholder="Cmd+K to search..." style={{ background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', padding: '8px 12px 8px 36px', borderRadius: '20px', color: 'var(--text-primary)', outline: 'none', width: '250px' }} />
        </div>
        <Bell size={20} style={{ color: 'var(--text-secondary)', cursor: 'pointer' }} />
        <div style={{ width: '32px', height: '32px', borderRadius: '50%', backgroundColor: 'var(--accent-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: '0.875rem', fontWeight: 600 }}>
          {user?.name ? user.name.charAt(0) : 'PM'}
        </div>
      </div>
    </header>
  );
};

// Main App Layout Shell
const AppShell = ({ children }) => {
  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      <Sidebar />
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Header />
        <div style={{ flex: 1, position: 'relative', overflowY: 'auto' }}>
          {children}
        </div>
      </main>
    </div>
  );
};

function App() {
  const themePreference = useWorkspaceStore(state => state.themePreference);

  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    if (themePreference === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      root.classList.add(systemTheme);
    } else {
      root.classList.add(themePreference);
    }
  }, [themePreference]);

  const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID || "YOUR_GOOGLE_CLIENT_ID";

  return (
    <GoogleOAuthProvider clientId={googleClientId}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          
          <Route path="/" element={
            <ProtectedRoute>
              <AppShell><MainLayout /></AppShell>
            </ProtectedRoute>
          } />
          
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <AppShell><UserPortal /></AppShell>
            </ProtectedRoute>
          } />
          
          <Route path="/reports" element={
            <ProtectedRoute>
              <AppShell><LPStudio /></AppShell>
            </ProtectedRoute>
          } />
          
          <Route path="/admin" element={
            <ProtectedRoute requiredRole="ADMIN">
              <AppShell><AdminPortal /></AppShell>
            </ProtectedRoute>
          } />
          
        </Routes>
      </Router>
    </GoogleOAuthProvider>
  );
}

export default App;
