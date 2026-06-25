import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export const Login = () => {
  const login = useAuthStore(state => state.login);
  const navigate = useNavigate();

  const handleSuccess = async (credentialResponse) => {
    try {
      const response = await fetch('http://localhost:8000/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ credential: credentialResponse.credential })
      });
      const data = await response.json();
      if (data.status === 'SUCCESS') {
        login(data.user);
        navigate('/');
      }
    } catch (err) {
      console.error('Login failed', err);
    }
  };

  return (
    <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--bg-primary)' }}>
      <div className="glass-panel" style={{ padding: '40px', width: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '24px' }}>
        <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: 'linear-gradient(135deg, var(--accent-color), #8b5cf6)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold', fontSize: '1.5rem' }}>S</div>
        <div style={{ textAlign: 'center' }}>
          <h2 style={{ margin: 0, fontWeight: 600 }}>Sign in to Sbecipher</h2>
          <p style={{ margin: '8px 0 0 0', color: 'var(--text-secondary)' }}>Institutional Portfolio Management System</p>
        </div>
        <GoogleLogin
          onSuccess={handleSuccess}
          onError={() => console.log('Login Failed')}
          useOneTap
        />
      </div>
    </div>
  );
};
