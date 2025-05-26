import React, { useEffect, useState } from 'react';
import { Container, Typography, Paper, List, ListItem, ListItemText, CircularProgress, Alert, ListItemButton, Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, IconButton, DialogContentText, Select, MenuItem, InputLabel, FormControl, Checkbox, OutlinedInput } from '@mui/material';
import api from './api';
import { useNavigate } from 'react-router-dom';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import dayjs from 'dayjs';

interface Case {
  id: number;
  case_type: string;
  status: string;
  occurence_date: string;
  property: number;
  owner: number;
  assigned_sales: number | null;
  created_at: string;
  updated_at: string;
}

interface Owner { id: number; name: string; }
interface Property { id: number; address: string; }
interface User { id: number; employee_number: string; first_name: string; last_name: string; }
interface ConstructionType { id: number; name: string; }

// 案件種別・ステータスの選択肢
const CASE_TYPE_CHOICES = [
  { value: 'New', label: '新規' },
  { value: 'CS', label: 'CS' },
  // 必要に応じて追加
];
const CASE_STATUS_CHOICES = [
  { value: 'Appointment', label: 'アポ取得済' },
  { value: 'Surveyed', label: '調査/点検済' },
  { value: 'Negotiating', label: '商談中' },
  { value: 'Contracted', label: '契約済' },
  { value: 'InProgress', label: '施工中' },
  { value: 'Completed', label: '完了' },
  { value: 'Cancelled', label: '中止' },
  // 必要に応じて追加
];

const Cases: React.FC = () => {
  const [cases, setCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [open, setOpen] = useState(false);
  const [newCaseType, setNewCaseType] = useState('');
  const [newStatus, setNewStatus] = useState('');
  const [creating, setCreating] = useState(false);
  const [editOpen, setEditOpen] = useState(false);
  const [editCase, setEditCase] = useState<Case | null>(null);
  const [editCaseType, setEditCaseType] = useState('');
  const [editStatus, setEditStatus] = useState('');
  const [editLoading, setEditLoading] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deleteCase, setDeleteCase] = useState<Case | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const navigate = useNavigate();
  const [owners, setOwners] = useState<Owner[]>([]);
  const [properties, setProperties] = useState<Property[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [constructionTypes, setConstructionTypes] = useState<ConstructionType[]>([]);
  const [newOwner, setNewOwner] = useState<number | ''>('');
  const [newProperty, setNewProperty] = useState<number | ''>('');
  const [newAssignedSales, setNewAssignedSales] = useState<number | ''>('');
  const [newOccurenceDate, setNewOccurenceDate] = useState<string>('');
  const [newExpectedConstructionTypes, setNewExpectedConstructionTypes] = useState<number[]>([]);

  useEffect(() => {
    setLoading(true);
    api.get<Case[] | { results: Case[] }>('/cases/')
      .then(res => {
        if (Array.isArray(res.data)) {
          setCases(res.data);
        } else if (Array.isArray((res.data as any).results)) {
          setCases((res.data as any).results);
        } else {
          setCases([]);
        }
        setError('');
        setLoading(false);
      })
      .catch(() => {
        setError('案件データの取得に失敗しました');
        setLoading(false);
      });
    api.get<Owner[] | { results: Owner[] }>('/owners/').then(res => setOwners(Array.isArray(res.data) ? res.data : (res.data as any).results || [])).catch(() => {});
    api.get<Property[] | { results: Property[] }>('/properties/').then(res => setProperties(Array.isArray(res.data) ? res.data : (res.data as any).results || [])).catch(() => {});
    api.get<User[] | { results: User[] }>('/users/').then(res => setUsers(Array.isArray(res.data) ? res.data : (res.data as any).results || [])).catch(() => {});
    api.get<ConstructionType[] | { results: ConstructionType[] }>('/constructiontypes/').then(res => setConstructionTypes(Array.isArray(res.data) ? res.data : (res.data as any).results || [])).catch(() => {});
  }, []);

  const handleOpen = () => {
    setNewCaseType('');
    setNewStatus('');
    setNewOwner('');
    setNewProperty('');
    setNewAssignedSales('');
    setNewOccurenceDate(dayjs().format('YYYY-MM-DD'));
    setNewExpectedConstructionTypes([]);
    setOpen(true);
  };
  const handleClose = () => setOpen(false);

  // バリデーションエラーを日本語で分かりやすく変換する関数
  function parseApiError(err: any): string {
    if (err.response && err.response.data) {
      const data = err.response.data;
      if (typeof data === 'string') return data;
      if (typeof data === 'object') {
        let messages: string[] = [];
        for (const key in data) {
          if (Array.isArray(data[key])) {
            // choices系
            if (data[key][0]?.includes('is not a valid choice')) {
              if (key === 'case_type') messages.push('「案件種別」の値が不正です。選択肢から選んでください。');
              else if (key === 'status') messages.push('「ステータス」の値が不正です。選択肢から選んでください。');
              else messages.push(`${key}: ${data[key][0]}`);
            } else {
              messages.push(`${key}: ${data[key].join(' ')}`);
            }
          }
        }
        return messages.length ? messages.join('\n') : JSON.stringify(data);
      }
    }
    return '案件データの作成に失敗しました';
  }

  const handleCreate = () => {
    if (!newCaseType.trim() || !newStatus.trim() || !newOwner || !newProperty || !newAssignedSales || !newOccurenceDate) return;
    setCreating(true);
    api.post<Case>('/cases/', {
      case_type: newCaseType,
      status: newStatus,
      owner: newOwner,
      property: newProperty,
      assigned_sales: newAssignedSales,
      occurence_date: newOccurenceDate,
      expected_construction_types: newExpectedConstructionTypes,
    })
      .then(res => {
        setCases(prev => [...prev, res.data]);
        setOpen(false);
        setNewCaseType('');
        setNewStatus('');
        setNewOwner('');
        setNewProperty('');
        setNewAssignedSales('');
        setNewOccurenceDate('');
        setNewExpectedConstructionTypes([]);
        setError('');
        setCreating(false);
      })
      .catch((err) => {
        setError(parseApiError(err));
        setCreating(false);
      });
  };

  const handleEditOpen = (c: Case) => {
    setEditCase(c);
    setEditCaseType(c.case_type);
    setEditStatus(c.status);
    setEditOpen(true);
  };
  const handleEditClose = () => setEditOpen(false);
  const handleEditSave = () => {
    if (!editCase || !editCaseType.trim() || !editStatus.trim()) return;
    setEditLoading(true);
    api.put<Case>(`/cases/${editCase.id}/`, { case_type: editCaseType, status: editStatus })
      .then(res => {
        setCases(prev => prev.map(c => c.id === editCase.id ? res.data : c));
        setEditOpen(false);
        setEditCase(null);
        setEditCaseType('');
        setEditStatus('');
        setError('');
        setEditLoading(false);
      })
      .catch(() => {
        setError('案件の編集に失敗しました');
        setEditLoading(false);
      });
  };

  const handleDeleteOpen = (c: Case) => {
    setDeleteCase(c);
    setDeleteOpen(true);
  };
  const handleDeleteClose = () => setDeleteOpen(false);
  const handleDeleteConfirm = () => {
    if (!deleteCase) return;
    setDeleteLoading(true);
    api.delete(`/cases/${deleteCase.id}/`)
      .then(() => {
        setCases(prev => prev.filter(c => c.id !== deleteCase.id));
        setDeleteOpen(false);
        setDeleteCase(null);
        setError('');
        setDeleteLoading(false);
      })
      .catch(() => {
        setError('案件の削除に失敗しました');
        setDeleteLoading(false);
      });
  };

  return (
    <Container maxWidth="md" sx={{ mt: 8 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>案件一覧</Typography>
        <Button variant="contained" color="primary" sx={{ mb: 2 }} onClick={handleOpen}>新規案件追加</Button>
        {loading && <CircularProgress />}
        {error && <Alert severity="error">{error}</Alert>}
        {!loading && !error && (
          <List>
            {cases.map((c) => (
              <ListItem key={c.id} disablePadding
                secondaryAction={
                  <>
                    <IconButton edge="end" aria-label="edit" onClick={() => handleEditOpen(c)}><EditIcon /></IconButton>
                    <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteOpen(c)}><DeleteIcon /></IconButton>
                  </>
                }
              >
                <ListItemButton onClick={() => navigate(`/cases/${c.id}`)}>
                  <ListItemText primary={`#${c.id} ${c.case_type} - ${c.status}`} secondary={`発生日: ${c.occurence_date}`} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        )}
        <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
          <DialogTitle>新規案件追加</DialogTitle>
          <DialogContent>
            <FormControl fullWidth margin="dense">
              <InputLabel>案件種別</InputLabel>
              <Select
                value={newCaseType}
                onChange={e => setNewCaseType(e.target.value as string)}
                input={<OutlinedInput label="案件種別" />}
                disabled={creating}
              >
                {CASE_TYPE_CHOICES.map(opt => (
                  <MenuItem key={opt.value} value={opt.value}>{opt.label}</MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl fullWidth margin="dense">
              <InputLabel>ステータス</InputLabel>
              <Select
                value={newStatus}
                onChange={e => setNewStatus(e.target.value as string)}
                input={<OutlinedInput label="ステータス" />}
                disabled={creating}
              >
                {CASE_STATUS_CHOICES.map(opt => (
                  <MenuItem key={opt.value} value={opt.value}>{opt.label}</MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl fullWidth margin="dense">
              <InputLabel>オーナー</InputLabel>
              <Select
                value={newOwner}
                onChange={e => setNewOwner(e.target.value as number)}
                input={<OutlinedInput label="オーナー" />}
                disabled={creating}
              >
                {owners.map(o => <MenuItem key={o.id} value={o.id}>{o.name}</MenuItem>)}
              </Select>
            </FormControl>
            <FormControl fullWidth margin="dense">
              <InputLabel>物件</InputLabel>
              <Select
                value={newProperty}
                onChange={e => setNewProperty(e.target.value as number)}
                input={<OutlinedInput label="物件" />}
                disabled={creating}
              >
                {properties.map(p => <MenuItem key={p.id} value={p.id}>{p.address}</MenuItem>)}
              </Select>
            </FormControl>
            <FormControl fullWidth margin="dense">
              <InputLabel>担当営業</InputLabel>
              <Select
                value={newAssignedSales}
                onChange={e => setNewAssignedSales(e.target.value as number)}
                input={<OutlinedInput label="担当営業" />}
                disabled={creating}
              >
                {users.map(u => <MenuItem key={u.id} value={u.id}>{u.employee_number} {u.first_name} {u.last_name}</MenuItem>)}
              </Select>
            </FormControl>
            <TextField
              margin="dense"
              label="発生日"
              type="date"
              fullWidth
              value={newOccurenceDate}
              onChange={e => setNewOccurenceDate(e.target.value)}
              InputLabelProps={{ shrink: true }}
              disabled={creating}
            />
            <FormControl fullWidth margin="dense">
              <InputLabel>想定工事種別</InputLabel>
              <Select
                multiple
                value={newExpectedConstructionTypes}
                onChange={e => setNewExpectedConstructionTypes(typeof e.target.value === 'string' ? e.target.value.split(',').map(Number) : e.target.value as number[])}
                input={<OutlinedInput label="想定工事種別" />}
                renderValue={selected => constructionTypes.filter(ct => selected.includes(ct.id)).map(ct => ct.name).join(', ')}
                disabled={creating}
              >
                {constructionTypes.map(ct => (
                  <MenuItem key={ct.id} value={ct.id}>
                    <Checkbox checked={newExpectedConstructionTypes.indexOf(ct.id) > -1} />
                    <ListItemText primary={ct.name} />
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose} disabled={creating}>キャンセル</Button>
            <Button onClick={handleCreate} variant="contained" disabled={creating || !newCaseType.trim() || !newStatus.trim() || !newOwner || !newProperty || !newAssignedSales || !newOccurenceDate}>
              {creating ? '作成中...' : '作成'}
            </Button>
          </DialogActions>
        </Dialog>
        <Dialog open={editOpen} onClose={handleEditClose}>
          <DialogTitle>案件編集</DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="案件種別"
              fullWidth
              value={editCaseType}
              onChange={e => setEditCaseType(e.target.value)}
              disabled={editLoading}
            />
            <TextField
              margin="dense"
              label="ステータス"
              fullWidth
              value={editStatus}
              onChange={e => setEditStatus(e.target.value)}
              disabled={editLoading}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleEditClose} disabled={editLoading}>キャンセル</Button>
            <Button onClick={handleEditSave} variant="contained" disabled={editLoading || !editCaseType.trim() || !editStatus.trim()}>
              {editLoading ? '保存中...' : '保存'}
            </Button>
          </DialogActions>
        </Dialog>
        <Dialog open={deleteOpen} onClose={handleDeleteClose}>
          <DialogTitle>案件削除</DialogTitle>
          <DialogContent>
            <DialogContentText>本当に削除しますか？</DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleDeleteClose} disabled={deleteLoading}>キャンセル</Button>
            <Button onClick={handleDeleteConfirm} color="error" variant="contained" disabled={deleteLoading}>
              {deleteLoading ? '削除中...' : '削除'}
            </Button>
          </DialogActions>
        </Dialog>
        {error && (
          <Dialog open={Boolean(error)} onClose={() => setError('')}>
            <DialogTitle>エラー</DialogTitle>
            <DialogContent>
              <DialogContentText>{error}</DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setError('')}>閉じる</Button>
            </DialogActions>
          </Dialog>
        )}
      </Paper>
    </Container>
  );
};

export default Cases; 