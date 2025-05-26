const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export async function login(username: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/api/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!response.ok) {
    throw new Error('ログインに失敗しました');
  }
  return response.json(); // { access, refresh }
} 