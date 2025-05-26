import React from 'react';

interface BoardHeaderProps {
  taskView: string;
  setTaskView: (v: string) => void;
  taskViews: string[];
  selectedProject: number | '';
  setSelectedProject: (v: number | '') => void;
  projects: { id: number; name: string }[];
  onOpenCreate: () => void;
  statusText?: string;
  showAssigneeFilter?: boolean;
  assigneeList?: string[];
  assigneeFilter?: string;
  setAssigneeFilter?: (v: string) => void;
}

const BoardHeader: React.FC<BoardHeaderProps> = ({
  taskView, setTaskView, taskViews,
  selectedProject, setSelectedProject, projects,
  onOpenCreate, statusText,
  showAssigneeFilter = false, assigneeList = [], assigneeFilter = 'all', setAssigneeFilter
}) => (
  <div style={{
    display: 'flex',
    alignItems: 'center',
    gap: 32,
    background: '#fff',
    padding: '16px 32px',
    borderRadius: 12,
    boxShadow: '0 2px 8px #0001',
    marginBottom: 24,
    border: '1.5px solid #e3eaf5',
    flexWrap: 'wrap',
  }}>
    {/* ボード切り替え */}
    <div style={{ display: 'flex', gap: 12 }}>
      {taskViews.map(v => (
        <button key={v} onClick={() => setTaskView(v)} style={{ fontWeight: taskView === v ? 700 : 400, fontSize: 15, padding: '6px 18px', borderRadius: 6, border: taskView === v ? '2px solid #1976d2' : '1px solid #bbb', background: taskView === v ? '#e3f2fd' : '#f5f7fa', color: taskView === v ? '#1976d2' : '#333', cursor: 'pointer' }}>{v}</button>
      ))}
    </div>
    {/* プロジェクト選択 */}
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <span style={{ fontWeight: 600, color: '#1976d2', fontSize: 15 }}>プロジェクト選択:</span>
      <select value={selectedProject} onChange={e => setSelectedProject(Number(e.target.value) || '')} style={{ fontSize: 15, padding: '6px 16px', borderRadius: 6, border: '1.5px solid #90caf9', background: '#fff', minWidth: 120 }}>
        <option value="">全プロジェクト</option>
        {projects.map(p => (
          <option key={p.id} value={p.id}>{p.name}</option>
        ))}
      </select>
    </div>
    {/* 担当者フィルター */}
    {showAssigneeFilter && setAssigneeFilter && (
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <span style={{ fontWeight: 600, color: '#1976d2', fontSize: 15 }}>担当者フィルター:</span>
        <select value={assigneeFilter} onChange={e => setAssigneeFilter(e.target.value)} style={{ fontSize: 15, padding: '6px 16px', borderRadius: 6, border: '1.5px solid #90caf9', background: '#fff', minWidth: 100 }}>
          <option value="all">全員</option>
          {assigneeList.map(name => (
            <option key={name} value={name}>{name}</option>
          ))}
        </select>
      </div>
    )}
    {/* 状態説明 */}
    {/* {statusText && <div style={{ color: '#888', fontSize: 14 }}>{statusText}</div>} */}
  </div>
);

export default BoardHeader; 