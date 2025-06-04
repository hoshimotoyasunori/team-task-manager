# Django + PostgreSQL + Docker Compose 運用・セットアップガイド

## 1. 構成概要
- バックエンド: Django REST Framework
- DB: PostgreSQL（Docker Compose管理）
- 開発・本番ともにDocker Composeで一貫運用

## 2. セットアップ手順

### 1. 依存パッケージインストール
```
pip install -r requirements.txt
```

### 2. .envファイル作成（例）
```
DJANGO_DB_NAME=app_db
DJANGO_DB_USER=app_user
DJANGO_DB_PASSWORD=app_pass
DJANGO_DB_HOST=db
DJANGO_DB_PORT=5432
DEBUG=1
```

### 3. Docker ComposeでDB・Django起動
```
docker-compose up --build
```
- 初回は自動でマイグレーション＆サーバ起動
- DBは`localhost:5432`でPostgreSQLが立ち上がります

### 4. 管理画面・API確認
- http://localhost:8000/admin/
- http://localhost:8000/api/

## 3. 既存データ移行（SQLite→PostgreSQL）
- `docs/SQLite_to_PostgreSQL移行手順.md` を参照

## 4. 運用・バックアップ・リストア
- DBデータは`postgres_data`ボリュームに永続化
- バックアップ例：
```
docker exec -t <db_container> pg_dump -U app_user app_db > backup.sql
```
- リストア例：
```
docker exec -i <db_container> psql -U app_user app_db < backup.sql
```

## 5. トラブル対応
- DB接続エラー：環境変数・docker-compose.ymlの設定を再確認
- マイグレーション失敗：`docker-compose run web python manage.py migrate` で手動実行
- DB初期化：`docker-compose down -v` でボリュームごと削除

---

ご不明点は`docs/SQLite_to_PostgreSQL移行手順.md`やDjango/pgloader公式ドキュメントも参照してください。 