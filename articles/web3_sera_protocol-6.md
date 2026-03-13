---
title: "【DEXを喋って動かす】Sera Protocol用MCPサーバーを開発。AIエージェントによるオンチェーンFXの幕開け"
emoji: "🎙️"
type: "tech"
topics: ["ethereum", "dex", "mcp", "typescript", "claude"]
published: true
---

:::message
この記事はAIと力を合わせて執筆しました。
:::

# はじめに

これまで連載形式で **Sera Protocol** の魅力を語ってきました。

1. [AMMを捨ててCLOBを選んだ技術的合理性](https://zenn.dev/mashharuki/articles/web3_sera_protocol-1)
2. [GraphQL APIでのデータ取得](https://zenn.dev/mashharuki/articles/web3_sera_protocol-2)
3. [Bun + TypeScriptでの自動化基盤](https://zenn.dev/mashharuki/articles/web3_sera_protocol-3)
4. [コントラクト呼び出しのチュートリアル](https://zenn.dev/mashharuki/articles/web3_sera_protocol-4)
5. [Reactによる実戦的ダッシュボードの自作](https://zenn.dev/mashharuki/articles/web3_sera_protocol-5)

6回目となる今回は **Model Context Protocol (MCP) SDK** を使ったSera ProtocolのMCPサーバーを開発しました。

**「喋れば動くDEX」**

AIエージェントが私の代わりに板を読み最適な指値を刺す。

そんな未来を実装した記録をシェアします！

ぜひ最後まで読んでいってください！

# MCP（Model Context Protocol）とは？：AIのための「USB規格」

Agent SKILLが出てきてそっちが主流になりつつありますがAIエージェント界隈で熱いトピックが **MCP** でしょう。

Anthropicが提唱したこのプロトコルは一言で言えば **「AIモデルと外部ツールを接続するための共通規格」** です。

これまでのAIエージェント開発は特定のプラットフォームに依存しがちでした。  
しかしMCPは「標準プロトコル」です。

一度MCPサーバーを作れば、**Claude Desktop**、**Cursor**、**Claude Code**、さらには自作のAIエージェントまであらゆる「知能」があなたのツールを理解し操作できるようになります。いわば、AIに「手足」を授けるためのUSBポートのようなものです。

# Sera Protocol MCP Server：AIにDEXを「解禁」する

今回開発したサーバーは、Sera ProtocolのオンチェーンオーダーブックをAIが直接読み書きできるように設計しました。

https://github.com/mashharuki/SeraProtocol-Sample/tree/main/mcp-server

### 提供する「8つの手足（Tools）」

AIは以下のツールを使い分け、人間と会話しながらトレードを完結させます。

| 分類 | ツール名 | AIができること |
| :--- | :--- | :--- |
| **Read** | `sera_get_market` | マーケットの詳細（最新価格、手数料、単位）を確認する |
| | `sera_list_markets` | 現在取引可能なペアの一覧を取得する |
| | `sera_get_orderbook` | 板情報（Bid/Ask）をリアルタイムで分析する |
| | `sera_get_orders` | ユーザーの注文履歴や約定状況をチェックする |
| | `sera_get_token_balance` | ウォレット内のトークン残高を確認する |
| **Write** | `sera_place_order` | 指値注文（買い/売り）を発行する |
| | `sera_claim_order` | 約定した注文から利益を回収（Claim）する |
| | `sera_approve_token` | トレードに必要なトークンの使用許可を出す |

### 実際の動作画面（MCP Client）

![](/images/web3_sera_protocol-6/0.png)
*`sera_get_market` によるマーケット詳細の取得。AIが人間にも分かりやすく整形してくれます。*

![](/images/web3_sera_protocol-6/1.png)
*`sera_list_markets` で現在取引可能なペアを一括取得。*

![](/images/web3_sera_protocol-6/2.png)
*`sera_get_orderbook` による板情報の可視化。スプレッドもAIが計算してくれます。*

### 1. 注文失敗を未然に防ぐ「シミュレーション」

オンチェーンの書き込みはガス代がかかります。AIが間違った注文を出してリバート（失敗）するのは避けたい。

そこで `placeLimitOrder` メソッド内では、トランザクションを送信する直前に `simulateContract` を実行しています。

```typescript
// services/blockchain.ts から抜粋
try {
  await publicClient.simulateContract({
    address: ROUTER_ADDRESS,
    abi: ROUTER_ABI,
    functionName,
    args: [orderParams],
    account,
    chain: sepolia,
  });
} catch (error) {
  if (reason.includes("0xe450d38c")) {
    throw new Error("ERC20InsufficientBalance: 残高が足りないよ！");
  }
}
```

このように実装することで無駄にガス代が消費するリスクを防げます。

## 2. Zodによる「AIへのガードレール」

AIは時に数値やアドレスを少しだけ間違えて解釈することがあります。

それをMCP側で厳格にブロックするために、**Zod** によるスキーマバリデーションを導入しました。

```typescript
// schemas/index.ts から抜粋
export const PlaceOrderInputSchema = z.object({
  market_id: AddressSchema,
  price_index: z.number().int().min(0).max(65535),
  raw_amount: z.string().regex(/^\d+$/),
  is_bid: z.boolean(),
});
```

## 3. 開発体験を最大化するデバッグ手法

MCPサーバー開発において、最も役立つのが **MCP Inspector** です。

これを使うと、Claude Desktopなどに組み込む前に、CLI上でツールの動作を個別に検証できます。

```bash
npx @modelcontextprotocol/inspector
```

これが無いと、AIとの「噛み合わない対話」で無限に時間を溶かすことになります。Web3エンジニアなら必須のツールです。

# セキュリティについて：AIに「財布」を渡すということ

:::info
**超重要**: このMCPサーバーを動かすには `PRIVATE_KEY` が必要です。
:::

AIに秘密鍵を扱わせることは、非常に強力ですがリスクも伴います。

- **必ず開発用（Sepolia等）用の秘密鍵を使ってください。**
- メインネットで運用する場合は、少額の「捨てウォレット」に限定し、AIが勝手に全財産を投げないようMCPサーバー側で1回あたりの注文上限額をハードコードするなどの防衛策を講じるべきです。

# 実践：AIと会話しながらトレードしてみた

![](/images/web3_sera_protocol-6/3.png)
*`sera_get_orders` で自分の注文履歴を確認。AIが「クレーム可能な注文」を教えてくれます。*

![](/images/web3_sera_protocol-6/4.png)
*`sera_get_token_balance` で残高チェック。AIが単位を適切に変換して表示。*

> **私**: 「TWETH/TUSDCの板情報を見せて。あと、私のTUSDC残高も教えて。」
>
> **AI**: （`sera_get_orderbook` と `sera_get_token_balance` を実行）
> 「現在の板は最良気配値が 20260 です。あなたのTUSDC残高は 9,998 です。」
>
> **私**: 「じゃあ、今の最良気配値の1つ下に 1,000 TUSDC 分の指値を出しておいて。Post Onlyでね。」
>
> **AI**: （`sera_place_order` を実行。シミュレーションで安全を確認後に送信）

# おわりに：AIエージェントが「流動性」になる未来

Sera ProtocolのMCPサーバーを開発して分かったのは、**「CLOB（板取引）」と「AIエージェント」は驚くほど相性が良い**ということです。

AMMではスリッページを気にする必要がありますが、CLOBならAIは「特定の価格インデックス」を指定して精密に動けます。

将来、オンチェーンFXの流動性の大部分は、人間ではなく、このようにMCPで武装したAIエージェントたちが供給するようになるでしょう。

Sera Protocolはそんな **「AIエージェント・ネイティブな金融」** のインフラとして進化を続けています。

今回はここまでになります！

ありがとうございました！

## 参考文献
- [Sera Protocol MCP Server ソースコード](https://github.com/mashharuki/SeraProtocol-Sample/tree/main/mcp-server)
- [Model Context Protocol 公式ドキュメント](https://modelcontextprotocol.io/)
