import React from 'react';
import { useEffect, useState } from 'react';
import { Container, Typography, List, ListItem, ListItemText, CircularProgress, Alert, Paper, Link, ListItemButton, Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import api from './api';
import { BrowserRouter, Routes, Route, useNavigate, useParams } from 'react-router-dom';
import Login from './Login';
import Dashboard from './Dashboard';
import Cases from './Cases';
import CaseDetail from './CaseDetail';
import ProtectedRoute from './ProtectedRoute';
import Layout from './Layout';

interface Company {
  id: number;
  name: string;
  // 必要に応じて他のフィールドも追加
}

function CompanyList() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [open, setOpen] = useState(false);
  const [newCompanyName, setNewCompanyName] = useState('');
  const [creating, setCreating] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    setLoading(true);
    api.get<Company[] | { results: Company[] }>('/companies/')
      .then((res) => {
        if (Array.isArray(res.data)) {
          setCompanies(res.data);
        } else if (Array.isArray((res.data as any).results)) {
          setCompanies((res.data as any).results);
        } else {
          setCompanies([]);
        }
        setError('');
        setLoading(false);
      })
      .catch(() => {
        setError('データ取得に失敗しました');
        setLoading(false);
      });
  }, []);

  const handleOpen = () => {
    setNewCompanyName('');
    setOpen(true);
  };
  const handleClose = () => setOpen(false);

  const handleCreate = () => {
    if (!newCompanyName.trim()) return;
    setCreating(true);
    api.post<Company>('/companies/', { name: newCompanyName })
      .then(res => {
        setCompanies(prev => [...prev, res.data]);
        setOpen(false);
        setNewCompanyName('');
        setError('');
        setCreating(false);
      })
      .catch(() => {
        setError('会社の作成に失敗しました');
        setCreating(false);
      });
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>会社一覧</Typography>
        <Button variant="contained" color="primary" sx={{ mb: 2 }} onClick={handleOpen}>新規会社追加</Button>
        {loading && <CircularProgress />}
        {error && <Alert severity="error">{error}</Alert>}
        {!loading && !error && (
          <List>
            {companies.map((company: Company) => (
              <ListItem key={company.id} disablePadding>
                <ListItemButton onClick={() => navigate(`/companies/${company.id}`)}>
                  <ListItemText primary={company.name} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        )}
        <Dialog open={open} onClose={handleClose}>
          <DialogTitle>新規会社追加</DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="会社名"
              fullWidth
              value={newCompanyName}
              onChange={e => setNewCompanyName(e.target.value)}
              disabled={creating}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose} disabled={creating}>キャンセル</Button>
            <Button onClick={handleCreate} variant="contained" disabled={creating || !newCompanyName.trim()}>
              {creating ? '作成中...' : '作成'}
            </Button>
          </DialogActions>
        </Dialog>
      </Paper>
    </Container>
  );
}

function CompanyDetail() {
  const { id } = useParams<{ id: string }>();
  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;
    api.get<Company>(`/companies/${id}/`)
      .then((res) => {
        setCompany(res.data);
        setError('');
        setLoading(false);
      })
      .catch(() => {
        setError('詳細データ取得に失敗しました');
        setLoading(false);
      });
  }, [id]);

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>会社詳細</Typography>
        {loading && <CircularProgress />}
        {error && <Alert severity="error">{error}</Alert>}
        {!loading && !error && company && (
          <>
            <Typography>ID: {company.id}</Typography>
            <Typography>名前: {company.name}</Typography>
          </>
        )}
        <Link href="/" underline="hover">一覧に戻る</Link>
      </Paper>
    </Container>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout>
                <CompanyList />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/companies/:id"
          element={
            <ProtectedRoute>
              <Layout>
                <CompanyDetail />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/cases"
          element={
            <ProtectedRoute>
              <Layout>
                <Cases />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/cases/:id"
          element={
            <ProtectedRoute>
              <Layout>
                <CaseDetail />
              </Layout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App; 