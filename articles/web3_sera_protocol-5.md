---
title: "Sera Protocolをフル活用！Reactで実戦的なDeFiダッシュボードを自作してみた"
emoji: "📈"
type: "tech"
topics: ["ethereum", "react", "tailwindcss", "web3", "defi"]
published: true
---

# はじめに

これまで、**Sera Protocol**の概要からGraphQL（Subgraph）の使い方、そしてCLIでの基本的なトレード方法までを連載形式で紹介してきました。

https://zenn.dev/mashharuki/articles/web3_sera_protocol-1

https://zenn.dev/mashharuki/articles/web3_sera_protocol-2

https://zenn.dev/mashharuki/articles/web3_sera_protocol-3

https://zenn.dev/mashharuki/articles/web3_sera_protocol-4

しかし、DeFiの真髄は「触ってなんぼ」です。

CLIで黒い画面に向き合うのも硬派で良いですが、やはり**直感的に板（OrderBook）を眺め、カチカチと注文を出したい**。

そこで今回はSera Protocolの機能をReact.js製のフロントエンドアプリから呼び出し、**「実戦で使えるレベル」のDeFiダッシュボード**を自作しました。

開発を通して得られた、学びをシェアするための記事となっていますのでぜひ最後まで読んでいってください。

# 今回試したサンプルコード

https://github.com/mashharuki/SeraProtocol-Sample

# アプリのコンセプト：信頼をデザインする

今回作成したダッシュボードは、モダンなDeFiにありがちな「AI感のある紫色のグラデーション」をあえて避けました。

目指したのは、**「日経新聞」や「ブルームバーグ端末」のような、情報の密度と信頼性を重視した硬派なUI**です。

![Dashboard Overview](/images/web3_sera_protocol-5/0.png)
*情報の密度と可読性を重視したダッシュボード画面*

:::message
**技術スタック**
- **Frontend**: React 19 + Vite
- **Styling**: Tailwind CSS v4 (新機能の `@theme` をフル活用)
- **Web3**: Ethers.js + Reown (AppKit)
- **Data**: Apollo Client (Subgraph)
:::

# こだわりの実装ポイント

単にコントラクトを呼び出すだけなら簡単ですが、ユーザーが迷わずかつ安全に取引できるようにするために以下の3つのポイントを意識しました。

## 1. 注文ボタンの「4段変身」ロジック

Web3アプリで最もユーザーが離脱するのは、**「今、何をすべきか分からない」** 瞬間です。

Walletが未接続なのか、ネットワークが違うのか、あるいはトークンのApproveが必要なのか……。

これらを解決するために、`OrderForm.tsx` ではユーザーの状態に合わせて**ボタン1つが4つの役割を自動で切り替える**ように実装しました！

![Trade Page](/images/web3_sera_protocol-5/1.png)
*板情報と連動した注文フォーム。状況に応じてボタンの役割が変化する*

```tsx
// src/components/trading/OrderForm.tsx から抜粋
{notConnected ? (
  <button onClick={connect}>Connect Wallet</button>
) : wrongNetwork ? (
  <button onClick={switchToSepolia}>Switch to Sepolia</button>
) : needsApproval ? (
  <button onClick={approve}>Approve {tokenSymbol}</button>
) : (
  <button type="submit">Place {isBid ? "Bid" : "Ask"} Order</button>
)}
```

これにより、ユーザーは「次に押すべきボタン」を迷うことがなくなります。

## 2. Post Only Safety：手数料損を防ぐフロントエンドの知恵

Sera Protocolのような板取引（CLOB）では、**Maker（指値）** として注文を出すことで手数料を抑える（あるいはリベートを得る）のが定石です。

しかし、価格入力をミスして現在の最良気配値（Best Ask/Bid）を突き抜けてしまうと意図せず **Taker（成行）** として即座に約定してしまいます。

これを防ぐため、フロントエンド側で **「Post Only」フラグがONの場合は、価格インデックスを自動補正するロジック** を組み込みました。

![Order Placement Flow](/images/web3_sera_protocol-5/2.png)
*注文実行時のフロー。安全性を考慮したインデックス補正が行われる*

```typescript
// src/hooks/usePlaceOrder.ts から抜粋
function resolvePostOnlyPriceIndex(params: PlaceOrderParams): number {
  if (!params.postOnly) return params.priceIndex;

  let resolved = params.priceIndex;
  const bestBid = params.bestBidIndex ? Number.parseInt(params.bestBidIndex, 10) : undefined;
  const bestAsk = params.bestAskIndex ? Number.parseInt(params.bestAskIndex, 10) : undefined;

  // 買い注文（Bid）が売り板（Ask）に突き刺さらないように補正
  if (params.isBid && Number.isInteger(bestAsk) && resolved >= (bestAsk as number)) {
    resolved = (bestAsk as number) - 1;
  }
  // ...売り注文も同様に補正
  return resolved;
}
```

「ユーザーのミスをシステムがカバーする」という金融アプリとしての矜持です。

## 3. 泥臭いエラーハンドリング：`execution reverted` を翻訳する

スマートコントラクトのエラーメッセージは、そのまま表示すると `execution reverted: 0x...` のような一般ユーザーには呪文にしか見えないものになります。これを可能な限り「人間が読める言葉」に変換するパーサーを実装しました。

```typescript
// src/hooks/usePlaceOrder.ts から抜粋
function parseContractError(err: unknown): string {
  if (!(err instanceof Error)) return "Transaction failed";
  const msg = err.message;

  if (msg.includes("user rejected")) return "ユーザーによってキャンセルされました";
  if (msg.includes("insufficient funds")) return "ガス代（ETH）が不足しています";
  if (msg.includes("execution reverted")) {
    return "コントラクトでエラーが発生しました。残高不足や価格設定が無効な可能性があります。";
  }
  return msg.slice(0, 100) + "...";
}
```

![Error Handling](/images/web3_sera_protocol-5/4.png)
*エラー発生時も、可能な限り分かりやすい言葉でユーザーをナビゲートする*

この「ひと手間」がアプリのUXを向上させるポイントになります！

# サンプルコードの構成

実装したソースコードの全体像は以下の通りです。  
非常にクリーンな構成を意識しました。

![My Orders Page](/images/web3_sera_protocol-5/3.png)
*自分の注文一覧。約定状況や請求可能額がリアルタイムに更新される*

- `hooks/`: Web3の複雑なロジック（Wallet, Token, Order）をカプセル化
- `components/`: UIパーツ。Tailwind v4 の `@layer` と `theme` で一貫性を保持
- `lib/`: Subgraphクエリやフォーマッタなど、ピュアなユーティリティ

特に `useOrders.ts` では、Subgraphから自分の注文履歴を定期的にポーリングし、**「約定（Filled）」や「請求可能（Claimable）」の状態をリアルタイムに反映**するようにしています。

# おわりに

Sera Protocolのコントラクトは、非常に洗練されたインターフェースを持っています。  

今回作成したダッシュボードは単なる「動くもの」ではなく、「トレードの道具」としての使い心地を追求しました。ブロックチェーンという「信頼の基盤」の上に優れたUI/UXという「使いやすさ」を乗せる。

これこそが、Web3をマスアダプションへ導く唯一の道だと信じています。

皆さんもぜひ、自分だけの最強のDeFiフロントエンドを作ってみてください！

---

**参考リンク**
- [Sera Protocol 公式ドキュメント](https://sera-protocol.gitbook.io/)
- [今回のサンプルコード (Frontend)](https://github.com/your-repo/sera-frontend)
