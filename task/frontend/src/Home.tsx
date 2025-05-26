import React, { useState, useEffect } from 'react';
import TaskList from './TaskList';
import GanttChart from './GanttChart';
import KanbanBoard from './KanbanBoard';
import { fetchProjects } from './api/projects';
import { getUsers } from './api/user';
import BoardHeader from './BoardHeader';
import TaskCreateModal from './TaskCreateModal';

const TASK_VIEWS = ['リスト', 'ガント', 'カンバン'] as const;
type TaskView = typeof TASK_VIEWS[number];

interface HomeProps {
  username?: string;
  userId?: number;
}

const Home: React.FC<HomeProps> = ({ username, userId }) => {
  const [taskView, setTaskView] = useState<TaskView>('リスト');
  const [selectedProject, setSelectedProject] = useState<number | ''>('');
  const [projects, setProjects] = useState<{ id: number; name: string }[]>([]);
  const [users, setUsers] = useState<{ id: number; username: string }[]>([]);
  const [createOpen, setCreateOpen] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      fetchProjects(token).then(setProjects).catch(() => setProjects([]));
      getUsers(token).then(setUsers).catch(() => setUsers([]));
    }
  }, []);

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
          ? '全プロジェクトの自分のタスクを表示しています'
          : `${projects.find(p => p.id === selectedProject)?.name} の自分のタスクを表示しています`}
        showAssigneeFilter={false}
      />
      <TaskCreateModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onCreate={handleCreateTask}
        users={users}
        projects={projects}
      />
      <div className="board-main-box">
      {taskView === 'リスト' && <TaskList onlyMine={true} hideAssigneeFilter={true} username={username} userId={userId} filterProject={selectedProject || undefined} hideProjectFilter={true} />}
        {taskView === 'ガント' && <GanttChart onlyMine={true} hideAssigneeFilter={true} username={username} userId={userId} filterProject={selectedProject || undefined} hideProjectFilter={true} groupBy="none" />}
        {taskView === 'カンバン' && userId !== undefined && (
          <KanbanBoard onlyMine={true} hideAssigneeFilter={true} username={username} userId={userId} filterProject={selectedProject || undefined} hideProjectFilter={true} />
        )}
        {taskView === 'カンバン' && userId === undefined && (
          <div>ユーザー情報取得中...</div>
        )}
      </div>
    </>
  );
};

export default Home; 