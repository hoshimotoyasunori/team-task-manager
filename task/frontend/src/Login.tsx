import React, { useState } from 'react';
import { login } from './api/auth';

const Login: React.FC<{ onLogin: () => void }> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const data = await login(username, password);
      localStorage.setItem('accessToken', data.access);
      localStorage.setItem('refreshToken', data.refresh);
      onLogin();
    } catch (err) {
      setError('ログインに失敗しました');
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f5f7fa' }}>
      <form onSubmit={handleSubmit} style={{ background: '#fff', borderRadius: 14, boxShadow: '0 2px 16px #0002', padding: '40px 32px', minWidth: 340, width: 360, display: 'flex', flexDirection: 'column', gap: 22 }}>
        <div style={{ textAlign: 'center', marginBottom: 8 }}>
          <div style={{ fontWeight: 700, fontSize: 28, color: '#1976d2', marginBottom: 6 }}>TaskBoard</div>
          <div style={{ color: '#888', fontSize: 15 }}>ログイン</div>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <label style={{ fontWeight: 500, fontSize: 15 }}>ユーザー名</label>
          <input value={username} onChange={e => setUsername(e.target.value)} style={{ fontSize: 16, padding: '8px 12px', borderRadius: 7, border: '1px solid #bbb' }} autoFocus />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, position: 'relative' }}>
          <label style={{ fontWeight: 500, fontSize: 15 }}>パスワード</label>
          <input
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={e => setPassword(e.target.value)}
            style={{ fontSize: 16, padding: '8px 38px 8px 12px', borderRadius: 7, border: '1px solid #bbb' }}
          />
          <button
            type="button"
            onClick={() => setShowPassword(v => !v)}
            style={{ position: 'absolute', right: 10, top: 32, background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}
            tabIndex={-1}
            aria-label={showPassword ? 'パスワードを非表示' : 'パスワードを表示'}
          >
            {showPassword ? (
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z" stroke="#888" strokeWidth="2"/><circle cx="12" cy="12" r="3" stroke="#888" strokeWidth="2"/></svg>
            ) : (
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M17.94 17.94C16.11 19.25 14.13 20 12 20c-7 0-11-8-11-8a21.77 21.77 0 0 1 5.06-6.06M9.53 9.53A3.001 3.001 0 0 0 12 15a3 3 0 0 0 2.47-5.47" stroke="#888" strokeWidth="2"/><path d="m1 1 22 22" stroke="#888" strokeWidth="2"/></svg>
            )}
          </button>
        </div>
        <button type="submit" style={{ background: '#1976d2', color: '#fff', border: 'none', borderRadius: 7, padding: '12px 0', fontSize: 17, fontWeight: 600, marginTop: 8, cursor: 'pointer', letterSpacing: 1 }}>ログイン</button>
        {error && <div style={{ color: '#d32f2f', fontWeight: 500, textAlign: 'center', marginTop: 6 }}>{error}</div>}
      </form>
    </div>
  );
};

export default Login; 