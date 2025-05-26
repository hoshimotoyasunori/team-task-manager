const API_URL = 'http://localhost:8000/api/projects/';

export async function fetchProjects(token: string) {
  const res = await fetch(API_URL, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    throw new Error('プロジェクト取得に失敗しました');
  }
  return res.json();
} 