import React, { useEffect, useState } from 'react';
import { fetchTasks, createTask, updateTask, deleteTask } from './api/tasks';
import { fetchUserMe, getUsers } from './api/user';
import { fetchProjects } from './api/projects';

type Task = {
  id: number;
  title: string;
  description?: string;
  status: string;
  assignee?: number;
  start_date?: string;
  end_date?: string;
  assignee_name?: string;
  creator?: number;
  creator_name?: string;
  project?: number;
};

type User = {
  id: number;
  username: string;
};

type Project = {
  id: number;
  name: string;
};

interface TaskListProps {
  onlyMine?: boolean;
  hideAssigneeFilter?: boolean;
  username?: string;
  userId?: number;
  filterProject?: number | '';
  hideProjectFilter?: boolean;
  assigneeFilter?: string;
  setAssigneeFilter?: (v: string) => void;
}

const TaskList: React.FC<TaskListProps> = ({ onlyMine, hideAssigneeFilter, userId, filterProject: filterProjectProp, hideProjectFilter, assigneeFilter, setAssigneeFilter }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [error, setError] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [assignee, setAssignee] = useState<number | ''>('');
  const [loading, setLoading] = useState(false);
  const [editId, setEditId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editAssignee, setEditAssignee] = useState<number | ''>('');
  const [username, setUsername] = useState('');
  const [users, setUsers] = useState<User[]>([]);
  const [detailTask, setDetailTask] = useState<Task | null>(null);
  const [search, setSearch] = useState('');
  const [filterAssignee, setFilterAssignee] = useState<string>('');
  const [editStartDate, setEditStartDate] = useState('');
  const [editEndDate, setEditEndDate] = useState('');
  const [projects, setProjects] = useState<Project[]>([]);
  const [filterProject, setFilterProject] = useState<number | ''>(filterProjectProp ?? '');
  const [project, setProject] = useState<number | ''>('');
  const [editProject, setEditProject] = useState<number | ''>('');

  const loadTasks = () => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      setError('認証トークンがありません');
      return;
    }
    fetchTasks(token, filterProject)
      .then(rawTasks => {
        const tasksWithNames = rawTasks.map((task: any) => ({
          ...task,
          assignee_name: users.find(u => u.id === task.assignee)?.username || '',
          creator_name: users.find(u => u.id === task.creator)?.username || '',
        }));
        setTasks(tasksWithNames);
      })
      .catch(() => setError('タスク取得に失敗しました'));
  };

  useEffect(() => {
    setFilterProject(filterProjectProp ?? '');
  }, [filterProjectProp]);

  useEffect(() => {
    loadTasks();
    const token = localStorage.getItem('accessToken');
    if (token) {
      fetchUserMe(token)
        .then(user => setUsername(user.username))
        .catch(() => setUsername(''));
      getUsers(token)
        .then(setUsers)
        .catch(() => setUsers([]));
      fetchProjects(token)
        .then(setProjects)
        .catch(() => setProjects([]));
    }
    // eslint-disable-next-line
  }, [filterProject]);

  useEffect(() => {
    if (assigneeFilter !== undefined && setAssigneeFilter) {
      setFilterAssignee(assigneeFilter === 'all' ? '' : assigneeFilter);
    }
  }, [assigneeFilter]);

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    const token = localStorage.getItem('accessToken');
    if (!token) {
      setError('認証トークンがありません');
      setLoading(false);
      return;
    }
    try {
      await createTask(token, { title, description, assignee: assignee || undefined, project: project || undefined });
      setTitle('');
      setDescription('');
      setAssignee('');
      setProject('');
      loadTasks();
    } catch (err: any) {
      setError(err instanceof Error ? err.message : 'タスク作成に失敗しました');
    }
    setLoading(false);
  };

  const handleEdit = (task: Task) => {
    setEditId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setEditAssignee(task.assignee || '');
    setEditStartDate(task.start_date || '');
    setEditEndDate(task.end_date || '');
    setEditProject(task.project || '');
  };

  const handleUpdateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (editId === null) return;
    setLoading(true);
    setError('');
    const token = localStorage.getItem('accessToken');
    if (!token) {
      setError('認証トークンがありません');
      setLoading(false);
      return;
    }
    try {
      await updateTask(token, editId, {
        title: editTitle,
        description: editDescription,
        assignee: editAssignee || undefined,
        start_date: editStartDate || undefined,
        end_date: editEndDate || undefined,
        project: editProject || undefined,
      });
      setEditId(null);
      setEditTitle('');
      setEditDescription('');
      setEditAssignee('');
      setEditStartDate('');
      setEditEndDate('');
      setEditProject('');
      loadTasks();
    } catch {
      setError('タスク編集に失敗しました');
    }
    setLoading(false);
  };

  const handleDeleteTask = async (id: number) => {
    if (!window.confirm('本当に削除しますか？')) return;
    setLoading(true);
    setError('');
    const token = localStorage.getItem('accessToken');
    if (!token) {
      setError('認証トークンがありません');
      setLoading(false);
      return;
    }
    try {
      await deleteTask(token, id);
      loadTasks();
    } catch {
      setError('タスク削除に失敗しました');
    }
    setLoading(false);
  };

  // フィルタ・検索適用後のタスクリスト
  const filteredTasks = tasks.filter(task => {
    const matchAssignee = filterAssignee === '' || String(task.assignee) === filterAssignee;
    let matchMine = true;
    if (onlyMine && userId !== undefined) {
      matchMine = task.assignee === userId;
    }
    return matchAssignee && matchMine;
  });

  const statusBadge = (status: string) => {
    let color = '#aaa';
    let label = '';
    switch (status) {
      case 'todo':
        color = '#1976d2'; label = 'ToDo'; break;
      case 'in_progress':
        color = '#ffa000'; label = 'In Progress'; break;
      case 'done':
        color = '#388e3c'; label = 'Done'; break;
      default:
        label = status;
    }
    return <span style={{ background: color, color: '#fff', borderRadius: 8, padding: '2px 8px', marginLeft: 8, fontSize: 12 }}>{label}</span>;
  };

  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <div style={{ marginBottom: 12 }}>
        {!hideProjectFilter && (
          <select value={filterProject} onChange={e => setFilterProject(Number(e.target.value) || '')} style={{ marginRight: 8 }}>
            <option value="">全プロジェクト</option>
            {projects.map(p => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        )}
        {!hideAssigneeFilter && (
          <select value={filterAssignee} onChange={e => {
            setFilterAssignee(e.target.value);
            if (setAssigneeFilter) setAssigneeFilter(e.target.value);
          }}>
            <option value="">全員（担当者で絞り込まない）</option>
            {users.map(user => (
              <option key={user.id} value={String(user.id)}>{user.username}</option>
            ))}
          </select>
        )}
      </div>
      <ul>
        {filteredTasks.map(task => (
          <li key={task.id}>
            {editId === task.id ? (
              <form onSubmit={handleUpdateTask} style={{ display: 'inline' }}>
                <input
                  value={editTitle}
                  onChange={e => setEditTitle(e.target.value)}
                  required
                />
                <input
                  value={editDescription}
                  onChange={e => setEditDescription(e.target.value)}
                />
                <select value={editAssignee} onChange={e => setEditAssignee(Number(e.target.value) || '')}>
                  <option value="">担当者（任意）</option>
                  {users.map(user => (
                    <option key={user.id} value={user.id}>{user.username}</option>
                  ))}
                </select>
                <select value={editProject} onChange={e => setEditProject(Number(e.target.value) || '')}>
                  <option value="">プロジェクト（任意）</option>
                  {projects.map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
                <input
                  type="date"
                  value={editStartDate}
                  onChange={e => setEditStartDate(e.target.value)}
                  style={{ marginLeft: 8 }}
                  required
                />
                <input
                  type="date"
                  value={editEndDate}
                  onChange={e => setEditEndDate(e.target.value)}
                  style={{ marginLeft: 4 }}
                  required
                />
                <button type="submit" disabled={loading}>保存</button>
                <button type="button" onClick={() => setEditId(null)}>キャンセル</button>
              </form>
            ) : (
              <>
                <span
                  style={{
                    cursor: 'pointer', textDecoration: task.status === 'done' ? 'line-through' : 'underline',
                    color: task.status === 'done' ? '#888' : undefined
                  }}
                  onClick={() => setDetailTask(task)}
                >
                  {task.title}
                </span>
                {statusBadge(task.status)}
                {task.description && <> - {task.description}</>}
                {task.assignee && (
                  <span style={{ marginLeft: 8, color: '#555' }}>
                    担当: {users.find(u => u.id === task.assignee)?.username || task.assignee}
                  </span>
                )}
                {task.project && (
                  <span style={{ marginLeft: 8, color: '#888', fontSize: 12 }}>
                    プロジェクト: {projects.find(p => p.id === task.project)?.name || task.project}
                  </span>
                )}
                {task.start_date && (
                  <span style={{ marginLeft: 8, color: '#888', fontSize: 12 }}>
                    開始: {task.start_date}
                  </span>
                )}
                {task.end_date && (
                  <span style={{ marginLeft: 8, color: '#888', fontSize: 12 }}>
                    終了: {task.end_date}
                  </span>
                )}
                <button onClick={() => handleEdit(task)} style={{ marginLeft: 8 }}>編集</button>
                <button onClick={() => handleDeleteTask(task.id)} style={{ marginLeft: 4 }}>削除</button>
              </>
            )}
          </li>
        ))}
      </ul>
      {detailTask && (
        <div style={{
          position: 'fixed', left: 0, top: 0, width: '100vw', height: '100vh',
          background: 'rgba(0,0,0,0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center',
        }} onClick={() => setDetailTask(null)}>
          <div style={{ background: '#fff', padding: 24, borderRadius: 8, minWidth: 300 }} onClick={e => e.stopPropagation()}>
            <h3>タスク詳細</h3>
            <div><b>タイトル:</b> {detailTask.title}</div>
            <div><b>説明:</b> {detailTask.description || '-'}</div>
            <div><b>ステータス:</b> {detailTask.status}</div>
            <div><b>担当者:</b> {users.find(u => u.id === detailTask.assignee)?.username || '-'}</div>
            <div><b>プロジェクト:</b> {projects.find(p => p.id === detailTask.project)?.name || '-'}</div>
            <button onClick={() => setDetailTask(null)} style={{ marginTop: 16 }}>閉じる</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskList; 