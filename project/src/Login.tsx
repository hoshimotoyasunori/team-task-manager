import React, { useState } from 'react';
import axios from 'axios';

const Login: React.FC = () => {
  const [employeeNumber, setEmployeeNumber] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('/api/token/', {
        username: employeeNumber,
        password,
      });
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        // 必要に応じてリダイレクトや状態更新
        window.location.href = '/';
      } else {
        setError(response.data.non_field_errors ? response.data.non_field_errors[0] : 'ログインに失敗しました');
      }
    } catch (err) {
      setError('通信エラーが発生しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '80px auto', padding: 32, boxShadow: '0 2px 8px #eee', borderRadius: 8, background: '#fff' }}>
      <h2 style={{ textAlign: 'center' }}>ログイン</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 16 }}>
          <label>社員番号</label>
          <input
            type="text"
            value={employeeNumber}
            onChange={e => setEmployeeNumber(e.target.value)}
            required
            style={{ width: '100%', padding: 8, marginTop: 4 }}
            autoFocus
          />
        </div>
        <div style={{ marginBottom: 16 }}>
          <label>パスワード</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            style={{ width: '100%', padding: 8, marginTop: 4 }}
          />
        </div>
        {error && <div style={{ color: 'red', marginBottom: 16 }}>{error}</div>}
        <button type="submit" style={{ width: '100%', padding: 10, background: '#1976d2', color: '#fff', border: 'none', borderRadius: 4 }} disabled={loading}>
          {loading ? 'ログイン中...' : 'ログイン'}
        </button>
      </form>
    </div>
  );
};

export default Login; 