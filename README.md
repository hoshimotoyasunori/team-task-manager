# チームタスク管理・共有Webアプリ

## 概要
チームでのタスク管理・共有を目的とした業務用Webアプリです。Django REST Framework（バックエンド）、React+TypeScript（フロントエンド）、MySQL/SQLite、GitHub連携を前提としています。

## 主な機能
- ユーザー認証（JWT）
- タスクの作成・編集・削除・詳細表示
- カンバン・ガントチャート・リスト表示
- プロジェクト・担当者フィルター
- プロフィール編集・パスワード変更
- サイドバー開閉・モダンなUI/UX
- ダミーデータ生成コマンド

## セットアップ手順
### 1. バックエンド（Django）
```sh
cd task/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # 管理者作成
python manage.py runserver
```

### 2. フロントエンド（React）
```sh
cd task/frontend
npm install
npm run dev
```

### 3. DB
- デフォルトはSQLite。MySQL利用時は`settings.py`を編集し、DBを用意してください。

### 4. その他
- `.env`ファイルでAPIエンドポイントやDB接続情報を管理
- `.gitignore`で不要ファイル除外

## 開発・運用のポイント
- GitHubでブランチ運用・Pull Request推奨
- コード・UI/UXのリファインは随時AIアシスト可
- バグ・要望はIssueで管理

## 今後の拡張予定
- プロジェクト・チーム管理の拡張（チームタブ/スペース）
- 権限管理・ユーザー招待・コメント機能
- ダークモードやカラーテーマ切り替え
- 必要に応じて管理画面・分析ダッシュボード等

## ライセンス・問い合わせ
- ライセンス: MIT（仮）
- 問い合わせ: your-email@example.com（仮） 