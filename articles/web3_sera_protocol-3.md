---
title: "curl 卒業。Bun + TypeScript で Sera Protocol の自動化基盤を爆速で構築する"
emoji: "🚀"
type: "tech"
topics: ["ethereum", "dex", "defi", "typescript", "bun"]
published: true
---

:::message
この記事はAIと力を合わせて執筆しました。
:::

# はじめに

前回までの記事で、Sera Protocol の概要と `curl` を使ったデータ取得の基本を学びました。

https://zenn.dev/mashharuki/articles/web3_sera_protocol-1

https://zenn.dev/mashharuki/articles/web3_sera_protocol-2

しかし、私たちはエンジニアです。いつまでも手動で `curl` を叩いているわけにはいきません。今回は、**Bun + TypeScript** を使って、Sera Protocol のデータを自動で引っこ抜き、自由自在に扱うための「最強の自動化基盤」を構築します。

なぜ Node.js ではなく **Bun** なのか？ それは TypeScript を設定なしでそのまま実行できる爆速な体験と、`fetch` が標準搭載されているスマートさがあるからです。正直、一度この体験を知ると元には戻れません。

# 自動化基盤をセットアップする

まずは爆速で環境を作りましょう。

```bash
mkdir sera-api-client
cd sera-api-client
bun init -y
```

`package.json` に開発用のスクリプトを追加しておきます。

```json
{
  "name": "sera-api-client",
  "module": "src/index.ts",
  "type": "module",
  "scripts": {
    "dev": "bun run ./src/index.ts"
  },
  "devDependencies": {
    "@types/bun": "latest"
  }
}
```

# 型安全な GraphQL クライアントの実装

ここからが TypeScript の真骨頂です。GraphQL のレスポンスに型を当てることで、プロパティの補完が効く「最高に気持ちいい」開発体験を手に入れます。

## 1. 共通定数とヘルパー関数の定義

まずは API のエンドポイントと、通信を支えるヘルパー関数を実装します。

- `src/utils/constants.ts`

```ts
export const SUBGRAPH_URL = "https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn";
```

- `src/utils/helpers.ts`

```ts
import { SUBGRAPH_URL } from "./constants";

/**
 * GraphQL Subgraph へのクエリ実行ヘルパー
 * 型引数 T を渡すことでレスポンスを型安全に扱えます
 */
export async function querySubgraph<T>(query: string, variables = {}): Promise<T> {
  const response = await fetch(SUBGRAPH_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, variables })
  });
  
  const { data, errors } = await response.json();
  if (errors) {
    throw new Error(`[GraphQL Error] ${errors[0].message}`);
  }
  return data as T;
}
```

## 2. マーケット情報の型定義とメイン関数

今回はマーケットの情報を取得するスクリプトを実装します。
`Market` インターフェースを定義することで、`data.markets[0].id` と打つときに VS Code が完璧に補完してくれます。

- `src/index.ts`

```ts
import { querySubgraph } from "./utils/helpers";

/**
 * Sera Protocol のマーケット型定義
 */
interface Market {
  id: string;
  quoteToken: { symbol: string; decimals: string };
  baseToken: { symbol: string; decimals: string };
}

interface GetMarketsResponse {
  markets: Market[];
}

const main = async () => {
  console.log("🚀 Sera Protocol からマーケット情報を取得中...");

  const data = await querySubgraph<GetMarketsResponse>(`
    query GetMarkets($first: Int!) {
      markets(first: $first) {
        id
        quoteToken { symbol decimals }
        baseToken { symbol decimals }
      }
    }
  `, { first: 10 });

  console.log(`✅ ${data.markets.length} 件のマーケットが見つかりました：`);
  console.table(data.markets.map(m => ({
    ID: m.id.slice(0, 10) + "...",
    Pair: `${m.baseToken.symbol}/${m.quoteToken.symbol}`
  })));
};

main().catch((err) => {
  console.error("❌ エラーが発生しました:", err.message);
  process.exit(1);
});
```

# 動かしてみよう！

準備は整いました。以下のコマンドを叩いてみてください。

```bash
bun run dev
```

`console.table` を使ったことで、ターミナル上に整然とマーケットリストが表示されるはずです。`curl` で見ていたあの無機質な JSON が、あなたの手で制御可能な「データ」に変わった瞬間です！

# 著者のこだわり：なぜ Interface を書くのか？

「GraphQL のクエリを書くのも Interface を書くのも二度手間で面倒だ」と思うかもしれません。しかし、自動化ボットを運用する際、プロパティの打ち間違いによるランタイムエラーは致命傷になります。
**「コンパイルが通れば、通信も通る」**。この安心感こそが、伝説のブロガーが TypeScript を愛してやまない理由です。

# おわりに：自動化の先にある未来

今回はマーケット情報の取得までですが、この基盤さえあれば次のようなことが数行で実装できます：

- `setInterval` で回して、新しいマーケットが作られたら Discord に通知する
- 特定のペアの板（Depth）を監視して、裁定機会を見つける
- 定期的にチャートデータを取得して、独自のテクニカル分析を行う

**Sera Protocol の自動化ボット開発**の土台は完成しました。
次回は、いよいよ板情報のデータを活用した、より実践的なロジックの実装に踏み込んでいきたいと思います。お楽しみに！
