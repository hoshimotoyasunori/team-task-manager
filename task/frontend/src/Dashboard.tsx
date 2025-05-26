import React, { useState, useEffect } from 'react';
import TaskList from './TaskList';
import GanttChart from './GanttChart';
import KanbanBoard from './KanbanBoard';
import BoardHeader from './BoardHeader';
import TaskCreateModal from './TaskCreateModal';
import { fetchProjects } from './api/projects';
import { getUsers } from './api/user';

const TASK_VIEWS = ['リスト', 'ガント', 'カンバン'] as const;
type TaskView = typeof TASK_VIEWS[number];

const Dashboard: React.FC = () => {
  const [taskView, setTaskView] = useState<TaskView>('リスト');
  const [selectedProject, setSelectedProject] = useState<number | ''>('');
  const [projects, setProjects] = useState<{ id: number; name: string }[]>([]);
  const [users, setUsers] = useState<{ id: number; username: string }[]>([]);
  const [assigneeFilter, setAssigneeFilter] = useState<string>('all');
  const [createOpen, setCreateOpen] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      fetchProjects(token).then(setProjects).catch(() => setProjects([]));
      getUsers(token).then(setUsers).catch(() => setUsers([]));
    }
  }, []);

  // 担当者リスト（重複なし）
  const assigneeList = users.map(u => u.username);

  // タスク作成
  const handleCreateTask = async (data: any) => {
    const token = localStorage.getItem('accessToken');
    if (!token) return;
    // API呼び出しは各ボード側でリロードするためここでは閉じるだけ
    setCreateOpen(false);
  };

  return (
    <>
      <BoardHeader
        taskView={taskView}
        setTaskView={v => setTaskView(v as TaskView)}
        taskViews={TASK_VIEWS as unknown as string[]}
        selectedProject={selectedProject}
        setSelectedProject={setSelectedProject}
        projects={projects}
        onOpenCreate={() => setCreateOpen(true)}
        statusText={selectedProject === '' || selectedProject === undefined
          ? '全プロジェクトのタスクを表示しています'
          : `${projects.find(p => p.id === selectedProject)?.name} のタスクを表示しています`}
        showAssigneeFilter={true}
        assigneeList={assigneeList}
        assigneeFilter={assigneeFilter}
        setAssigneeFilter={setAssigneeFilter}
      />
      <TaskCreateModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onCreate={handleCreateTask}
        users={users}
        projects={projects}
      />
      <div className="board-main-box">
        {taskView === 'リスト' && (
          <TaskList
            hideProjectFilter={true}
            hideAssigneeFilter={true}
            filterProject={selectedProject || undefined}
            assigneeFilter={assigneeFilter}
            setAssigneeFilter={setAssigneeFilter}
          />
        )}
        {taskView === 'ガント' && (
          <GanttChart
            hideProjectFilter={true}
            hideAssigneeFilter={false}
            filterProject={selectedProject || undefined}
            assigneeFilter={assigneeFilter}
            setAssigneeFilter={setAssigneeFilter}
            groupBy="project"
          />
        )}
        {taskView === 'カンバン' && (
          <KanbanBoard
            hideProjectFilter={true}
            hideAssigneeFilter={false}
            filterProject={selectedProject || undefined}
            assigneeFilter={assigneeFilter}
            setAssigneeFilter={setAssigneeFilter}
          />
        )}
      </div>
    </>
  );
};

export default Dashboard; 