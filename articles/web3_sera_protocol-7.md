---
title: "オンチェーンFX SeraProtocolのAgent SKILLを作ってみた！"
emoji: "💪"
type: "tech"
topics: ["ethereum", "dex", "mcp", "typescript", "claude"]
published: true
---

# はじめに

これまで連載形式で **Sera Protocol** の魅力を語ってきました。

1. [AMMを捨ててCLOBを選んだ技術的合理性](https://zenn.dev/mashharuki/articles/web3_sera_protocol-1)
2. [GraphQL APIでのデータ取得](https://zenn.dev/mashharuki/articles/web3_sera_protocol-2)
3. [Bun + TypeScriptでの自動化基盤](https://zenn.dev/mashharuki/articles/web3_sera_protocol-3)
4. [コントラクト呼び出しのチュートリアル](https://zenn.dev/mashharuki/articles/web3_sera_protocol-4)
5. [Reactによる実戦的ダッシュボードの自作](https://zenn.dev/mashharuki/articles/web3_sera_protocol-5)
6. [SeraProcolのMCPサーバーの実装](https://zenn.dev/mashharuki/articles/web3_sera_protocol-6)

7回目となる今回はその集大成として**SeraProcol**の**Agent SKILL**を作ってみたことについてまとめたいと思います！

ぜひ最後まで読んでいってください！

# 作成したSKILLについて

今回作成したスキルは以下のGitHubリポジトリから確認できます！

https://github.com/mashharuki/SeraProtocol-Sample/tree/main/.claude/skills/sera-protocol

## Agent SKILLの内容

このスキルには以下の4つの観点からSeraProtocolを使ったアプリ開発を包括的に支援するための機能が含まれています。

- GraphQLを使って開発するパターン
- スマートコントラクトを使って開発するパターン
- フロントエンドアプリケーションとのインテグレーションを行うパターン
- MCPサーバーを開発するパターン

# SKILLの実装方法

SKILLの実装には**Anthropic**社の**skill-creator**を使いました！  
最近アップデートされて生成される**Agent SKILL**の質が上がったと話題になっています！

https://github.com/anthropics/skills/tree/main/skills

また、スキル作成を依頼した際にはこれまでのブログ記事の内容と実装してきたサンプルコードをコンテキストとして渡してみました！

今回はその結果がどうなったのかも含めて共有していきます！

:::message
モデルは**Claude Opus 4.6**を使いました。
:::

# 作成されたSKILLの3つの評価シナリオ

**skill-creator**のアップデートとして作成したスキルを評価する機能が盛り込まれました。

具体的には3つの評価シナリオを用意し、スキルを使った場合と使わなかった場合でそれぞれどの程度要件を満たすことに成功したかを計測するというものです！

今回だと以下のようなシナリオが用意されました。

## シナリオ1
 
- **プロンプト**:  

  ```bash
  SeraProtocolのサブグラフからTWETH/TUSDCマーケットの板情報（bid/ask各5本）を取得するTypeScriptスクリプトを書いてください。viemは使わずfetchだけで。
  ```

- **期待される結果**： 

  ```bash
  GraphQL queryを使い、depths entityからbid/askを取得するfetch-basedのTypeScriptコード。正しいsubgraph URL、適切なwhere/orderBy/orderDirection条件、rawAmount_gt:0フィルタを含む。
  ```

## シナリオ2

- **プロンプト**:  

  ```bash
  Sera ProtocolでlimitBidを出すための完全な手順を教えて。トークンのapproveからtx送信、確認待ちまで。viemを使った具体的なコード例をください。priceIndex=12000, rawAmount=500で。
  ```

- **期待される結果**：  

  ```bash
  "1)ERC20 approve→2)simulateContract→3)writeContract→4)waitForTransactionReceiptの完全なフロー。正しいROUTER_ADDRESS、LimitOrderParams構造体、deadline設定、postOnly=trueの安全設定を含むviemコード。
  ```

## シナリオ3

- **プロンプト**: 

  ```bash
  SeraProtocolのMCPサーバーに新しいツール sera_get_chart_data を追加したい。OHLCV(ローソク足)データを返すread-onlyツールです。どのファイルをどう変更すればいい？
  ```
  
- **期待される結果**：   

  ```bash
  1)schemas/index.tsにZodスキーマ追加 2)services/subgraph.tsにchartLogs GraphQLクエリ関数追加 3)tools/read-tools.tsにツール登録。intervalType(1m,5m,15m,1h,4h,1d,1w)パラメータを含む。既存のコード構造・パターンに沿った実装方針。
  ```

# 3つの評価シナリオの結果

結果は以下のようになりました！

まずは全体サマリーです。

| 項目 | SKILLあり | SKILLなし | 差分（あり基準） |
| :--- | :--- | :--- | :--- |
| 平均Pass Rate | 1.00 (±0.00) | 0.83 (±0.14) | **+17%** |
| 平均実行時間 | 88.07s (±31.2) | 69.47s (±22.4) | +27% |
| 平均トークン数 | 31,483 (±7,460) | 23,423 (±5,020) | +34% |

続いて、シナリオ別の比較です。

| シナリオ | SKILLあり <br/>（Pass / Time / Tokens） | SKILLなし<br/>（Pass / Time / Tokens） | コメント |
| :--- | :--- | :--- | :--- |
| graphql-orderbook | 8/8 (100%)<br/> 66.4s<br/> 21,513 | 8/8 (100%)<br/> 51.1s<br/> 18,033 | 両者とも要件達成 |
| limit-bid-flow | 9/9 (100%)<br/> 131.7s<br/> 39,321 | 8/9 (89%)<br/> 101.0s<br/> 30,163 | SKILLなしで精度低下 |
| mcp-chart-tool | 7/7 (100%)<br/> 66.1s<br/> 33,614 | 5/7 (71%)<br/> 57.3s<br/> 22,072 | 差が最も大きい |

分析ポイントをまとめると以下の通りです。

- **SKILLありは3シナリオすべてで100%達成（24/24 assertions）**
- SKILLなしはシナリオ2・3で失点（市場情報取得漏れ、approve式の誤り、ポーリング不足、postOnly安全策不足、`candles`/`chartLogs`取り違え、`1w` interval欠落）
- シナリオ1は識別力が低く、両者とも満点
- SKILLありはトークン消費が増える一方で、ドメイン固有知識を踏まえた実装の正確性・網羅性が向上

中々の精度ですね！

## 実際に生成されたコードの比較

次に実際に生成されたコードをシナリオごとにみていこうと思います。

### シナリオ ①

こちらのシナリオでは`viem`を使用せず、GraphQLのみを使ってSeraProtocolのデータを取得するシンプルなスクリプトの実装を試していますが、両方のパターンともに要件を満たせていそうです！

- **SKILL**あり

  https://github.com/mashharuki/SeraProtocol-Sample/tree/main/sera-protocol-workspace/iteration-1/eval-1-graphql-orderbook/with_skill

- **SKILL**なし

  https://github.com/mashharuki/SeraProtocol-Sample/tree/main/sera-protocol-workspace/iteration-1/eval-1-graphql-orderbook/without_skill

### シナリオ ②

次に`viem`を使った場合(書き込み系の処理)も入ってくるパターンのシナリオの結果ですが、SKILLを使用していないパターンだと精度が落ちていることがわかります。

SKILLありの場合にはトランザクション処理をシミュレーションするロジックが実装されており丁寧です。

- **SKILL**あり

  https://github.com/mashharuki/SeraProtocol-Sample/tree/main/sera-protocol-workspace/iteration-1/eval-2-limit-bid-flow/with_skill

- **SKILL**なし

  https://github.com/mashharuki/SeraProtocol-Sample/tree/main/sera-protocol-workspace/iteration-1/eval-2-limit-bid-flow/without_skill

### シナリオ ③

最後に最も難しいMCPサーバーの実装についてですが、SKILLありとなしの場合でより鮮明に結果が分かれました。

SKILLがある場合についてはビルド・テストコマンドに加えて、**MCP Inspector**を使った稼働確認方法まで出力されていました。

- **SKILL**あり

  https://github.com/mashharuki/SeraProtocol-Sample/tree/main/sera-protocol-workspace/iteration-1/eval-3-mcp-chart-tool/with_skill

- **SKILL**なし

  https://github.com/mashharuki/SeraProtocol-Sample/tree/main/sera-protocol-workspace/iteration-1/eval-3-mcp-chart-tool/without_skill

# まとめ

これまで調べてきたことそしてサンプルコードを作りながら試したことをSKILLにして試してみました！

より複雑な実装方法になればなるほどSKILLが力を発揮することが確認できました。

SeraProtocolはまだテストネットのみの対応とのことですので、メインネットが出る前に皆さんもSKILLを使ってSeraProtocol上での開発をマスターしてみてはいかがでしょうか？！

https://sera.cx/

ここまで読んでいただきありがとうございました！！


