---
title: "Sera ProtocolのGraphQLを使ってみよう！"
emoji: "🚀"
type: "tech"
topics: ["ethereum", "dex", "stablecoin", "clob", "defi"]
published: true
---

# はじめに

前回の記事で **Sera Protocol**の概要を取り上げました。

今回の記事では**Sera Protocol**のGraphQLの使い方を解説します！

# APIを早速使ってみよう！

**Sera Protocol**のGraphQLでは次の5つのデータを取得することができます！

- Market
- Order
- Depths
- Charts
- Tokens

それぞれ呼び出していきたいと思います！

## Market

マーケット`0xd99802ee8f16d6ff929e27546de15d03fdcce4bd`の情報を取得するには以下のcurlコマンドを実行します！

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "{ market(id: \"0xd99802ee8f16d6ff929e27546de15d03fdcce4bd\") { id quoteToken { symbol decimals } baseToken { symbol decimals } quoteUnit makerFee takerFee minPrice tickSpace latestPrice } }"}' \
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq
```

以下のような結果が返ってくればOKです！

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

## Order

オーダー情報を取得するには以下のcurlコマンドを実行します！

これはウォレットアドレス`0xda6e605db8c3221f4b3706c1da9c4e28195045f5`に関するものの情報を取得する例です。

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "{ openOrders(first: 10, where: { user: \"0xda6e605db8c3221f4b3706c1da9c4e28195045f5\" }) { id market { id } priceIndex isBid rawAmount status } }"}' \
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq
```

以下のようになればOKです！

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
      },
      {
        "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1-139843184478670403461003023281457089717564369994116372380703065822621335553",
        "market": {
          "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1"
        },
        "priceIndex": "20262",
        "isBid": false,
        "rawAmount": "15223933",
        "status": "pending"
      },
      {
        "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1-140685197532978852243070063496654886822763405288721159540432893777924849664",
        "market": {
          "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1"
        },
        "priceIndex": "20384",
        "isBid": false,
        "rawAmount": "1",
        "status": "cancelled"
      },
      {
        "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1-140685197532978852243070063496654886822763405288721159540432893777924849665",
        "market": {
          "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1"
        },
        "priceIndex": "20384",
        "isBid": false,
        "rawAmount": "10000485",
        "status": "cancelled"
      },
      {
        "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1-140685197532978852243070063496654886822763405288721159540432893777924849666",
        "market": {
          "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1"
        },
        "priceIndex": "20384",
        "isBid": false,
        "rawAmount": "10000485",
        "status": "cancelled"
      },
      {
        "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1-140685197532978852243070063496654886822763405288721159540432893777924849667",
        "market": {
          "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1"
        },
        "priceIndex": "20384",
        "isBid": false,
        "rawAmount": "15306523",
        "status": "cancelled"
      },
      {
        "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1-140685197532978852243070063496654886822763405288721159540432893777924849668",
        "market": {
          "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1"
        },
        "priceIndex": "20384",
        "isBid": false,
        "rawAmount": "15306523",
        "status": "cancelled"
      },
      {
        "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1-140685197532978852243070063496654886822763405288721159540432893777924849669",
        "market": {
          "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1"
        },
        "priceIndex": "20384",
        "isBid": false,
        "rawAmount": "15306523",
        "status": "cancelled"
      },
      {
        "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1-142079350295030546128131884180834845964158529301099577624575723671132307456",
        "market": {
          "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1"
        },
        "priceIndex": "20586",
        "isBid": false,
        "rawAmount": "374254",
        "status": "cancelled"
      },
      {
        "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1-591583188115153175039970098735075236656846805549584683575755763842956656640",
        "market": {
          "id": "0x002930b390ac7d686f07cffb9d7ce39609d082d1"
        },
        "priceIndex": "20179",
        "isBid": true,
        "rawAmount": "366928",
        "status": "cancelled"
      }
    ]
  }
}
```

## Depths

続いてDepthを取得する方法の解説です！

マーケット`0xd99802ee8f16d6ff929e27546de15d03fdcce4bd`のDepthを取得するには以下のcurlコマンドを実行します！

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "{ depths(first: 10, where: { market: \"0xd99802ee8f16d6ff929e27546de15d03fdcce4bd\", isBid: true, rawAmount_gt: \"0\" }, orderBy: priceIndex, orderDirection: desc) { priceIndex price rawAmount } }"}' \
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq
```

以下のようになればOKです！

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
      },
      {
        "priceIndex": "64058",
        "price": "100000000000000640580",
        "rawAmount": "10000000"
      },
      {
        "priceIndex": "64048",
        "price": "100000000000000640480",
        "rawAmount": "9950000"
      },
      {
        "priceIndex": "64047",
        "price": "100000000000000640470",
        "rawAmount": "10000000"
      },
      {
        "priceIndex": "64046",
        "price": "100000000000000640460",
        "rawAmount": "10000000"
      },
      {
        "priceIndex": "64036",
        "price": "100000000000000640360",
        "rawAmount": "9950000"
      },
      {
        "priceIndex": "64035",
        "price": "100000000000000640350",
        "rawAmount": "10000000"
      },
      {
        "priceIndex": "64034",
        "price": "100000000000000640340",
        "rawAmount": "10000000"
      },
      {
        "priceIndex": "64024",
        "price": "100000000000000640240",
        "rawAmount": "9950000"
      }
    ]
  }
}
```

## Charts

続いてチャート情報を取得してみましょう！

これはマーケット`0xd99802ee8f16d6ff929e27546de15d03fdcce4bd`のチャート情報を取得するためのcurlコマンドです！

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "{ chartLogs(first: 7, where: { market: \"0xd99802ee8f16d6ff929e27546de15d03fdcce4bd\", intervalType: \"1d\" }, orderBy: timestamp, orderDirection: desc) { timestamp open high low close baseVolume } }"}' \
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq
```

以下のようになればOKです！

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
      },
      {
        "timestamp": "1764288000",
        "open": "100.0000000000003",
        "high": "100.00000000000035",
        "low": "100.0000000000003",
        "close": "100.00000000000035",
        "baseVolume": "1.005999999999996478"
      }
    ]
  }
}
```

## Tokens

最後に最後にトークンの情報を首都する方法を紹介します！

今回はトークンシンボルに`USD`が含まれているものの情報を首都するcurlコマンドになります！

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "{ tokens(where: { symbol_contains_nocase: \"USD\" }) { id symbol name decimals } }"}' \
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq
```

以下のような結果が返ってくればOKです！

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

# まとめ

今回はここまでです！

実際にデータを取得してみて**Sera Protocol**に対する解像度が上がったのではないでしょうか？

次回はbunとTypeScriptを使ったスクリプトの実装方法の解説を紹介します！