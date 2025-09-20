# zenn-docs

ブログ記事プラットフォーム Zenn と連携するためのリポジトリです。

## 動かし方

- インストール

  ```bash
  npm i
  ```

- 👇 新しい記事を作成する

  ```bash
  npx zenn new:article --slug 記事のスラッグ --title タイトル --type tech --emoji 🛠
  ```

  npx zenn new:article --slug web3_ai_vibecoding --title Kiro×CodeXで最高のSpec駆動開発を！数時間でWeb3ネイティブなアプリを開発してハッカソンで入賞した話 --type tech --emoji 🛠

- 👇 新しい本を作成する

  ```bash
  npx zenn new:book
  ```

- 👇 投稿をプレビューする

  ```bash
  npx zenn preview
  ```
