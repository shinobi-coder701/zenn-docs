---
title: "Hands-on with Sera Protocol's GraphQL API!"
emoji: "🚀"
type: "tech"
topics: ["ethereum", "dex", "stablecoin", "clob", "defi"]
published: true
---

# Introduction

In the previous article, we covered the overview of **Sera Protocol**.

In this article, I will explain how to use **Sera Protocol's** GraphQL API!

# Let's Use the API Right Away!

With **Sera Protocol's** GraphQL, you can retrieve the following five types of data:

- Market
- Order
- Depths
- Charts
- Tokens

Let's call each of them!

## Market

To get information about the market `0xd99802ee8f16d6ff929e27546de15d03fdcce4bd`, run the following curl command:

```bash
curl -s -X POST 
  -H "Content-Type: application/json" 
  -d '{"query": "{ market(id: "0xd99802ee8f16d6ff929e27546de15d03fdcce4bd") { id quoteToken { symbol decimals } baseToken { symbol decimals } quoteUnit makerFee takerFee minPrice tickSpace latestPrice } }"}' 
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq
```

If you get a result like this, you're good to go!

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

To retrieve order information, run the following curl command.

This example retrieves information related to the wallet address `0xda6e605db8c3221f4b3706c1da9c4e28195045f5`.

```bash
curl -s -X POST 
  -H "Content-Type: application/json" 
  -d '{"query": "{ openOrders(first: 10, where: { user: "0xda6e605db8c3221f4b3706c1da9c4e28195045f5" }) { id market { id } priceIndex isBid rawAmount status } }"}' 
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq
```

The output should look like this:

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
      // ... (other orders)
    ]
  }
}
```

## Depths

Next, here's how to retrieve market Depth.

To get the Depth of the market `0xd99802ee8f16d6ff929e27546de15d03fdcce4bd`, run the following curl command:

```bash
curl -s -X POST 
  -H "Content-Type: application/json" 
  -d '{"query": "{ depths(first: 10, where: { market: "0xd99802ee8f16d6ff929e27546de15d03fdcce4bd", isBid: true, rawAmount_gt: "0" }, orderBy: priceIndex, orderDirection: desc) { priceIndex price rawAmount } }"}' 
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq
```

You should see something like this:

```json
{
  "data": {
    "depths": [
      {
        "priceIndex": "64060",
        "price": "100000000000000640600",
        "rawAmount": "9950000"
      },
      // ... (other depth levels)
    ]
  }
}
```

## Charts

Now, let's fetch some chart information.

This curl command retrieves chart data for the market `0xd99802ee8f16d6ff929e27546de15d03fdcce4bd`:

```bash
curl -s -X POST 
  -H "Content-Type: application/json" 
  -d '{"query": "{ chartLogs(first: 7, where: { market: "0xd99802ee8f16d6ff929e27546de15d03fdcce4bd", intervalType: "1d" }, orderBy: timestamp, orderDirection: desc) { timestamp open high low close baseVolume } }"}' 
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq
```

The output should look like this:

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
      // ... (other logs)
    ]
  }
}
```

## Tokens

Finally, let's see how to fetch token information.

This curl command retrieves information for tokens whose symbol contains `USD`:

```bash
curl -s -X POST 
  -H "Content-Type: application/json" 
  -d '{"query": "{ tokens(where: { symbol_contains_nocase: "USD" }) { id symbol name decimals } }"}' 
  https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn | jq
```

You should get a result like this:

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

# Summary

That's it for this time!

By actually fetching data, I hope your "resolution" on **Sera Protocol** has improved.

In the next article, I will introduce how to implement a script using Bun and TypeScript!
