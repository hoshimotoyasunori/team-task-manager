# 情報共有app（パーソナルタスク管理Webアプリ）

## 概要
チームや個人のタスクを直感的に管理・共有できるWebアプリです。  
**バックエンド：Django REST Framework**  
**フロントエンド：React（TypeScript）**

---


## 1. ディレクトリ構成

```
backend/    # Django REST Framework（APIサーバ）
frontend/   # React（TypeScript）
docs/       # ドキュメント類
docker/     # Docker関連ファイル（任意）
```

---

## 2. 初回セットアップ

### バックエンド

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # 管理者ユーザー作成
```

### フロントエンド

```bash
cd ../frontend
npm install
```

### Docker利用時（任意）

```bash
cd ../docker
docker-compose up --build
```

---

## 3. 開発・起動方法

### バックエンド

```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### フロントエンド

```bash
cd frontend
npm start
```
- ブラウザで http://localhost:3000 にアクセス

---

## 4. API利用例

### タスク一覧取得

```bash
curl http://localhost:8000/api/tasks/
```

### タスク新規作成

```bash
curl -X POST -H "Content-Type: application/json" -d '{"title": "テストタスク", "creator": 1}' http://localhost:8000/api/tasks/
```

### ユーザー登録

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "newuser", "email": "newuser@example.com", "password": "password123"}' http://localhost:8000/api/register/
```

---

## 5. 認証（JWT）

- トークン取得・リフレッシュ・認証付きAPIリクエスト例を記載
- JWTの有効期限やリフレッシュ仕様は`backend/config/settings.py`を参照

---

## 6. ダミーデータ作成

開発・動作確認用に、ダミーユーザーとダミータスクを自動作成できます。

```bash
cd backend
source venv/bin/activate
python manage.py create_dummy_data
```
- 既存データへの影響：既存ユーザー・タスクは上書きされません

---

## 7. 主な機能・UI/UX

- カンバン方式（ToDo/進行中/レビュー待ち/完了）でタスクをドラッグ＆ドロップ移動
- ガントチャート表示
- 担当者バッジ・フィルター
- タスク編集・削除・詳細モーダル
- マイページ（プロフィール編集、通知、活動履歴、アカウント設定）

---

## 8. マイページ機能

- プロフィール情報の表示・編集
- パスワード変更
- 自分のタスク一覧（担当・作成タスク、ステータス別タブ・フィルター）
- 通知・お知らせ一覧
- アカウント設定（メール通知ON/OFF、ダークモード切替、退会機能）
- 活動履歴

---

## 9. 管理者ページ（Django Admin）

- `/admin/` で管理者用GUI
- ユーザー・タスク・通知・活動履歴などの管理
- スーパーユーザーは `python manage.py createsuperuser` で作成

---

## 10. 自動テスト

- 主要APIの自動テストあり
- 実行方法：

```bash
cd backend
source venv/bin/activate
python manage.py test
```

---

## 11. 運用・開発フロー

- ブランチ運用ルール（main, develop, feature/xxx, bugfix/xxx）
- マイグレーション・DB管理（バックアップ必須、不要ファイル削除、リセット時の記録）
- デプロイ・ロールバック手順はdocs/参照
- 依存パッケージはバージョン固定、pip-auditで脆弱性チェック

---

## 12. ドキュメント・設計資料

- docs/配下に「機能一覧」「UIイメージ」「要件定義書」などを随時更新
- 画面遷移図やAPI仕様書もdocs/に格納

---

## 13. 改善・今後の展望（推奨）

- APIエンドポイント一覧やレスポンス例をまとめたドキュメント追加
- Docker利用時の.envサンプルやdocker-composeの詳細手順追加
- テストカバレッジの目標値や現状のカバレッジをREADMEやdocsに明記
- i18n（多言語化）やアクセシビリティ対応の方針も検討

---

## 14. お問い合わせ・コントリビュート

- バグ報告・機能要望はIssueへ
- コントリビュート歓迎！ブランチ運用ルールを守ってPRを作成してください

---

詳細は `docs/` フォルダの各種ドキュメントを参照してください。

---

## サーバー起動・API動作確認メモ

### Djangoサーバーの起動方法
```
cd backend
source venv/bin/activate
python manage.py runserver
```

### API動作確認（例：curlコマンド）
- タスク一覧取得
```
curl http://localhost:8000/api/tasks/
```
- タスク新規作成（例）
```
curl -X POST -H "Content-Type: application/json" -d '{"title": "テストタスク", "creator": 1}' http://localhost:8000/api/tasks/
```

### ユーザー登録（サインアップ）
```
curl -X POST -H "Content-Type: application/json" -d '{"username": "newuser", "email": "newuser@example.com", "password": "password123"}' http://localhost:8000/api/register/
```

---

## 認証（JWT）について

### トークン取得
```
curl -X POST -H "Content-Type: application/json" -d '{"username": "<ユーザー名>", "password": "<パスワード>"}' http://localhost:8000/api/token/
```
- レスポンス例：
```
{"refresh": "...", "access": "..."}
```

### トークンリフレッシュ
```
curl -X POST -H "Content-Type: application/json" -d '{"refresh": "<リフレッシュトークン>"}' http://localhost:8000/api/token/refresh/
```

### 認証付きAPIリクエスト例
- 取得したアクセストークンを使ってAPIにアクセス
```
curl -H "Authorization: Bearer <アクセストークン>" http://localhost:8000/api/tasks/
```

---

## フロントエンド（React）の起動方法

```
cd task/frontend
npm start
```

- ブラウザで http://localhost:3000 にアクセス
- ログイン画面が表示されます

---

## ダミーデータ作成コマンド

開発・動作確認用に、ダミーユーザーとダミータスクを自動作成できます。

```
cd backend
source venv/bin/activate
python manage.py create_dummy_data
```

- ユーザー: user1〜user5（パスワード: testpass123）
- タスク: ダミータスク1〜10（担当者・作成者はランダム）

---

## 最新の主な機能・UI/UX

- カンバン方式（ToDo/進行中/レビュー待ち/完了）でタスクをドラッグ＆ドロップ移動
- react-beautiful-dndによる直感的なドラッグ操作（下に避けるUXも実現済み）
- ガントチャート表示（担当者ごとグルーピング、sticky列、日付ラベル、今日の強調）
- 担当者バッジ（色分け・イニシャル表示）
- 担当者フィルター（プルダウンで絞り込み）
- タスク編集・削除ボタン、詳細モーダル、編集モーダル（API連携・バリデーション付き）
- ダミーデータ生成コマンド

### カンバンの「下に避ける」UXについて
- react-beautiful-dndの仕様上、タスクカードとplaceholderを同じラッパーdiv（margin/paddingはラッパーで管理）で囲むことで、ドラッグ時に下に避ける自然な挙動を実現しています。
- 詳細は`frontend/src/KanbanBoard.tsx`の該当箇所を参照。

---

## 変更履歴・ドキュメント反映
- docs/配下の「機能一覧」「UIイメージ案」「要件定義書」も現状に合わせて随時更新しています。

---

## マイページ機能

- プロフィール情報の表示・編集（ユーザー名、メールアドレス、プロフィール画像、自己紹介、所属チーム等）
- パスワード変更（現在のパスワード、新パスワード、バリデーション）
- 自分のタスク一覧（担当・作成タスク、ステータス別タブ・フィルター、詳細・編集・進捗変更）
- 通知・お知らせ一覧（タスク割り当て・完了・コメント等、既読/未読管理、該当タスク遷移）
- アカウント設定（メール通知ON/OFF、ダークモード切替、退会機能）
- 活動履歴（最近のタスク操作履歴）

### 画面イメージ
- サイドバーやヘッダーから「マイページ」へ遷移
- 上部にプロフィール情報＋編集ボタン
- 下部に「自分のタスク一覧」タブ（担当/作成/全て/フィルター）
- 右側や下部に「通知」「アカウント設定」などのタブ or セクション
- 編集・パスワード変更・画像アップロードはモーダル or 別画面

---

## 運用・開発フローの注意点

### ブランチ運用ルール
- `main`：本番用
- `develop`：開発用
- `feature/xxx`：新機能開発用
- `bugfix/xxx`：バグ修正用

### マイグレーション・DB管理
- 本番DBは必ずバックアップを取得してからmigrateを実施
- モデル大幅変更時は、不要なマイグレーションファイルを削除し直す
- DBリセット時は必ずデータバックアップ＆リストア手順を記録

### デプロイ・ロールバック手順
- デプロイ前にテスト・レビューを徹底
- 万一の不具合時は直前のリリースタグにロールバック
- ロールバック手順もdocs/に記載

### 依存パッケージ・セキュリティ
- `requirements.txt`はバージョン固定
- `pip list --outdated`で定期的にアップデート確認
- `pip-audit`で脆弱性チェック

---

## 管理者ページ（Django Admin）について

- `/admin/` にアクセスすると、管理者用のGUI画面でユーザー・担当者・タスク・通知・活動履歴などのデータを追加・編集・削除できます。
- スーパーユーザー（管理者）は `python manage.py createsuperuser` で作成できます。
- 管理画面では、担当者（ユーザー）の登録・編集、タスクや通知の管理、操作ログ（ActivityLogやDjango標準の操作履歴）の確認が可能です。
- 本番DBがリセットされた場合も、管理画面からデータを再登録できます。
- 管理者の操作履歴は標準＋拡張で記録・監査できます。

---

## 自動テストの実行方法（Djangoバックエンド）

- 主要なAPI（ユーザー登録・認証・タスク作成・編集・削除など）の自動テストが用意されています。
- 下記コマンドで全テストを実行できます。

```
cd backend
source venv/bin/activate
python manage.py test
```

- テストがすべてOKなら「本番公開前の品質チェック」も安心です。
- テスト追加・修正も `users/tests.py` や `tasks/tests.py` を編集するだけで簡単です。

---
