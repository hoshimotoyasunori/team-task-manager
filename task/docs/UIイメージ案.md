# UIイメージ案（最新版/PostgreSQL・Docker Compose対応）

## 1. ログイン画面
- ユーザー名／メールアドレス、パスワード入力
- 新規登録・パスワードリセットへのリンク

## 2. ダッシュボード（メイン画面）
- サイドバー：ホーム、ダッシュボード、タスク作成
- メインエリア：タスク一覧（カンバン・ガントチャート・リスト切替）
- カンバン：各ステータスごとにカラム分け、カード型でドラッグ＆ドロップ
- 担当者バッジ・フィルター、編集・削除・詳細モーダル
- 上部バー：ユーザー名、ログアウト、プロフィール編集

## 3. タスク詳細・編集画面
- タスク名、説明、担当者、期限、優先度、進捗状況など編集
- コメント欄（今後追加予定）

## 4. マイページ画面
- 上部にプロフィール情報（画像・名前・メール・自己紹介など）
- 編集・パスワード変更ボタン
- 下部に自分のタスク一覧、通知、アカウント設定、活動履歴

---

## インフラ・運用
- DBはPostgreSQL（Docker Composeで一貫運用）
- 既存データ移行（SQLite→PostgreSQL）手順をサポート

---

### 操作イメージ
- タスクのドラッグ＆ドロップで進捗や担当者を変更
- クリックで詳細表示、ダブルクリックで編集
- フィルタや検索でタスクを素早く絞り込み

---

ご要望に応じて、さらに詳細な画面設計やデザイン案も作成可能です。 