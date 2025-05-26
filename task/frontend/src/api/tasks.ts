const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export async function fetchTasks(token: string, projectId?: number | '') {
  let url = `${API_BASE_URL}/api/tasks/`;
  if (projectId) {
    url += `?project=${projectId}`;
  }
  const response = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error('タスク取得に失敗しました');
  }
  return response.json();
}

export async function createTask(token: string, data: { title: string; description?: string; assignee?: number; project?: number }) {
  const response = await fetch(`${API_BASE_URL}/api/tasks/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || JSON.stringify(errorData) || 'タスク作成に失敗しました');
  }
  return response.json();
}

export async function updateTask(token: string, id: number, data: { title: string; description?: string; status?: string; assignee?: number; start_date?: string; end_date?: string; project?: number }) {
  const response = await fetch(`${API_BASE_URL}/api/tasks/${id}/`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error('タスク編集に失敗しました');
  }
  return response.json();
}

export async function deleteTask(token: string, id: number) {
  const response = await fetch(`${API_BASE_URL}/api/tasks/${id}/`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error('タスク削除に失敗しました');
  }
  return true;
} 