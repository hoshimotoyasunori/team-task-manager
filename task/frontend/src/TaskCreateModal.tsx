import React, { useState } from 'react';

interface TaskCreateModalProps {
  open: boolean;
  onClose: () => void;
  onCreate: (data: any) => void;
  users: { id: number; username: string }[];
  projects: { id: number; name: string }[];
}

const TaskCreateModal: React.FC<TaskCreateModalProps> = ({ open, onClose, onCreate, users, projects }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [assignee, setAssignee] = useState<number | ''>('');
  const [project, setProject] = useState<number | ''>('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('タイトルは必須です');
      return;
    }
    if (startDate && endDate && startDate > endDate) {
      setError('開始日は終了日より前にしてください');
      return;
    }
    setError('');
    onCreate({ title, description, assignee: assignee || undefined, project: project || undefined, start_date: startDate || undefined, end_date: endDate || undefined });
    setTitle(''); setDescription(''); setAssignee(''); setProject(''); setStartDate(''); setEndDate('');
  };

  if (!open) return null;
  return (
    <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: '#0008', zIndex: 2000, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ background: '#fff', borderRadius: 12, padding: 32, minWidth: 340, minHeight: 220, boxShadow: '0 2px 16px #0002' }}>
        <h3 style={{ marginBottom: 18 }}>タスク新規作成</h3>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: 12 }}>
            <input value={title} onChange={e => setTitle(e.target.value)} placeholder="タイトル*" style={{ width: '100%', fontSize: 16, padding: 6, borderRadius: 6, border: '1px solid #bbb' }} maxLength={200} required />
          </div>
          <div style={{ marginBottom: 12 }}>
            <textarea value={description} onChange={e => setDescription(e.target.value)} placeholder="説明（任意）" style={{ width: '100%', fontSize: 15, padding: 6, borderRadius: 6, border: '1px solid #bbb', minHeight: 60 }} maxLength={1000} />
          </div>
          <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
            <select value={assignee} onChange={e => setAssignee(Number(e.target.value) || '')} style={{ flex: 1, fontSize: 15, padding: 6, borderRadius: 6, border: '1px solid #bbb' }}>
              <option value="">担当者（任意）</option>
              {users.map(u => (
                <option key={u.id} value={u.id}>{u.username}</option>
              ))}
            </select>
            <select value={project} onChange={e => setProject(Number(e.target.value) || '')} style={{ flex: 1, fontSize: 15, padding: 6, borderRadius: 6, border: '1px solid #bbb' }}>
              <option value="">プロジェクト（任意）</option>
              {projects.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
          <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
            <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} style={{ flex: 1, fontSize: 15, padding: 6, borderRadius: 6, border: '1px solid #bbb' }} />
            <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} style={{ flex: 1, fontSize: 15, padding: 6, borderRadius: 6, border: '1px solid #bbb' }} />
          </div>
          {error && <div style={{ color: '#d32f2f', fontWeight: 500, marginBottom: 8 }}>{error}</div>}
          <div style={{ display: 'flex', gap: 16, marginTop: 8 }}>
            <button type="submit" style={{ background: '#1976d2', color: '#fff', border: 'none', borderRadius: 4, padding: '8px 24px', cursor: 'pointer', fontSize: 16, fontWeight: 500 }}>作成</button>
            <button type="button" onClick={onClose} style={{ background: '#eee', color: '#333', border: 'none', borderRadius: 4, padding: '8px 24px', cursor: 'pointer', fontSize: 16, fontWeight: 500 }}>キャンセル</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TaskCreateModal; 