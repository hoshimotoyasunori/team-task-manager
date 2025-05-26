import React, { useEffect, useState, useRef } from 'react';
import { fetchTasks } from './api/tasks';
import { getUsers } from './api/user';
import { fetchUserMe } from './api/user';
import { fetchProjects } from './api/projects';

// タスク型
type Task = {
  id: number;
  title: string;
  start_date?: string;
  end_date?: string;
  status: string;
  assignee?: number;
  assignee_name?: string;
  creator?: number;
  creator_name?: string;
  project_name?: string;
};

type User = {
  id: number;
  username: string;
};

type Project = { id: number; name: string };

// 日付差分（日数）を計算
function dateDiffInDays(a: string, b: string): number {
  return Math.floor((new Date(b).getTime() - new Date(a).getTime()) / (1000 * 60 * 60 * 24));
}

// ステータス色・ラベル
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

interface GanttChartProps {
  onlyMine?: boolean;
  hideAssigneeFilter?: boolean;
  username?: string;
  userId?: number;
  filterProject?: number | '';
  hideProjectFilter?: boolean;
  assigneeFilter?: string;
  setAssigneeFilter?: (v: string) => void;
  groupBy?: 'assignee' | 'project' | 'none';
}

const GanttChart: React.FC<GanttChartProps> = ({ onlyMine, hideAssigneeFilter, userId, filterProject: filterProjectProp, hideProjectFilter, assigneeFilter, setAssigneeFilter }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState('');
  const [minDate, setMinDate] = useState<string>('');
  const [maxDate, setMaxDate] = useState<string>('');
  const [assigneeFilterState, setAssigneeFilterState] = useState<string>('all');
  const [username, setUsername] = useState('');
  const [projects, setProjects] = useState<Project[]>([]);
  const [filterProject, setFilterProject] = useState<number | ''>(filterProjectProp ?? '');
  const ganttAreaRef = useRef<HTMLDivElement>(null);
  const [ganttWidth, setGanttWidth] = useState<number>(800);
  const ganttScrollRef = useRef<HTMLDivElement>(null);

  // filterProjectPropが変化したときにfilterProjectを更新
  useEffect(() => {
    setFilterProject(filterProjectProp ?? '');
  }, [filterProjectProp]);

  // filterProjectが変化したときにタスクを再取得
  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      setError('認証トークンがありません');
      return;
    }
    fetchTasks(token, filterProject)
      .then((data) => setTasks(data))
      .catch(() => setError('タスク取得に失敗しました'));
    getUsers(token)
      .then(setUsers)
      .catch(() => setUsers([]));
    fetchUserMe(token)
      .then(user => setUsername(user.username))
      .catch(() => setUsername(''));
    fetchProjects(token)
      .then(setProjects)
      .catch(() => setProjects([]));
  }, [filterProject]);

  // タスクに担当者名・作成者名を付与
  const tasksWithAssignee: Task[] = tasks.map(task => ({
    ...task,
    assignee_name: users.find(u => u.id === task.assignee)?.username || '',
    creator_name: users.find(u => u.id === task.creator)?.username || '',
  }));

  // onlyMineがtrueなら自分のタスクのみ
  const filteredTasks = onlyMine && userId !== undefined
    ? tasksWithAssignee.filter(t => t.assignee != null && userId != null && Number(t.assignee) === Number(userId))
    : tasksWithAssignee;

  // デバッグ用: userIdとfilteredTasksを画面に一時表示
  // 本番では削除してください
  // console.log('userId:', userId);
  // console.log('filteredTasks:', filteredTasks);

  // 担当者一覧（重複なし）
  const assignees = Array.from(new Set(filteredTasks.map(t => t.assignee_name).filter(Boolean)));

  // 日付範囲計算
  React.useEffect(() => {
    const validTasks = filteredTasks.filter((t: Task) => t.start_date && t.end_date);
    if (validTasks.length > 0) {
      const min = validTasks.reduce((a, b) => (a.start_date! < b.start_date! ? a : b) as Task).start_date!;
      const max = validTasks.reduce((a, b) => (a.end_date! > b.end_date! ? a : b) as Task).end_date!;
      setMinDate(min);
      setMaxDate(max);
    }
  }, [filteredTasks]);

  // タスクをプロジェクトごとにグループ化
  const groupedByProject: { project: string; tasks: Task[] }[] = [];
  const projectMap = new Map<string, Task[]>();
  filteredTasks.forEach(task => {
    const project = task.project_name || '未割当プロジェクト';
    if (!projectMap.has(project)) projectMap.set(project, []);
    projectMap.get(project)!.push(task);
  });
  projectMap.forEach((tasks, project) => {
    groupedByProject.push({ project, tasks });
  });

  // 外部からassigneeFilterが渡された場合は同期
  useEffect(() => {
    if (assigneeFilter !== undefined) {
      setAssigneeFilterState(assigneeFilter);
    }
  }, [assigneeFilter]);

  // ウィンドウリサイズ時にガント部分の横幅を取得
  useEffect(() => {
    const updateWidth = () => {
      if (ganttAreaRef.current) {
        setGanttWidth(ganttAreaRef.current.offsetWidth);
      }
    };
    updateWidth();
    window.addEventListener('resize', updateWidth);
    return () => window.removeEventListener('resize', updateWidth);
  }, []);

  // 初期表示時に「本日-7日」が一番左に来るように自動スクロール
  useEffect(() => {
    if (!minDate || !ganttScrollRef.current) return;
    const today = new Date();
    const targetDate = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7);
    const min = new Date(minDate);
    const diff = Math.max(0, Math.floor((targetDate.getTime() - min.getTime()) / (1000 * 60 * 60 * 24)));
    ganttScrollRef.current.scrollLeft = diff * 24;
  }, [minDate, maxDate]);

  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!minDate || !maxDate) return <div>表示するタスクがありません<br />userId: {String(userId)}<br />filteredTasks: {JSON.stringify(filteredTasks)}</div>;

  // 日数スケール
  const totalDays = dateDiffInDays(minDate, maxDate) + 1;
  const dayWidth = 24; // 1日あたりのpx幅（固定）
  const todayStr = new Date().toISOString().slice(0, 10);

  // 年月ラベル生成
  const monthLabels: { label: string; colSpan: number }[] = [];
  let prevMonth = '';
  let colSpan = 0;
  for (let i = 0; i < totalDays; i++) {
    const date = new Date(new Date(minDate).getTime() + i * 86400000);
    const ym = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    if (ym !== prevMonth) {
      if (colSpan > 0) monthLabels.push({ label: prevMonth, colSpan });
      prevMonth = ym;
      colSpan = 1;
    } else {
      colSpan++;
    }
  }
  if (colSpan > 0) monthLabels.push({ label: prevMonth, colSpan });

  return (
    <>
      {/* ヘッダー部分は外部から受け取る形に変更予定 */}
      {/* ステータス凡例（ガントチャート外に移動） */}
      <div style={{ display: 'flex', gap: 18, alignItems: 'center', padding: '10px 24px 4px 24px', fontSize: 14 }}>
        <span style={{ fontWeight: 500 }}>ステータス凡例:</span>
        {Object.entries(statusLabels).map(([key, label]) => (
          <span key={key} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <span style={{ width: 18, height: 10, background: statusColors[key], borderRadius: 4, display: 'inline-block', marginRight: 2, border: '1px solid #ccc' }} />
            {label}
          </span>
        ))}
      </div>
      <div style={{ display: 'flex', width: '100%' }}>
        {/* 左カラム：stickyでタスク名＋ステータスを常に固定 */}
        <div style={{ width: 340, minWidth: 340, maxWidth: 340, position: 'sticky', left: 0, zIndex: 4, background: '#fff', boxShadow: '2px 0 8px #90caf933' }}>
          {/* 年月ラベルの空白 */}
          <div style={{ height: 74, borderBottom: '1px solid #eee' }}></div>
          {/* プロジェクトごとにヘッダー＋タスク行を表示 */}
          {groupedByProject.map((proj, projIdx) => (
            <React.Fragment key={proj.project}>
              {/* プロジェクト名ヘッダー行 */}
              <div style={{
                height: 38,
                display: 'flex',
                alignItems: 'center',
                background: '#e3f2fd',
                borderBottom: '1.5px solid #90caf9',
                fontWeight: 800,
                fontSize: 16,
                color: '#1976d2',
                letterSpacing: 1,
                paddingLeft: 12,
              }}>{proj.project}</div>
              {/* タスク行 */}
              {proj.tasks
                .filter(t => t.start_date && t.end_date)
                .map((task, idx) => (
                  <div
                    key={task.id}
                    style={{
                      height: 36,
                      display: 'flex',
                      alignItems: 'center',
                      borderBottom: '1px solid #eee',
                      background: idx % 2 === 0 ? '#fff' : '#f6fafd',
                      fontWeight: 400,
                      fontSize: 15,
                      gap: 10,
                      boxSizing: 'border-box',
                      lineHeight: '36px',
                    }}
                  >
                    <span style={{ fontWeight: 600, color: '#333', minWidth: 120, paddingLeft: 32 }}>{task.title}</span>
                    <span style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: 4,
                      fontWeight: 500,
                      fontSize: 13,
                      color: statusColors[task.status] || '#1976d2',
                      background: '#f0f4c3',
                      borderRadius: 8,
                      padding: '2px 10px',
                      marginLeft: 8,
                      minWidth: 70,
                      justifyContent: 'center',
                      lineHeight: '18px',
                    }}>
                      <span style={{ width: 12, height: 12, borderRadius: '50%', background: statusColors[task.status] || '#1976d2', display: 'inline-block' }} />
                      {statusLabels[task.status] || task.status}
                    </span>
                  </div>
                ))}
            </React.Fragment>
          ))}
        </div>
        {/* 右カラム：ガント部分（年月・日付・バー） */}
        <div ref={ganttScrollRef} style={{ flex: 1, overflowX: 'auto', background: '#f8fafc' }}>
          {/* 年月ラベル行 */}
          <div style={{ display: 'flex', minWidth: totalDays * dayWidth }}>
            {monthLabels.map((m, idx) => (
              <div key={idx} style={{ width: m.colSpan * dayWidth, textAlign: 'center', fontWeight: 'bold', fontSize: 13, borderRight: '1px solid #ccc', background: '#f5f7fa', height: 38, lineHeight: '38px', borderBottom: '1px solid #ccc' }}>{m.label}</div>
            ))}
          </div>
          {/* 日付ラベル行 */}
          <div style={{ display: 'flex', minWidth: totalDays * dayWidth }}>
            {[...Array(totalDays)].map((_, i) => {
              const date = new Date(new Date(minDate).getTime() + i * 86400000);
              const dateStr = date.toISOString().slice(0, 10);
              const isToday = dateStr === todayStr;
              const isPast = date < new Date(todayStr);
              return (
                <div
                  key={i}
                  style={{
                    width: dayWidth,
                    textAlign: 'center',
                    fontSize: 12,
                    color: isToday ? '#d32f2f' : '#888',
                    borderRight: '1px solid #ccc',
                    fontWeight: isToday ? 'bold' : undefined,
                    background: isToday ? '#ffe0e0' : isPast ? '#f0f0f0' : '#fafbfc',
                    borderBottom: isToday ? '2px solid #d32f2f' : '1px solid #ccc',
                    borderTop: isToday ? '2px solid #d32f2f' : undefined,
                    height: 36,
                    lineHeight: '36px',
                  }}
                >
                  {date.getDate()}
                </div>
              );
            })}
          </div>
          {/* プロジェクトごとにヘッダー＋タスク行を表示 */}
          {groupedByProject.map((proj, projIdx) => (
            <React.Fragment key={proj.project}>
              {/* プロジェクト名ヘッダー行の空白 */}
              <div style={{ height: 38 }}></div>
              {/* タスク行 */}
              {proj.tasks
                .filter(t => t.start_date && t.end_date)
                .map((task, idx) => {
                  const startOffset = dateDiffInDays(minDate, task.start_date!);
                  const barLength = dateDiffInDays(task.start_date!, task.end_date!) + 1;
                  return (
                    <div key={task.id} style={{ display: 'flex', minWidth: totalDays * dayWidth, height: 36 }}>
                      {[...Array(totalDays)].map((_, i) => (
                        <div key={i} style={{ width: dayWidth, height: 36, position: 'relative', background: (new Date(new Date(minDate).getTime() + i * 86400000) < new Date(todayStr)) ? '#f0f0f0' : '#fff', borderRight: '1px solid #ccc', borderBottom: '1px solid #ccc', boxSizing: 'border-box', lineHeight: '36px' }}>
                          {/* ガントバーを該当セルにまたがって絶対配置 */}
                          {i === startOffset && (
                            <div style={{
                              position: 'absolute',
                              left: 0,
                              width: barLength * dayWidth,
                              height: 12,
                              top: 12,
                              background: statusColors[task.status] || '#1976d2',
                              borderRadius: 4,
                              opacity: 0.9,
                              zIndex: 2,
                              display: 'flex',
                              alignItems: 'center',
                              boxShadow: '0 1px 4px #1976d222',
                            }}>
                              <span style={{ marginLeft: 8, fontSize: 12, color: '#fff', fontWeight: 600 }}>{statusLabels[task.status] || task.status}</span>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  );
                })}
            </React.Fragment>
          ))}
        </div>
      </div>
    </>
  );
};

export default GanttChart; 