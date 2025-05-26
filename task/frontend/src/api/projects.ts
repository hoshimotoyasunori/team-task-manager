const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export async function fetchProjects(token: string) {
  const res = await fetch(`${API_BASE_URL}/api/projects/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    throw new Error('プロジェクト取得に失敗しました');
  }
  return res.json();
} 