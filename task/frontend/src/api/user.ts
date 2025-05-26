const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export async function fetchUserMe(token: string) {
  const response = await fetch(`${API_BASE_URL}/api/me/`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error('ユーザー情報取得に失敗しました');
  }
  return response.json();
}

export async function getUsers(token: string) {
  const response = await fetch(`${API_BASE_URL}/api/users/`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error('ユーザー一覧取得に失敗しました');
  }
  return response.json();
}

export async function fetchUserProfile(token: string) {
  const response = await fetch(`${API_BASE_URL}/api/users/me/`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error('プロフィール情報取得に失敗しました');
  }
  return response.json();
}

export async function updateUserProfile(token: string, data: any) {
  const response = await fetch(`${API_BASE_URL}/api/users/me/`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
    body: data instanceof FormData ? data : JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error('プロフィール更新に失敗しました');
  }
  return response.json();
}

export async function changePassword(token: string, current_password: string, new_password: string) {
  const response = await fetch(`${API_BASE_URL}/api/users/me/change_password/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ current_password, new_password }),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'パスワード変更に失敗しました');
  }
  return response.json();
}

export async function fetchNotifications(token: string) {
  const response = await fetch(`${API_BASE_URL}/api/notifications/`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error('通知一覧取得に失敗しました');
  }
  return response.json();
}

export async function fetchActivityLogs(token: string) {
  const response = await fetch(`${API_BASE_URL}/api/users/me/activity/`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error('活動履歴取得に失敗しました');
  }
  return response.json();
} 