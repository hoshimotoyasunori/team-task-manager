# CI/CD運用ドキュメント

## 1. CI/CDの流れ
- GitHub Actions（.github/workflows/ci.yml）でmainブランチへのpush/pull request時に自動実行
- バックエンド: 依存インストール→lint→テスト→マイグレーション
- フロントエンド: 依存インストール→lint→ビルド→ユニットテスト→E2Eテスト
- MySQLはCIサービスとして自動起動

## 2. E2Eテストの実行方法
- Playwrightを利用
- ローカルでの実行例:
  ```sh
  cd app/frontend
  npm install
  npx playwright install
  npx playwright test
  ```
- テストは`app/frontend/e2e/`配下に配置

## 3. 障害時の対応
- CIで失敗した場合、GitHub Actionsのログを確認
- バックエンド: requirements.txtやマイグレーション、テストコードを確認
- フロントエンド: npm依存、ビルドエラー、E2Eテスト失敗箇所を確認
- MySQL起動失敗時はポート競合や設定を見直す

## 4. よくある質問
- Q: E2Eテストだけ再実行したい
  - A: `npx playwright test`で個別実行可能
- Q: CIのMySQLに接続したい
  - A: `localhost:3306`で接続、ユーザーroot/パスワードroot 