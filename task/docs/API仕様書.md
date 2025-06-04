# API仕様書（最新版/PostgreSQL・Docker Compose対応）

## ユーザー関連

### ユーザー登録
- POST `/api/users/register/`
- body: { username, email, password }
- response: { id, username, email }

### ログイン（JWT）
- POST `/api/token/`
- body: { username, password }
- response: { refresh, access }

### 自分のユーザー情報取得
- GET `/api/users/me/`
- header: Authorization: Bearer <token>
- response: { id, username, email, profile_image, bio, department, notify_email }

### プロフィール更新
- PUT `/api/users/me/`
- body: { profile_image, bio, department, notify_email }
- response: ...

### パスワード変更
- POST `/api/users/me/change_password/`
- body: { current_password, new_password }
- response: { detail }

### 通知一覧
- GET `/api/notifications/`
- response: [ { id, message, is_read, created_at, link } ]

### 活動履歴一覧
- GET `/api/users/me/activity/`
- response: [ { id, action, created_at, related_task_id } ]

## タスク関連

### タスク一覧
- GET `/api/tasks/`
- response: [ { id, title, description, status, assignee, creator, start_date, end_date, ... } ]

### タスク作成
- POST `/api/tasks/`
- body: { title, description, status, assignee, start_date, end_date, ... }
- response: { ... }

### タスク編集
- PUT `/api/tasks/{id}/`
- body: { ... }

### タスク削除
- DELETE `/api/tasks/{id}/`

### プロジェクト一覧
- GET `/api/projects/`

### ユーザー一覧
- GET `/api/users/`

---

## インフラ・運用
- DBはPostgreSQL（Docker Composeで一貫運用）
- 既存データ移行（SQLite→PostgreSQL）手順をサポート

...（必要に応じて追記）... 