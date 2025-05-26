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

## 運用・デプロイ・ロールバック
- 本番デプロイは main ブランチへの push で自動実行（Vercel/Render 連携）
- デプロイ状況・履歴は各サービスの管理画面で確認
- DBマイグレーションは `python manage.py migrate` で実行。リセット時はバックアップ・ロールバック手順を遵守
- 依存パッケージは `requirements.txt`（Python）・`package.json`（frontend）でバージョン固定
- ロールバック時はGitの履歴・DBバックアップを活用

## APIドキュメント
- drf-spectacular導入済み。Swagger UI/RedocでAPI自動ドキュメント生成
- アクセス例: `/api/schema/swagger-ui/` `/api/schema/redoc/`
- 仕様詳細は `docs/API仕様書.md` 参照

## 依存パッケージ・Node.jsバージョン管理
- Node.jsは16.xまたは18.xを推奨（nvmで切替可）
- ルート直下のnpmファイルは削除済み、`task/frontend`配下のみで依存管理
- 依存競合・ビルドエラー時はキャッシュクリア・バージョン統一を徹底

## 自動テスト・管理者運用
- Django自動テスト: `python manage.py test`
- 管理者画面: `/admin/` でアクセス、初回は `createsuperuser` で作成
- 管理者操作ログ・データ管理も強化済み

## ドキュメント・運用ノウハウの一元管理
- 重要な運用・開発・品質・運用ノウハウはREADMEに必ず反映
- 新機能や運用改善のたびにREADMEを随時追記・整理 