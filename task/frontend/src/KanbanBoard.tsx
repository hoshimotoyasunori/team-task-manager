import React, { useEffect, useState } from 'react';
import { fetchTasks, updateTask, deleteTask } from './api/tasks';
import { getUsers, fetchUserMe } from './api/user';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { fetchProjects } from './api/projects';

// タスク型
type Task = {
  id: number;
  title: string;
  description?: string;
  status: string;
  assignee?: number;
  assignee_name?: string; // 担当者名（APIで取得できる場合）
  creator?: number;
  creator_name?: string; // 作成者名（APIで取得できる場合）
  start_date?: string;
  end_date?: string;
};

interface User {
  id: number;
  username: string;
}

type Project = { id: number; name: string };

const statusLabels: { [key: string]: string } = {
  not_started: '未着手',
  in_progress: '進行中',
  review: 'レビュー待ち',
  done: '完了',
};
const statusColors: { [key: string]: string } = {
  not_started: '#90a4ae', // グレー
  in_progress: '#1976d2', // 青
  review: '#fbc02d', // 黄
  done: '#43a047', // 緑
};
const statusOrder = ['not_started', 'in_progress', 'review', 'done'];

// 担当者名から色を決定する関数（hashで色を割り当て）
const getAssigneeColor = (name: string | undefined) => {
  if (!name) return '#bdbdbd';
  // 色パレット
  const palette = ['#1976d2', '#43a047', '#fbc02d', '#e64a19', '#6a1b9a', '#00838f', '#c2185b', '#7b1fa2', '#388e3c', '#f57c00'];
  let hash = 0;
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);
  return palette[Math.abs(hash) % palette.length];
};

interface KanbanBoardProps {
  onlyMine?: boolean;
  hideAssigneeFilter?: boolean;
  username?: string;
  userId?: number;
  filterProject?: number | '';
  hideProjectFilter?: boolean;
  assigneeFilter?: string;
  setAssigneeFilter?: (v: string) => void;
}

const KanbanBoard: React.FC<KanbanBoardProps> = ({ onlyMine, hideAssigneeFilter, userId, filterProject: filterProjectProp, hideProjectFilter, assigneeFilter, setAssigneeFilter }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [detailTask, setDetailTask] = useState<Task | null>(null); // 詳細モーダル用
  const [assigneeFilterState, setAssigneeFilterState] = useState<string>('all');
  const [editTask, setEditTask] = useState<Task | null>(null); // 編集モーダル用
  const [users, setUsers] = useState<User[]>([]);
  const [editForm, setEditForm] = useState<any>(null);
  const [editError, setEditError] = useState<string>('');
  const [username, setUsername] = useState('');
  const [projects, setProjects] = useState<Project[]>([]);
  const [filterProject, setFilterProject] = useState<number | ''>(filterProjectProp ?? '');

  useEffect(() => {
    setFilterProject(filterProjectProp ?? '');
  }, [filterProjectProp]);

  useEffect(() => {
    loadTasks();
    const token = localStorage.getItem('accessToken');
    if (token) {
      getUsers(token).then(setUsers).catch(() => setUsers([]));
      fetchUserMe(token)
        .then(user => setUsername(user.username))
        .catch(() => setUsername(''));
      fetchProjects(token)
        .then(setProjects)
        .catch(() => setProjects([]));
    }
  }, [filterProject]);

  useEffect(() => {
    if (assigneeFilter !== undefined && setAssigneeFilter) {
      setAssigneeFilterState(assigneeFilter);
    }
  }, [assigneeFilter]);

  const loadTasks = () => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      setError('認証トークンがありません');
      return;
    }
    fetchTasks(token, filterProject)
      .then(setTasks)
      .catch(() => setError('タスク取得に失敗しました'));
  };

  // タスクに担当者名・作成者名を付与
  const tasksWithNames: Task[] = tasks.map(task => ({
    ...task,
    assignee_name: users.find(u => u.id === task.assignee)?.username || '',
    creator_name: users.find(u => u.id === task.creator)?.username || '',
  }));

  // onlyMineがtrueなら自分のタスクのみ
  const filteredTasks = onlyMine && userId !== undefined
    ? tasksWithNames.filter(t => t.assignee != null && userId != null && Number(t.assignee) === Number(userId))
    : tasksWithNames;

  // デバッグ用: userIdとfilteredTasksを画面に一時表示
  // 本番では削除してください
  // if (error) return <div style={{ color: 'red' }}>{error}</div>;

  // 担当者一覧を取得（重複なし）
  const assignees = Array.from(
    new Set(filteredTasks.filter(t => t.assignee_name).map(t => t.assignee_name!))
  );

  // ステータスごとにタスクをグループ化（フィルター適用）
  const grouped: { [key: string]: Task[] } = { not_started: [], in_progress: [], review: [], done: [] };
  filteredTasks.forEach(task => {
    if (grouped[task.status]) {
      if (
        assigneeFilter === undefined ||
        assigneeFilter === 'all' ||
        (task.assignee_name && String(task.assignee_name) === String(assigneeFilter))
      ) {
        grouped[task.status].push(task);
      }
    }
  });

  const onDragEnd = async (result: any) => {
    const { source, destination, draggableId } = result;
    if (!destination) return;
    const sourceStatus = source.droppableId;
    const destStatus = destination.droppableId;
    if (sourceStatus === destStatus && source.index === destination.index) return;
    const taskId = Number(draggableId);
    const token = localStorage.getItem('accessToken');
    if (!token) return;
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;
    setLoading(true);
    try {
      await updateTask(token, taskId, {
        title: task.title,
        description: task.description,
        assignee: task.assignee,
        start_date: task.start_date,
        end_date: task.end_date,
        status: destStatus,
      });
      loadTasks();
    } finally {
      setLoading(false);
    }
  };

  // タスク削除（本実装）
  const handleDelete = async (task: Task) => {
    if (!window.confirm(`「${task.title}」を削除しますか？`)) return;
    const token = localStorage.getItem('accessToken');
    if (!token) {
      alert('認証トークンがありません');
      return;
    }
    setLoading(true);
    try {
      await deleteTask(token, task.id);
      loadTasks();
    } catch (e: any) {
      alert(e.message || '削除に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  // 編集（本実装）
  const handleEdit = (task: Task) => {
    setEditTask(task);
    setEditForm({
      title: task.title,
      description: task.description || '',
      assignee: task.assignee || '',
      start_date: task.start_date || '',
      end_date: task.end_date || '',
      status: task.status,
    });
    setEditError('');
  };

  const closeEditModal = () => {
    setEditTask(null);
    setEditForm(null);
    setEditError('');
  };

  const handleEditChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setEditForm((prev: any) => ({ ...prev, [name]: value }));
  };

  const handleEditSave = async () => {
    if (!editTask) return;
    // バリデーション
    if (!editForm.title.trim()) {
      setEditError('タイトルは必須です');
      return;
    }
    if (editForm.start_date && editForm.end_date && editForm.start_date > editForm.end_date) {
      setEditError('開始日は終了日より前にしてください');
      return;
    }
    setEditError('');
    setLoading(true);
    try {
      const token = localStorage.getItem('accessToken');
      if (!token) throw new Error('認証トークンがありません');
      await updateTask(token, editTask.id, {
        title: editForm.title,
        description: editForm.description,
        assignee: editForm.assignee || null,
        start_date: editForm.start_date || null,
        end_date: editForm.end_date || null,
        status: editForm.status,
      });
      closeEditModal();
      loadTasks();
    } catch (e: any) {
      setEditError(e.message || '保存に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  // モーダルを閉じる
  const closeModal = () => setDetailTask(null);

  // アイコンSVG
  const EditIcon = () => (
    <svg width="18" height="18" viewBox="0 0 20 20" fill="none"><path d="M14.7 2.29a1 1 0 0 1 1.42 0l1.59 1.59a1 1 0 0 1 0 1.42l-9.3 9.3-2.12.71.71-2.12 9.3-9.3z" stroke="#1976d2" strokeWidth="1.5"/><path d="M12.88 4.12l2.12 2.12" stroke="#1976d2" strokeWidth="1.5"/></svg>
  );
  const DeleteIcon = () => (
    <svg width="18" height="18" viewBox="0 0 20 20" fill="none"><path d="M6 6l8 8M6 14L14 6" stroke="#d32f2f" strokeWidth="1.5"/></svg>
  );

  // 担当者イニシャルバッジ
  const AssigneeBadge = ({ name }: { name?: string }) => {
    if (!name) return null;
    const color = getAssigneeColor(name);
    const initial = name.slice(0, 1).toUpperCase();
    return (
      <span style={{
        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
        width: 28, height: 28, borderRadius: '50%', background: color, color: '#fff', fontWeight: 700, fontSize: 15, marginRight: 6
      }} title={name}>{initial}</span>
    );
  };

  return (
    <>
      {/* ヘッダー部分は外部から受け取る形に変更予定 */}
      <DragDropContext onDragEnd={onDragEnd}>
        <div style={{ display: 'flex', gap: 24, padding: 0, overflowX: 'auto', background: '#fff', maxHeight: 'calc(100vh - 200px)', overflowY: 'auto' }}>
          {statusOrder.map(status => (
            <Droppable droppableId={String(status)} key={status} isDropDisabled={false} isCombineEnabled={false} ignoreContainerClipping={false}>
              {(provided: any, snapshot: any) => (
                <div
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                  style={{
                    width: 320,
                    minWidth: 320,
                    minHeight: 60,
                    background: snapshot.isDraggingOver ? '#e3f2fd' : '#fff',
                    borderRadius: 12,
                    boxShadow: '0 2px 12px #0001',
                    padding: 16,
                    boxSizing: 'border-box',
                    border: '1.5px solid #e3eaf5',
                    overflowY: 'auto',
                  }}
                >
                  <div style={{ fontWeight: 'bold', fontSize: 20, marginBottom: 12, color: statusColors[status], letterSpacing: 1, display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ display: 'inline-block', width: 12, height: 12, borderRadius: '50%', background: statusColors[status] }} />
                    {statusLabels[status]}
                  </div>
                  {grouped[status].map((task, idx) => (
                    <Draggable draggableId={String(task.id)} index={idx} key={task.id}>
                      {(provided: any, snapshot: any) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          style={{
                            marginBottom: 16,
                            background: '#fff',
                            borderLeft: `6px solid ${statusColors[task.status]}`,
                            borderRadius: 8,
                            boxShadow: snapshot.isDragging ? '0 8px 24px #1976d255' : '0 1px 6px #0002',
                            opacity: loading ? 0.5 : (snapshot.isDragging ? 1 : (snapshot.isDropAnimating ? 0.7 : 0.95)),
                            position: 'relative',
                            transition: 'margin 0.2s, box-shadow 0.2s, transform 0.2s, opacity 0.2s',
                            transform: snapshot.isDragging ? 'scale(1.05)' : 'none',
                            cursor: 'pointer',
                            filter: snapshot.isDragging ? 'none' : (snapshot.isDropAnimating ? 'blur(1px)' : 'none'),
                            minWidth: 0,
                            maxWidth: '100%',
                            width: 'auto',
                            boxSizing: 'border-box',
                            ...provided.draggableProps.style,
                          }}
                          onClick={e => {
                            if ((e.target as HTMLElement).closest('.task-action-btn')) return;
                            setDetailTask(task);
                          }}
                          onMouseEnter={e => (e.currentTarget.style.boxShadow = '0 4px 16px #1976d233')}
                          onMouseLeave={e => (e.currentTarget.style.boxShadow = snapshot.isDragging ? '0 8px 24px #1976d255' : '0 1px 6px #0002')}
                        >
                          {/* 編集・削除ボタン（アイコン化・右上） */}
                          <div style={{ position: 'absolute', top: 8, right: 12, display: 'flex', gap: 8, zIndex: 2 }}>
                            <button className="task-action-btn" onClick={e => { e.stopPropagation(); handleEdit(task); }} style={{
                              background: 'none', border: 'none', borderRadius: 4, padding: 2, cursor: 'pointer', marginRight: 2, width: 24, height: 24, display: 'flex', alignItems: 'center', justifyContent: 'center'
                            }} title="編集">
                              <EditIcon />
                            </button>
                            <button className="task-action-btn" onClick={e => { e.stopPropagation(); handleDelete(task); }} style={{
                              background: 'none', border: 'none', borderRadius: 4, padding: 2, cursor: 'pointer', width: 24, height: 24, display: 'flex', alignItems: 'center', justifyContent: 'center'
                            }} title="削除">
                              <DeleteIcon />
                            </button>
                          </div>
                          {/* 担当者イニシャルバッジ＋タスク名・日付のみ表示 */}
                          <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontWeight: 'bold', fontSize: 17, marginBottom: 4, paddingRight: 60, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                            <AssigneeBadge name={task.assignee_name} />
                            <span>{task.title}</span>
                          </div>
                          <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginTop: 6 }}>
                            {task.start_date && <span style={{ fontSize: 12, color: '#888' }}>開始: {task.start_date}</span>}
                            {task.end_date && <span style={{ fontSize: 12, color: '#888' }}>終了: {task.end_date}</span>}
                          </div>
                        </div>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          ))}
        </div>
      </DragDropContext>
      {/* タスク詳細モーダル */}
      {detailTask && (
        <div style={{
          position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(0,0,0,0.25)', zIndex: 1000,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }} onClick={closeModal}>
          <div style={{
            background: '#fff', borderRadius: 12, boxShadow: '0 8px 32px #0003', padding: 32, minWidth: 340, maxWidth: '90vw', position: 'relative',
          }} onClick={e => e.stopPropagation()}>
            <div style={{ position: 'absolute', top: 16, right: 16, cursor: 'pointer', fontSize: 22, color: '#888' }} onClick={closeModal} title="閉じる">×</div>
            <div style={{ fontWeight: 'bold', fontSize: 22, marginBottom: 12 }}>{detailTask.title}</div>
            <div style={{ marginBottom: 12, color: '#555' }}>{detailTask.description || <span style={{ color: '#bbb' }}>説明なし</span>}</div>
            <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
              <AssigneeBadge name={detailTask.assignee_name} />
              {detailTask.assignee_name && (
                <span style={{ background: '#f3e5f5', color: '#6a1b9a', borderRadius: 12, padding: '2px 10px', fontSize: 13, fontWeight: 500 }}>担当: {detailTask.assignee_name}</span>
              )}
              {detailTask.start_date && <span style={{ fontSize: 13, color: '#888' }}>開始: {detailTask.start_date}</span>}
              {detailTask.end_date && <span style={{ fontSize: 13, color: '#888' }}>終了: {detailTask.end_date}</span>}
            </div>
            <div style={{ display: 'flex', gap: 16, marginTop: 8 }}>
              <button onClick={() => handleEdit(detailTask)} style={{
                background: '#e3f2fd', border: 'none', borderRadius: 4, padding: '6px 18px', cursor: 'pointer', fontSize: 15, color: '#1976d2', fontWeight: 500
              }}>編集</button>
              <button onClick={() => handleDelete(detailTask)} style={{
                background: '#ffebee', border: 'none', borderRadius: 4, padding: '6px 18px', cursor: 'pointer', fontSize: 15, color: '#d32f2f', fontWeight: 500
              }}>削除</button>
            </div>
          </div>
        </div>
      )}
      {/* 編集モーダル */}
      {editTask && editForm && (
        <div style={{
          position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(0,0,0,0.25)', zIndex: 1100,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }} onClick={closeEditModal}>
          <div style={{
            background: '#fff', borderRadius: 12, boxShadow: '0 8px 32px #0003', padding: 32, minWidth: 360, maxWidth: '95vw', position: 'relative',
          }} onClick={e => e.stopPropagation()}>
            <div style={{ position: 'absolute', top: 16, right: 16, cursor: 'pointer', fontSize: 22, color: '#888' }} onClick={closeEditModal} title="閉じる">×</div>
            <div style={{ fontWeight: 'bold', fontSize: 20, marginBottom: 18 }}>タスク編集</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <label>
                タイトル<span style={{ color: '#d32f2f' }}>*</span><br />
                <input name="title" value={editForm.title} onChange={handleEditChange} style={{ width: '100%', fontSize: 16, padding: 6, borderRadius: 6, border: '1px solid #bbb' }} maxLength={200} required />
              </label>
              <label>
                説明<br />
                <textarea name="description" value={editForm.description} onChange={handleEditChange} style={{ width: '100%', fontSize: 15, padding: 6, borderRadius: 6, border: '1px solid #bbb', minHeight: 60 }} maxLength={1000} />
              </label>
              <label>
                担当者<br />
                <select name="assignee" value={editForm.assignee} onChange={handleEditChange} style={{ width: '100%', fontSize: 15, padding: 6, borderRadius: 6, border: '1px solid #bbb' }}>
                  <option value="">未割当</option>
                  {users.map(u => (
                    <option key={u.id} value={u.id}>{u.username}</option>
                  ))}
                </select>
              </label>
              <div style={{ display: 'flex', gap: 12 }}>
                <label style={{ flex: 1 }}>
                  開始日<br />
                  <input type="date" name="start_date" value={editForm.start_date} onChange={handleEditChange} style={{ width: '100%', fontSize: 15, padding: 6, borderRadius: 6, border: '1px solid #bbb' }} />
                </label>
                <label style={{ flex: 1 }}>
                  終了日<br />
                  <input type="date" name="end_date" value={editForm.end_date} onChange={handleEditChange} style={{ width: '100%', fontSize: 15, padding: 6, borderRadius: 6, border: '1px solid #bbb' }} />
                </label>
              </div>
              <label>
                ステータス<br />
                <select name="status" value={editForm.status} onChange={handleEditChange} style={{ width: '100%', fontSize: 15, padding: 6, borderRadius: 6, border: '1px solid #bbb' }}>
                  {statusOrder.map(s => (
                    <option key={s} value={s}>{statusLabels[s]}</option>
                  ))}
                </select>
              </label>
              {editError && <div style={{ color: '#d32f2f', fontWeight: 500 }}>{editError}</div>}
              <div style={{ display: 'flex', gap: 16, marginTop: 8 }}>
                <button onClick={handleEditSave} style={{
                  background: '#1976d2', color: '#fff', border: 'none', borderRadius: 4, padding: '8px 24px', cursor: 'pointer', fontSize: 16, fontWeight: 500
                }} disabled={loading}>保存</button>
                <button onClick={closeEditModal} style={{
                  background: '#eee', color: '#333', border: 'none', borderRadius: 4, padding: '8px 24px', cursor: 'pointer', fontSize: 16, fontWeight: 500
                }} disabled={loading}>キャンセル</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

// 型エラー抑制用
declare module 'react-beautiful-dnd';

export default KanbanBoard; 