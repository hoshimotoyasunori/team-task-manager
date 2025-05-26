# 開発・テスト・品質管理ガイド

## 1. テスト実行方法

Django/DRFのAPIテストはpytestで実行します。

```sh
cd app/backend
pytest --ds=es_app.settings api/tests.py
```

## 2. カバレッジ計測

coverageでテストカバレッジを計測できます。

```sh
cd app/backend
coverage run --source=api -m pytest --ds=es_app.settings api/tests.py
coverage report -m
```

## 3. pre-commitフック

コミット前に自動でコード整形・静的解析（black, isort, flake8）を実行できます。

初回のみ:
```sh
pip install pre-commit
pre-commit install
```

手動実行:
```sh
pre-commit run --all-files
```

## 4. 注意事項
- テスト・カバレッジは必ず100%を目指してください（現状97%以上）
- コード整形・静的解析エラーはコミット前に必ず修正してください
- テスト・カバレッジ・pre-commitの手順はこのREADMEを参照

--- 