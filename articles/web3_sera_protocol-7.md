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

```json
{
  "skill_name": "sera-protocol",
  "iteration": 1,
  "configs": [
    {
      "name": "with_skill",
      "pass_rate": {"mean": 1.0, "stddev": 0.0},
      "time": {"mean": 88.07, "stddev": 31.2},
      "tokens": {"mean": 31483, "stddev": 7460}
    },
    {
      "name": "without_skill",
      "pass_rate": {"mean": 0.83, "stddev": 0.14},
      "time": {"mean": 69.47, "stddev": 22.4},
      "tokens": {"mean": 23423, "stddev": 5020}
    }
  ],
  "delta": {
    "pass_rate": "+17%",
    "time": "+27%",
    "tokens": "+34%"
  },
  "evals": [
    {
      "eval_name": "graphql-orderbook",
      "with_skill": {"pass_rate": 1.0, "passed": 8, "total": 8, "time_s": 66.4, "tokens": 21513},
      "without_skill": {"pass_rate": 1.0, "passed": 8, "total": 8, "time_s": 51.1, "tokens": 18033}
    },
    {
      "eval_name": "limit-bid-flow",
      "with_skill": {"pass_rate": 1.0, "passed": 9, "total": 9, "time_s": 131.7, "tokens": 39321},
      "without_skill": {"pass_rate": 0.89, "passed": 8, "total": 9, "time_s": 101.0, "tokens": 30163}
    },
    {
      "eval_name": "mcp-chart-tool",
      "with_skill": {"pass_rate": 1.0, "passed": 7, "total": 7, "time_s": 66.1, "tokens": 33614},
      "without_skill": {"pass_rate": 0.71, "passed": 5, "total": 7, "time_s": 57.3, "tokens": 22072}
    }
  ],
  "analysis": {
    "observations": [
      "With-skill achieves 100% pass rate across all 3 evals (24/24 assertions)",
      "Without-skill drops on Eval 2 (complete_flow: missing market info fetch, wrong approve formula, no polling, no postOnly safety) and Eval 3 (wrong GraphQL entity name 'candles' vs 'chartLogs', missing '1w' interval)",
      "Eval 1 is non-discriminating - both pass 8/8. The without-skill agent found correct info by reading the codebase directly",
      "With-skill uses ~34% more tokens on average due to reading skill + reference files, but produces more complete and correct output",
      "The biggest skill advantage is domain-specific knowledge: correct GraphQL entity names (chartLogs), price formulas (rawAmount*quoteUnit for approve), and safety mechanisms (resolvePostOnlyBidPriceIndex)"
    ]
  }
}
```

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


