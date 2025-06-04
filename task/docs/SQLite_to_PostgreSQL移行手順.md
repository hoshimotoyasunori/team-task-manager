# SQLite→PostgreSQL 移行手順（Django/Docker Compose対応）

## 概要
- 既存のSQLiteデータベースをPostgreSQLへ安全に移行する手順です。
- Docker Compose＋Django＋PostgreSQL前提。

## 1. 事前準備
- 既存の`db.sqlite3`をバックアップ
- 依存パッケージ確認：`pip install psycopg2-binary pgloader`

## 2. PostgreSQLコンテナ起動
```
docker-compose up -d db
```

## 3. PostgreSQLに空DBを作成（不要な場合はスキップ）
- docker-compose.ymlの環境変数で自動作成されます

## 4. DjangoマイグレーションでPostgreSQLにテーブル作成
```
docker-compose run web python manage.py migrate
```

## 5. SQLite→PostgreSQLデータ移行
- `pgloader`を使う方法（推奨）

例：
```
pgloader db.sqlite3 postgresql://app_user:app_pass@localhost:5432/app_db
```
- Dockerコンテナ内で実行する場合は、`db`サービスのPostgreSQLに合わせて接続情報を調整

## 6. 動作確認
- DjangoでPostgreSQLに切り替わっているか確認
- 管理画面やAPIでデータが正しく移行されているか確認

## 7. 不要なSQLiteファイル・設定の削除
- `db.sqlite3`や`sqlite3`関連の設定を削除

## 8. 注意点
- マイグレーション後は必ずバックアップを取得
- 文字コードや日付型の差異に注意
- 必要に応じてDjangoの`inspectdb`でスキーマ確認

---

ご不明点・トラブル時は`pgloader`のログやDjangoのエラーメッセージを参照してください。 