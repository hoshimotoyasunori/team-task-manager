export async function login(username: string, password: string) {
  const response = await fetch('http://localhost:8000/api/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!response.ok) {
    throw new Error('ログインに失敗しました');
  }
  return response.json(); // { access, refresh }
} 