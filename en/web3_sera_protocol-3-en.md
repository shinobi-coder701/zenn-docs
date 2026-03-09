---
title: "Let's Build a Script to Retrieve Data from Sera Protocol!"
emoji: "🚀"
type: "tech"
topics: ["ethereum", "dex", "stablecoin", "clob", "defi"]
published: true
---

:::message
This article was written in collaboration with AI.
:::

# Introduction

In my previous articles, I provided an overview of **Sera Protocol** and how to use its GraphQL API.

- [Part 1: Why Sera Protocol Replaced AMM with CLOB](https://dev.to/mashharuki/next-gen-on-chain-fx-why-sera-protocol-replaced-amm-with-clob-a-technical-deep-dive-1aoj)
- [Part 2: Hands-on with Sera Protocol's GraphQL API](https://dev.to/mashharuki/hands-on-with-sera-protocols-graphql-api-1i2p)

In this article, I will explain how to implement a script to retrieve information from **Sera Protocol**!

# Data Types Available via Sera Protocol GraphQL

As introduced in the previous article, you can retrieve the following five types of data using **Sera Protocol's** GraphQL:

- Market
- Order
- Depths
- Charts
- Tokens

In this guide, we will implement a script to fetch `Market` information, which is one of these data types.

# Implementing the Sample Code

Follow these commands in order to set up your environment. We will be using **Bun**, a fast all-in-one JavaScript runtime.

```bash
mkdir sample
cd sample
bun init -y
```

Update your `package.json` with the following content:

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

## 1. Prepare Two Utility Files

First, let's create a directory for utilities and add the following files.

- `utils/constants.ts`

  ```ts
  export const SUBGRAPH_URL = "https://api.goldsky.com/api/public/project_cmicv6kkbhyto01u3agb155hg/subgraphs/sera-pro/1.0.9/gn";
  ```

- `utils/helpers.ts`

  ```ts
  import { SUBGRAPH_URL } from "./constants";

  /**
   * Helper function to query the subgraph
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

## 2. Implement the Main Function

This script is simple and focuses on retrieving market information. Create `src/index.ts` and add the following:

```ts
import { querySubgraph } from "./utils/helpers";

/**
 * Main execution method
 */
const main = async () => {
  // Fetch market information (list)
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

## 3. Run the Script!

Execute the following command in your terminal:

```bash
bun run dev
```

If successful, you should see an output similar to this:

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
    // ... (additional markets)
  ]
}
```

As you can see, we have successfully retrieved a list of market information!

# Conclusion

That's it for this tutorial! 

By implementing this script, you now have a foundation for building automated trading tools or analytics dashboards powered by **Sera Protocol**.

Happy coding!
