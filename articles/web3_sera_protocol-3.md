---
title: "Sera Protocolの情報を取得するスクリプトを実装してみよう！"
emoji: "🚀"
type: "tech"
topics: ["ethereum", "dex", "stablecoin", "clob", "defi"]
published: true
---

:::message
この記事はAIと力を合わせて執筆しました。
:::

# はじめに

これまで記事で **Sera Protocol**の概要を取り上げてきました。

https://zenn.dev/mashharuki/articles/web3_sera_protocol-1

https://zenn.dev/mashharuki/articles/web3_sera_protocol-2

今回の記事では**Sera Protocol**の情報を取得するスクリプトの実装方法を解説します！

# Sera ProtocolのGraphQLで取得できる種類のデータ

前回の記事でも紹介しましたが、**Sera Protocol**のGraphQLでは次の5つのデータを取得することができます！

- Market
- Order
- Depths
- Charts
- Tokens

この記事ではその内の一つである`Market`を取得するスクリプトを実装してみたいと思います。

# サンプルコードを実装してみよう！

以下のコマンドを順番に実行して環境をセットアップします。

```bash
mkdir sample
cd sample
bun init -y
```

`package.json`の内容を以下のようにします。

```json
{
  "name": "api-sample-app",
  "module": "index.ts",
  "type": "module",
  "scripts": {
    "dev": "bun run ./src/index.ts"
  },
  "devDependencies": {
    "@types/bun": "latest"
  },
  "peerDependencies": {
    "typescript": "^5.0.0"
  }
}
```

## 2つのユーティリティファイルを用意

- `utils/constants.ts`

  ```ts
  export const SUBGRAPH_URL = "https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn";
  ```

- `utils/helpers.ts`

  ```ts
  import { SUBGRAPH_URL } from "./constants";

  /**
   * API call helper function to query the subgraph
   * @param query 
   * @param variables 
   * @returns 
   */
  export async function querySubgraph(query: any, variables = {}) {
    const response = await fetch(SUBGRAPH_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, variables })
    });
    
    const { data, errors } = await response.json();
    if (errors) throw new Error(errors[0].message);
    return data;
  }
  ```

## メイン関数を実装

今回はマーケットの情報を取得するだけのシンプルな内容となっています。

```ts
import { querySubgraph } from "./utils/helper";

/**
 * main method
 */
const main = async () => {
  // get markets info(list)
  const data = await querySubgraph(`
    query GetMarkets($first: Int!) {
      markets(first: $first) {
        id
        quoteToken { symbol }
        baseToken { symbol }
      }
    }
  `, { first: 10 });

  console.log(JSON.stringify(data, null, 2));
};

main().catch(console.error);
```

## 動かしてみよう！

以下のコードを実行します！

```bash
bun run dev
```

以下のようになればOKです！

```json
{
  "markets": [
    {
      "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1",
      "quoteToken": {
        "symbol": "AUDD"
      },
      "baseToken": {
        "symbol": "MYRC"
      }
    },
    {
      "id": "0x00382985b0cfa69ff72f22f21cc99e902d334c5b",
      "quoteToken": {
        "symbol": "MYRC"
      },
      "baseToken": {
        "symbol": "KRWO"
      }
    },
    {
      "id": "0x004b97c5ecf61c89b1dd48725b5df3b03d2539ec",
      "quoteToken": {
        "symbol": "GYEN"
      },
      "baseToken": {
        "symbol": "BRLA"
      }
    },
    {
      "id": "0x00630dbaa9a7605d7f7f336036be5978d59ef4f8",
      "quoteToken": {
        "symbol": "BRZ"
      },
      "baseToken": {
        "symbol": "A7A5"
      }
    },
    {
      "id": "0x0072b15dba7dff1cae17c3806cbeeddcec46ca64",
      "quoteToken": {
        "symbol": "IDRX"
      },
      "baseToken": {
        "symbol": "JPYC"
      }
    },
    {
      "id": "0x00b9608d7df89612df1af6929f0334dde36aed1a",
      "quoteToken": {
        "symbol": "VGBP"
      },
      "baseToken": {
        "symbol": "MYRC"
      }
    },
    {
      "id": "0x00bc05c5ff325b5e75962b7200fd6992e3f2c43e",
      "quoteToken": {
        "symbol": "XSGD"
      },
      "baseToken": {
        "symbol": "ARC"
      }
    },
    {
      "id": "0x0148d96aca15f325c6b4aa0685a28597545a23a3",
      "quoteToken": {
        "symbol": "MYRC"
      },
      "baseToken": {
        "symbol": "ZARP"
      }
    },
    {
      "id": "0x0196a2f505494ea26cea1948b2d3202174cc6acb",
      "quoteToken": {
        "symbol": "THBK"
      },
      "baseToken": {
        "symbol": "CADC"
      }
    },
    {
      "id": "0x0206ea31e927a65528b14cc8a2a2f7ca0b261836",
      "quoteToken": {
        "symbol": "ARZ"
      },
      "baseToken": {
        "symbol": "KRWIN"
      }
    }
  ]
}
```

ちゃんとマーケットの情報がリストで取得できましたね！

今回はここまでになります！