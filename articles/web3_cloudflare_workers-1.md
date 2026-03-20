---
title: "VibeKanbanを使ってCloudFlareWorkersにx402MCPサーバーを開発＆デプロイしてみた！"
emoji: "💵"
type: "tech" 
topics: ["blockchain","web3","cloudflare","mcp","ai"]
published: false
---

# はじめに

皆さん、こんにちは！

先日初めてちゃんと**Cloudflare Workers**について勉強してみたのでそのアウトプットの記事を書いてみました！

今回は実装で試してみたことやMCPサーバーを**Cloudflare Workers**にデプロイする方法などをシェアする記事になっています！

# CloudFlare Workerとは？

https://www.cloudflare.com/ja-jp/developer-platform/products/workers/

**Cloudflare Workers**は、**Cloudflare**社が展開しているサーバーレスコンピューティングプラットフォームです。

バンドルサイズなど一部制約がありますが、TypeScript/JavaScript製のアプリをフロントエンド感覚で簡単にデプロイすることができる点が魅力です！

その他、**KV**や**D1**など**Cloudflare**の主力サービスとも連携しやすい点が魅力と言えます！

# Honoとの相性の良さ

https://hono.dev/

Honoは、主にTypeScript/JavaScriptでWebアプリケーションやAPIを開発するための、軽量・高速・モダンなWebフレームワークです。

高速かつ軽量であるなど**Cloudflare Workersとは非常に相性が良い**です！

# Vibe Kanbanとは

https://vibekanban.com/

AIコーディングエージェント（Claude CodeやCodex）をカンバン方式（タスクの見える化）で管理し、自動化された開発フローを実現するツールです！

## cc-sdd + VibeKanban + GitWorkTreeによる開発のワークフロー

今回実装するにあたり以下のような開発ワークフローを実践してみました。

- 0. プロダクトのビジョン、コンセプトを策定する
- 1. cc-sddで要件定義と設計書、タスクリストを作成する
- 2. VibeKanbanにタスクを登録(GitHubにイシュー登録)
  ![](/images/web3_cloudflare_workers-1/0.png)
- 3. git worktreeで作業ディレクトリを準備
  ![](/images/web3_cloudflare_workers-1/1.png)
- 4. タスクの並列実行
  ![](/images/web3_cloudflare_workers-1/3.png)
- 5. 各成果物をセルフレビュー・PR作成
  ![](/images/web3_cloudflare_workers-1/5.png)

  コードレビューには**CodeRabbit**を使ってみました！

  ![](/images/web3_cloudflare_workers-1/6.png)

## cc-sddで生成したタスクをVibeKanban用のタスクに変換・登録する方法

cc-sddで生成したタスクをVibeKanban用のタスクに変換・登録するために以下のようなプロンプトを使ってみました！

```bash
@(cc-sddで生成したタスクリスト)を確認して、作業計画を Task 単位で vibe_kanban へ Task として登録してください。

タスクには以下の内容を記載します:

- 設計は @design.md を参照すること
- このタスクでの具体的な作業内容
- 依存する他のタスクや、並列作業が可能かどうか
- 並列実行できる場合は、タイトルに + をつけてください

タスクは降順に登録してください。
```

そのままGitHub イシュー化できてしまえるのが良い点ですね！

# x402とは？

https://www.x402.org/

x402は米国で著名な暗号資産交換所である**Coinbase**社が発表したステーブルコイン決済のため標準プロトコルです。

その名の通りHTTPステータスコード402 **Payment Required** を採用しており、HTTPプロトコルに準拠している点が非常に話題となりました。

**Cloudflare**社とはx402 foundationも設立している他、AI Agentとも相性が良いことから数あるブロックチェーンの技術スタックでも大きな注目を集めている技術になります。

https://blog.cloudflare.com/x402/

# 今回作ったアプリについて

## 概要

**Cloudflare Workers**にx402バックエンドサーバーとMCPサーバーをデプロイして、さらにGPT App内のチャットインターフェースから天気予報の情報を取得すると同時にステーブルコイン支払いが行われるサンプルアプリを作りました！

できること
- GPT App から get_weather ツールを呼び出して天気情報を取得
- x402 による支払い検証を通過したリクエストのみ /weather にアクセス
- Cloudflare Workers 上で x402server と mcpserver を分離デプロイ
- E2E テストで mcpserver -> x402FetchClient -> x402server の結合動作を検証

## サンプルコード

今回試したソースコードは以下のGitHubリポジトリに格納しています。

https://github.com/mashharuki/vibekanban-gitworktree-sample

### リポジトリ構成

| パス                    | 役割                                                                     | 主な技術                                                          |
| ----------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| `pkgs/x402server`       | 天気 API と x402 決済検証を提供するバックエンド                          | Hono / x402 / Cloudflare Workers / TypeScript                     |
| `pkgs/mcpserver`        | GPT App から呼び出される MCP サーバー。`x402server` を決済付きで呼び出す | Hono MCP / MCP SDK / x402 fetch / Cloudflare Workers / TypeScript |
| `pkgs/*/__tests__`      | 単体・結合テスト群                                                       | Vitest                                                            |
| ルート (`package.json`) | monorepo の共通スクリプト・ワークスペース管理                            | pnpm workspace                                                    |

## 実装した機能一覧

| 機能                             | 概要                                         | 提供パッケージ            | 補足                               |
| -------------------------------- | -------------------------------------------- | ------------------------- | ---------------------------------- |
| ヘルスチェック API               | サービス稼働確認 (`/`, `/health`)            | `x402server`, `mcpserver` | 監視・疎通確認に利用               |
| 天気情報取得 API                 | 都市名を受けて天気を返却 (`/weather`)        | `x402server`              | 都市未登録時は 404                 |
| x402 課金付きアクセス制御        | `/weather` を課金保護し未決済時は 402 を返却 | `x402server`              | 価格・ネットワークは環境変数で設定 |
| MCP ツール公開                   | `get_weather` ツールを外部クライアントへ公開 | `mcpserver`               | 入力検証・エラー整形を実施         |
| x402 決済付き fetch クライアント | 支払い情報付きで `x402server` を呼び出す     | `mcpserver`               | Service Binding / URL の両方に対応 |
| E2E 結合テスト                   | MCP から backend までの通し動作を検証        | `mcpserver` テスト        | 402/404/正常系を確認               |

# ポイントなる実装部分

簡単に重要な箇所をピックアップして実装部分を紹介していきます。

## x402サーバー編

## MCPサーバー編

## Cloudflare Workersへのデプロイ方法！

### x402バックエンドサーバー

- セットアップ

  環境変数用のファイルを作成

  ```bash
  cp pkgs/x402server/.dev.vars.example pkgs/x402server/.dev.vars
  ```

- デプロイ

  ```bash
  pnpm x402server run deploy
  ```

### MCPサーバー

- セットアップ

  環境変数用のファイルを作成

  ```bash
  cp pkgs/mcpserver/.dev.vars.example pkgs/mcpserver/.dev.vars
  ```

  `X402_SERVER_URL`には上記でCloudFlare Workersにデプロイしたx402バックエンドサーバーのAPIエンドポイントURLを指定する

  (Cloudflare Workersにデプロイする場合)x402クライアント用の秘密鍵とx402バックエンドサーバーのエンドポイントの登録

  ```bash
  pnpm mcpserver run secret CLIENT_PRIVATE_KEY --name mcpserver
  pnpm mcpserver run secret X402_SERVER_URL --name mcpserver
  ```

- デプロイ

  ```bash
  pnpm mcpserver run deploy
  ```

  `https://mcpserver.<固有値>.workers.dev/mcp`をGPT AppのURLに登録すればチャットからx402の支払いができる！

## ChatGPTのチャットインターフェース内から呼び出す方法

1. MCPサーバーのエンドポイントをGPT Appに登録する
2. +ボタンから追加したアプリを選んで追加した状態で天気予報を教えてもらう
3. 天気予報が返ってきてUSDCが支払いされていればOK!

    ![](/images/web3_cloudflare_workers-1/7.png)

    ブロックエクスプローラーでステーブルコインが支払われているはず！

    ![](/images/web3_cloudflare_workers-1/11.png)

4. 検証が終わったら必ずサーバーを落とし、MCPサーバーの接続も解除する。

# 参考文献

- [【2026年最新】Claude Code作者が実践する「超並列駆動」開発術がエンジニアの常識を破壊していた](https://qiita.com/ot12/items/66e7c07c459e3bb7082d)
- [世界一わかりやすくGit worktreeを解説！AI駆動開発でも活用できる並列開発の方法](https://zenn.dev/tmasuyama1114/articles/git_worktree_beginner)
- [Claude Code × VibeKanban × git worktreeで実現するタスク並列実行のすすめ](https://zenn.dev/coconala/articles/379aadf643ecb8)
- [公式サイト - Vibekanban](https://vibekanban.com/)
- [GitHub - Vibekanban](https://github.com/BloopAI/vibe-kanban)
