---
title: "Sera Protocolの深層へ。GraphQL APIで板情報やチャートデータを直接引っこ抜く方法"
emoji: "🚀"
type: "tech"
topics: ["ethereum", "dex", "stablecoin", "clob", "defi"]
published: true
---

:::message
この記事はAIと力を合わせて執筆しました。
:::

# はじめに

前回の記事で **Sera Protocol**の概要を取り上げました。

https://zenn.dev/mashharuki/articles/web3_sera_protocol-1

「板（CLOB）があるDEX」として非常に興味深いSeraですが、その真の面白さは**オンチェーンデータの透明性**にあります。今回は、Seraの心臓部からデータを直接引き出すための「GraphQL API」の使い方を徹底解説します！

なぜRESTではなくGraphQLなのか？ それは、DEXの膨大な板情報の中から「今、自分が必要なデータだけ」をピンポイントで、かつ高速に取得するためです。

# APIを早速叩いてみよう！

Sera Protocolでは、データのインデックスに **Goldsky** を採用しています。
ブラウザ上でポチポチとクエリを試したい方は、以下のプレイグラウンドも覗いてみてください。
[Goldsky Sera Subgraph](https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn)

今回は、主要な5つのデータを `curl` で取得する方法を紹介します！

**Tips:** 開発現場では、APIのレスポンスを `.json` ファイルとして保存しておくのが「鉄則」です。後で `jq` でフィルタリングしたり、挙動を比較したりする際に非常に役立ちます。

## 1. Market（マーケット情報の取得）

まずは基本となるマーケット情報です。特定のペアがどのような手数料設定になっているかを確認しましょう。

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "{ market(id: \"0xd99802ee8f16d6ff929e27546de15d03fdcce4bd\") { id quoteToken { symbol decimals } baseToken { symbol decimals } quoteUnit makerFee takerFee minPrice tickSpace latestPrice } }"}' \
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq . > market.json
```

実行結果のサンプル（`market.json`）：

```json
{
  "data": {
    "market": {
      "id": "0xd99802ee8f16d6ff929e27546de15d03fdcce4bd",
      "quoteToken": {
        "symbol": "TUSDC",
        "decimals": "6"
      },
      "baseToken": {
        "symbol": "TWETH",
        "decimals": "18"
      },
      "quoteUnit": "1000",
      "makerFee": "0",
      "takerFee": "0",
      "minPrice": "100000000000000000000",
      "tickSpace": "10",
      "latestPrice": "100000000000000640600"
    }
  }
}
```

ここで注目すべきは `latestPrice` です。これは単なる数値ではなく、プロトコル内部でのスケーリングがかかった状態の価格が返ってきます。

## 2. Order（注文履歴の追跡）

特定のウォレットがどのような注文を出しているか、あるいはキャンセルしたかを追跡できます。

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "{ openOrders(first: 10, where: { user: \"0xda6e605db8c3221f4b3706c1da9c4e28195045f5\" }) { id market { id } priceIndex isBid rawAmount status } }"}' \
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq . > orders.json
```

実行結果のサンプル（`orders.json`）：

```json
{
  "data": {
    "openOrders": [
      {
        "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1-139843184478670403461003023281457089717564369994116372380703065822621335552",
        "market": {
          "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1"
        },
        "priceIndex": "20262",
        "isBid": false,
        "rawAmount": "15223933",
        "status": "cancelled"
      }
      // ... 他のオーダーも同様に取得されます
    ]
  }
}
```

実際に叩いてみて気づいたのですが、`status` が `cancelled` になっているものも取得できるため、ユーザーの行動分析には非常に便利です。

## 3. Depths（板の厚みを知る）

CLOBにおいて最も重要な「板の厚み」を取得します。

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "{ depths(first: 10, where: { market: \"0xd99802ee8f16d6ff929e27546de15d03fdcce4bd\", isBid: true, rawAmount_gt: \"0\" }, orderBy: priceIndex, orderDirection: desc) { priceIndex price rawAmount } }"}' \
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq . > depths.json
```

実行結果のサンプル（`depths.json`）：

```json
{
  "data": {
    "depths": [
      {
        "priceIndex": "64060",
        "price": "100000000000000640600",
        "rawAmount": "9950000"
      },
      {
        "priceIndex": "64059",
        "price": "100000000000000640590",
        "rawAmount": "10000000"
      }
      // ... 深さに応じてリストが続きます
    ]
  }
}
```

## 4. Charts（ロウソク足データの取得）

チャート描画に必要なヒストリカルデータも一発で取れます。

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "{ chartLogs(first: 7, where: { market: \"0xd99802ee8f16d6ff929e27546de15d03fdcce4bd\", intervalType: \"1d\" }, orderBy: timestamp, orderDirection: desc) { timestamp open high low close baseVolume } }"}' \
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq . > charts.json
```

実行結果のサンプル（`charts.json`）：

```json
{
  "data": {
    "chartLogs": [
      {
        "timestamp": "1764374400",
        "open": "100.00000000000035",
        "high": "100.0000000000006406",
        "low": "100.00000000000022",
        "close": "100.0000000000006406",
        "baseVolume": "9.413999999999956363"
      }
    ]
  }
}
```

## 5. Tokens（トークン情報の検索）

最後に、プロトコルで扱われているトークン情報を取得する方法です。
「USD」を含むトークンを検索してみましょう。

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "{ tokens(where: { symbol_contains_nocase: \"USD\" }) { id symbol name decimals } }"}' \
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq . > tokens.json
```

実行結果のサンプル（`tokens.json`）：

```json
{
  "data": {
    "tokens": [
      {
        "id": "0x1920bf0643ae49b4fb334586dad6bed29ff30f88",
        "symbol": "USDT",
        "name": "USDT",
        "decimals": "6"
      },
      {
        "id": "0x4fcb0d963cb4dc4e60af0f78a859524087eccda9",
        "symbol": "TUSDC",
        "name": "Test USDC",
        "decimals": "6"
      }
    ]
  }
}
```

# なぜ実行結果をファイルに残すのか？

今回のようにコマンドの末尾に `> filename.json` を付けてリダイレクトするのは、単なる「整理整頓」以上の意味があります。

1. **デバッグの高速化**: APIを何度も叩かずに、手元のJSONファイルを使ってスクリプトの開発やテストが進められます（レートリミット対策にもなります）。
2. **履歴の保存**: プロトコルのアップデート前後でレスポンスがどう変わったか、Gitなどで管理して比較することが可能になります。
3. **チーム共有**: 取得したJSONをチームメンバーに送るだけで、同じデータに基づいた議論ができます。

# まとめ

いかがでしたでしょうか？
実際に `curl` で生データを叩いてファイルに保存してみると、Sera Protocol がオンチェーンでどのように「板」を表現しているのか、その解像度がぐっと上がったはずです。

APIでデータが取れるようになれば、次は「自動化」したくなりますよね？
次回は **Bun + TypeScript** を使って、これらの保存したJSONを活用しながら、プログラムから美しくデータを扱う実装方法を解説します。お楽しみに！
