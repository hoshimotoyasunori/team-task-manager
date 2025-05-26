import React, { useState } from 'react';
import Login from './Login';
import TaskList from './TaskList';
import GanttChart from './GanttChart';
import KanbanBoard from './KanbanBoard';
import Dashboard from './Dashboard';
import Home from './Home';
import './App.css';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate, useLocation } from 'react-router-dom';
import { fetchUserProfile, updateUserProfile, changePassword } from './api/user';
import TaskCreateModal from './TaskCreateModal';
import { fetchProjects } from './api/projects';
import { getUsers } from './api/user';

const ProfileModal: React.FC<{ open: boolean, onClose: () => void, profile: any, onSave: (data: any) => void, onChangePassword: (current: string, newPass: string) => void }> = ({ open, onClose, profile, onSave, onChangePassword }) => {
  const [bio, setBio] = React.useState(profile?.bio || '');
  const [department, setDepartment] = React.useState(profile?.department || '');
  const [currentPassword, setCurrentPassword] = React.useState('');
  const [newPassword, setNewPassword] = React.useState('');
  const [tab, setTab] = React.useState<'profile' | 'password'>('profile');
  const [error, setError] = React.useState('');
  const [success, setSuccess] = React.useState('');
  React.useEffect(() => {
    setBio(profile?.bio || '');
    setDepartment(profile?.department || '');
    setError('');
    setSuccess('');
  }, [profile, open]);
  if (!open) return null;
  return (
    <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(0,0,0,0.25)', zIndex: 2000, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ background: '#fff', borderRadius: 18, boxShadow: '0 4px 32px #0003', minWidth: 340, width: 380, padding: '36px 32px 28px', position: 'relative' }}>
        {/* 閉じるボタン */}
        <button onClick={onClose} style={{ position: 'absolute', right: 18, top: 18, background: 'none', border: 'none', fontSize: 22, color: '#888', cursor: 'pointer' }} aria-label="閉じる">×</button>
        {/* タイトル */}
        <div style={{ textAlign: 'center', marginBottom: 18 }}>
          <div style={{ fontWeight: 700, fontSize: 22, color: '#1976d2' }}>プロフィール</div>
        </div>
        {/* タブ切り替え */}
        <div style={{ display: 'flex', gap: 16, marginBottom: 18, justifyContent: 'center' }}>
          <button onClick={() => setTab('profile')} style={{ fontWeight: tab === 'profile' ? 700 : 400, fontSize: 16, padding: '8px 20px', borderRadius: 7, border: tab === 'profile' ? '2px solid #1976d2' : '1px solid #bbb', background: tab === 'profile' ? '#e3f2fd' : '#f5f7fa', color: tab === 'profile' ? '#1976d2' : '#333', cursor: 'pointer', transition: 'all 0.2s' }}>プロフィール編集</button>
          <button onClick={() => setTab('password')} style={{ fontWeight: tab === 'password' ? 700 : 400, fontSize: 16, padding: '8px 20px', borderRadius: 7, border: tab === 'password' ? '2px solid #1976d2' : '1px solid #bbb', background: tab === 'password' ? '#e3f2fd' : '#f5f7fa', color: tab === 'password' ? '#1976d2' : '#333', cursor: 'pointer', transition: 'all 0.2s' }}>パスワード変更</button>
        </div>
        {tab === 'profile' && (
          <form onSubmit={e => { e.preventDefault(); if (!bio.trim()) { setError('自己紹介は必須です'); setSuccess(''); return; } setError(''); setSuccess('保存しました'); onSave({ bio, department }); }} style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
            <div style={{ width: '100%' }}>
              <label style={{ fontWeight: 500, fontSize: 15, marginBottom: 4, display: 'block' }}>自己紹介</label>
              <textarea value={bio} onChange={e => setBio(e.target.value)} style={{ width: '100%', fontSize: 16, padding: '9px 12px', borderRadius: 8, border: '1px solid #bbb', background: '#f7fafd', minHeight: 60, boxSizing: 'border-box' }} />
            </div>
            <div style={{ width: '100%' }}>
              <label style={{ fontWeight: 500, fontSize: 15, marginBottom: 4, display: 'block' }}>部署</label>
              <input value={department} onChange={e => setDepartment(e.target.value)} style={{ width: '100%', fontSize: 16, padding: '9px 12px', borderRadius: 8, border: '1px solid #bbb', background: '#f7fafd', boxSizing: 'border-box' }} />
            </div>
            {error && <div style={{ color: '#d32f2f', fontWeight: 500, textAlign: 'center' }}>{error}</div>}
            {success && <div style={{ color: '#388e3c', fontWeight: 500, textAlign: 'center' }}>{success}</div>}
            <div style={{ display: 'flex', gap: 12, marginTop: 8 }}>
              <button type="submit" style={{ flex: 1, background: '#1976d2', color: '#fff', border: 'none', borderRadius: 8, padding: '12px 0', fontSize: 16, fontWeight: 600, cursor: 'pointer' }}>保存</button>
              <button type="button" onClick={onClose} style={{ flex: 1, background: '#eee', color: '#555', border: 'none', borderRadius: 8, padding: '12px 0', fontSize: 16, fontWeight: 600, cursor: 'pointer' }}>キャンセル</button>
            </div>
          </form>
        )}
        {tab === 'password' && (
          <form onSubmit={e => { e.preventDefault(); if (!currentPassword || !newPassword) { setError('両方入力してください'); setSuccess(''); return; } setError(''); setSuccess('パスワードを変更しました'); onChangePassword(currentPassword, newPassword); }} style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
            <div>
              <label style={{ fontWeight: 500, fontSize: 15, marginBottom: 4, display: 'block' }}>現在のパスワード</label>
              <input type="password" value={currentPassword} onChange={e => setCurrentPassword(e.target.value)} style={{ width: '100%', fontSize: 16, padding: '9px 12px', borderRadius: 8, border: '1px solid #bbb', background: '#f7fafd' }} />
            </div>
            <div>
              <label style={{ fontWeight: 500, fontSize: 15, marginBottom: 4, display: 'block' }}>新しいパスワード</label>
              <input type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)} style={{ width: '100%', fontSize: 16, padding: '9px 12px', borderRadius: 8, border: '1px solid #bbb', background: '#f7fafd' }} />
            </div>
            {error && <div style={{ color: '#d32f2f', fontWeight: 500, textAlign: 'center' }}>{error}</div>}
            {success && <div style={{ color: '#388e3c', fontWeight: 500, textAlign: 'center' }}>{success}</div>}
            <div style={{ display: 'flex', gap: 12, marginTop: 8 }}>
              <button type="submit" style={{ flex: 1, background: '#1976d2', color: '#fff', border: 'none', borderRadius: 8, padding: '12px 0', fontSize: 16, fontWeight: 600, cursor: 'pointer' }}>変更</button>
              <button type="button" onClick={onClose} style={{ flex: 1, background: '#eee', color: '#555', border: 'none', borderRadius: 8, padding: '12px 0', fontSize: 16, fontWeight: 600, cursor: 'pointer' }}>キャンセル</button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

const Header: React.FC<{ username?: string; onLogout: () => void; onProfileClick: () => void }> = ({ username, onLogout, onProfileClick }) => (
  <header className="header">
    <div className="header-left">TaskBoard</div>
    <div className="header-right">
      {username && <span className="header-user" onClick={onProfileClick} style={{ cursor: 'pointer' }}>{username}</span>}
      <button className="header-logout" onClick={onLogout}>ログアウト</button>
    </div>
  </header>
);

const Sidebar: React.FC<{ onOpenCreate: () => void; sidebarOpen: boolean; setSidebarOpen: (open: boolean) => void }> = ({ onOpenCreate, sidebarOpen, setSidebarOpen }) => {
  const location = useLocation();
  const menu = [
    { label: 'ホーム', path: '/home', icon: '🏠' },
    { label: 'ダッシュボード', path: '/', icon: '📊' },
  ];
  const SIDEBAR_WIDTH = sidebarOpen ? 220 : 56;
  const TOGGLE_BTN_WIDTH = 36;
  const TOGGLE_BTN_HEIGHT = 72;
  return (
    <div style={{ position: 'relative', display: 'flex', height: '100vh' }}>
      {/* サイドバー本体 */}
      <nav
        className="sidebar"
        style={{
          width: SIDEBAR_WIDTH,
          transition: 'width 0.25s cubic-bezier(.4,0,.2,1)',
          overflow: 'hidden',
          position: 'relative',
          boxSizing: 'border-box',
          minHeight: '100vh',
          background: '#fff',
          borderRadius: '0 18px 18px 0',
          boxShadow: '2px 0 16px #0002',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'stretch',
        }}
      >
        {/* タスク作成ボタン */}
        <div style={{ display: 'flex', justifyContent: sidebarOpen ? 'flex-start' : 'center', alignItems: 'center', margin: '28px 0 18px 0', paddingLeft: sidebarOpen ? 18 : 0 }}>
          <button
            onClick={onOpenCreate}
            style={{
              background: '#1976d2',
              color: '#fff',
              border: 'none',
              borderRadius: '50%',
              width: 44,
              height: 44,
              fontSize: 26,
              fontWeight: 700,
              boxShadow: '0 2px 8px #0001',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'background 0.2s',
              marginRight: sidebarOpen ? 12 : 0,
            }}
            title="タスク作成"
            aria-label="タスク作成"
          >
            ＋
          </button>
          {sidebarOpen && <span style={{ fontSize: 17, fontWeight: 600, color: '#1976d2', marginLeft: 2, letterSpacing: 1 }}>タスク作成</span>}
        </div>
        {/* メニュー */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, flex: 1 }}>
          {menu.map(item => (
            <Link
              key={item.path}
              to={item.path}
              className={location.pathname === item.path ? 'active' : ''}
              style={{
                display: 'flex', alignItems: 'center', gap: 12, fontSize: 17, fontWeight: 500,
                padding: sidebarOpen ? '10px 18px' : '10px 0',
                borderRadius: 12,
                margin: '0 8px',
                transition: 'all 0.2s',
                justifyContent: sidebarOpen ? 'flex-start' : 'center',
                position: 'relative',
                color: location.pathname === item.path ? '#1976d2' : '#333',
                background: location.pathname === item.path ? '#e3f2fd' : 'transparent',
                cursor: 'pointer',
                minHeight: 44,
              }}
              title={item.label}
            >
              <span style={{ fontSize: 22 }}>{item.icon}</span>
              {sidebarOpen && <span>{item.label}</span>}
              {/* 閉じている時はhoverでラベルを表示 */}
              {!sidebarOpen && (
                <span
                  style={{
                    position: 'absolute',
                    left: '110%',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: '#333',
                    color: '#fff',
                    borderRadius: 6,
                    fontSize: 14,
                    padding: '2px 12px',
                    whiteSpace: 'nowrap',
                    opacity: 0,
                    pointerEvents: 'none',
                    transition: 'opacity 0.2s',
                  }}
                  className="sidebar-tooltip"
                >
                  {item.label}
                </span>
              )}
            </Link>
          ))}
        </div>
        {/* トグルボタンをサイドバーの右端中央に縦長タブ型で配置 */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          style={{
            position: 'fixed',
            top: '50%',
            left: `calc(${SIDEBAR_WIDTH}px - ${TOGGLE_BTN_WIDTH / 2}px)`,
            transform: 'translateY(-50%)',
            background: '#fff',
            color: '#1976d2',
            border: '1.5px solid #e3eaf5',
            borderRadius: 18,
            width: TOGGLE_BTN_WIDTH,
            height: TOGGLE_BTN_HEIGHT,
            fontSize: 22,
            fontWeight: 700,
            boxShadow: '2px 2px 12px #0002',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 10000,
            cursor: 'pointer',
            transition: 'background 0.2s, color 0.2s',
            outline: 'none',
          }}
          title={sidebarOpen ? 'サイドバーを閉じる' : 'サイドバーを開く'}
          aria-label={sidebarOpen ? 'サイドバーを閉じる' : 'サイドバーを開く'}
        >
          {sidebarOpen ? '◀' : '▶'}
        </button>
      </nav>
      {/* ツールチップのhover表示用CSS（JSX内でstyleタグ追加） */}
      <style>{`
        .sidebar a:hover .sidebar-tooltip {
          opacity: 1;
          pointer-events: auto;
        }
      `}</style>
    </div>
  );
};

const Layout: React.FC<{ username?: string; onLogout: () => void; onProfileClick: () => void; children: React.ReactNode; onOpenCreate: () => void }> = ({ username, onLogout, onProfileClick, children, onOpenCreate }) => {
  const [sidebarOpen, setSidebarOpen] = React.useState(() => {
    const saved = localStorage.getItem('sidebarOpen');
    return saved === null ? true : saved === 'true';
  });
  React.useEffect(() => {
    localStorage.setItem('sidebarOpen', String(sidebarOpen));
  }, [sidebarOpen]);
  return (
    <div className="layout">
      <Header username={username} onLogout={onLogout} onProfileClick={onProfileClick} />
      <div className="layout-main">
        <Sidebar onOpenCreate={onOpenCreate} sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
        <main className="main-content" style={{ marginLeft: sidebarOpen ? 0 : 0, transition: 'all 0.2s' }}>{children}</main>
      </div>
    </div>
  );
};

const PageContainer: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div style={{ padding: 20 }}>
    {children}
  </div>
);

const AppRoutes: React.FC<{ onLogout: () => void, onLogin: () => void, isLoggedIn: boolean, username?: string, userId?: number, onProfileClick: () => void, onOpenCreate: () => void }> = ({ onLogout, onLogin, isLoggedIn, username, userId, onProfileClick, onOpenCreate }) => {
  const navigate = useNavigate();

  const handleLogin = () => {
    onLogin();
    navigate('/home');
  };

  if (!isLoggedIn) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <Layout username={username} onLogout={onLogout} onProfileClick={onProfileClick} onOpenCreate={onOpenCreate}>
      <Routes>
        <Route path="/" element={<PageContainer><Dashboard /></PageContainer>} />
        <Route path="/home" element={<PageContainer><Home username={username} userId={userId} /></PageContainer>} />
      </Routes>
    </Layout>
  );
};

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(() => !!localStorage.getItem('accessToken'));
  const [username, setUsername] = useState<string | undefined>(undefined);
  const [userId, setUserId] = useState<number | undefined>(undefined);
  const [profileModalOpen, setProfileModalOpen] = useState(false);
  const [profile, setProfile] = useState<any>(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [users, setUsers] = useState<{ id: number; username: string }[]>([]);
  const [projects, setProjects] = useState<{ id: number; name: string }[]>([]);

  React.useEffect(() => {
    if (isLoggedIn) {
      const token = localStorage.getItem('accessToken');
      if (token) {
        fetch('http://localhost:8000/api/me/', {
          headers: { 'Authorization': `Bearer ${token}` },
        })
          .then(res => res.ok ? res.json() : null)
          .then(data => {
            setUsername(data?.username || '');
            setUserId(data?.id);
            setProfile(data);
          });
        getUsers(token).then(setUsers).catch(() => setUsers([]));
        fetchProjects(token).then(setProjects).catch(() => setProjects([]));
      }
    } else {
      setUsername(undefined);
      setUserId(undefined);
      setProfile(null);
      setUsers([]);
      setProjects([]);
    }
  }, [isLoggedIn, profileModalOpen]);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setIsLoggedIn(false);
  };

  const handleProfileSave = async (data: any) => {
    const token = localStorage.getItem('accessToken');
    if (!token) return;
    try {
      await updateUserProfile(token, data);
      setProfile({ ...profile, ...data });
      setProfileModalOpen(false);
    } catch {
      alert('プロフィール更新に失敗しました');
    }
  };

  const handleChangePassword = async (current: string, newPass: string) => {
    const token = localStorage.getItem('accessToken');
    if (!token) return;
    try {
      await changePassword(token, current, newPass);
      alert('パスワードを変更しました');
      setProfileModalOpen(false);
    } catch (e: any) {
      alert(e.message || 'パスワード変更に失敗しました');
    }
  };

  const handleCreateTask = async (data: any) => {
    setCreateOpen(false);
  };

  return (
    <Router>
      <AppRoutes onLogout={handleLogout} onLogin={handleLogin} isLoggedIn={isLoggedIn} username={username} userId={userId} onProfileClick={() => setProfileModalOpen(true)} onOpenCreate={() => setCreateOpen(true)} />
      <ProfileModal open={profileModalOpen} onClose={() => setProfileModalOpen(false)} profile={profile} onSave={handleProfileSave} onChangePassword={handleChangePassword} />
      <TaskCreateModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onCreate={handleCreateTask}
        users={users}
        projects={projects}
      />
    </Router>
  );
};

export default App;
