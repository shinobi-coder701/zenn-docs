---
title: "[DEX via Natural Language] Building an MCP Server for Sera Protocol: The Dawn of AI-Agent Driven On-Chain FX"
emoji: "🎙️"
type: "tech"
topics: ["ethereum", "dex", "mcp", "typescript", "claude"]
published: true
---

:::message
This article was written in collaboration with AI.
:::

# Introduction

I have been sharing the brilliance of **Sera Protocol** through a series of articles:

1. [Technical Rationality for CLOB over AMM](https://zenn.dev/mashharuki/articles/web3_sera_protocol-1)
2. [Direct Data Extraction via GraphQL API](https://zenn.dev/mashharuki/articles/web3_sera_protocol-2)
3. [Rapid Automation with Bun + TypeScript](https://zenn.dev/mashharuki/articles/web3_sera_protocol-3)
4. [Tutorial: Interacting with Smart Contracts](https://zenn.dev/mashharuki/articles/web3_sera_protocol-4)
5. [Building a Practical DeFi Dashboard with React](https://zenn.dev/mashharuki/articles/web3_sera_protocol-5)

For the 6th entry in this series, I have developed an MCP server for Sera Protocol using the **Model Context Protocol (MCP) SDK**.

**"A DEX that moves when you speak."**

Imagine an AI agent reading the order book on your behalf and placing optimal limit orders.

I’m excited to share the journey of implementing this future!

# What is MCP (Model Context Protocol)?: The "USB Standard" for AI

While "Agent Skills" are becoming mainstream, **MCP** is undoubtedly the hottest topic in the AI agent space right now.

Proposed by Anthropic, this protocol is, in short, a **"universal standard for connecting AI models to external tools and data."**

Previously, AI agent development often depended on specific platforms.  
However, MCP is a "standard protocol."

Once you build an MCP server, any "intelligence"—from **Claude Desktop** and **Cursor** to **Claude Code** and your own custom AI agents—can understand and operate your tools. It’s like providing a USB port to give "hands and feet" to an AI.

# Sera Protocol MCP Server: "Unlocking" DEX for AI

The server I developed is designed to allow AI to directly read and write the on-chain order book of Sera Protocol.

https://github.com/mashharuki/SeraProtocol-Sample/tree/main/mcp-server

### The "8 Hands and Feet" (Tools)

The AI utilizes the following tools to complete trades through conversation:

| Category | Tool Name | What AI Can Do |
| :--- | :--- | :--- |
| **Read** | `sera_get_market` | Check market details (latest price, fees, units). |
| | `sera_list_markets` | List all currently tradable pairs. |
| | `sera_get_orderbook` | Analyze order book (Bid/Ask) in real-time. |
| | `sera_get_orders` | Check user's order history and execution status. |
| | `sera_get_token_balance` | View ERC20 token balances in the wallet. |
| **Write** | `sera_place_order` | Submit limit orders (Buy/Sell). |
| | `sera_claim_order` | Collect proceeds from filled orders (Claim). |
| | `sera_approve_token` | Approve token usage for the Router contract. |

### Real Action (MCP Client)

![](/images/web3_sera_protocol-6/0.png)
*Fetching market details via `sera_get_market`. The AI formats it for human readability.*

![](/images/web3_sera_protocol-6/1.png)
*Listing available pairs with `sera_list_markets`.*

![](/images/web3_sera_protocol-6/2.png)
*Visualizing the order book via `sera_get_orderbook`. The AI even calculates the spread.*

# Implementation Highlights: The "Soul" of the Code

Simply wrapping an API isn't enough to be "legendary." To make an AI agent autonomous in a Web3 environment, I focused on these three critical points.

### 1. "Simulation" to Prevent Transaction Failure

On-chain writes cost gas. You want to avoid an AI placing a wrong order that results in a revert (failure).

Within the `placeLimitOrder` method, I execute `simulateContract` immediately before sending the transaction.

```typescript
// Excerpt from services/blockchain.ts
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
    throw new Error("ERC20InsufficientBalance: Your balance is insufficient!");
  }
}
```

This implementation effectively mitigates the risk of wasting gas.

## 2. Guardrails for AI with Zod

AI can sometimes misinterpret numbers or addresses.

To strictly block such errors on the MCP side, I introduced **Zod** schema validation.

```typescript
// Excerpt from schemas/index.ts
export const PlaceOrderInputSchema = z.object({
  market_id: AddressSchema,
  price_index: z.number().int().min(0).max(65535),
  raw_amount: z.string().regex(/^\d+$/),
  is_bid: z.boolean(),
});
```

## 3. Debugging Methods to Maximize Developer Experience

In MCP server development, the most helpful tool is the **MCP Inspector**.

This allows you to verify the behavior of tools individually on the CLI before integrating them into Claude Desktop or other clients.

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

Without this, you would spend endless time in "misaligned conversations" with the AI. It’s an essential tool for Web3 engineers.

# Security: Handing the "Wallet" to an AI

:::info
**CRITICAL**: To run this MCP server, a `PRIVATE_KEY` is required.
:::

Giving an AI access to a private key is powerful but carries risks.

- **Always use a private key for development (e.g., Sepolia testnet).**
- For mainnet operations, limit it to a "disposable wallet" with small funds. You should also implement defense mechanisms, such as hard-coding a maximum order limit per transaction on the MCP server side, to prevent the AI from accidentally draining your funds.

# Practice: Trading Through Conversation with AI

![](/images/web3_sera_protocol-6/3.png)
*Checking my order history with `sera_get_orders`. The AI identifies "claimable orders."*

![](/images/web3_sera_protocol-6/4.png)
*Balance check via `sera_get_token_balance`. The AI converts units appropriately.*

> **Me**: "Show me the order book for TWETH/TUSDC. Also, tell me my TUSDC balance."
>
> **AI**: (Executes `sera_get_orderbook` and `sera_get_token_balance`)
> "The current best price index is 20260. Your TUSDC balance is 9,998."
>
> **Me**: "Okay, place a limit bid for 1,000 TUSDC one index below the best price. Make it Post Only."
>
> **AI**: (Executes `sera_place_order` after verifying safety via simulation)

# Conclusion: A Future Where AI Agents Become "Liquidity"

Developing the MCP server for Sera Protocol revealed that **CLOB (Central Limit Order Book)** and **AI Agents** are an incredibly powerful match.

In AMMs, you have to worry about slippage. In a CLOB, an AI can move with precision by specifying an exact "price index."

In the future, the majority of on-chain FX liquidity will likely be supplied not by humans, but by AI agents armed with MCP.

Sera Protocol is evolving as the infrastructure for such **"AI-Agent Native Finance."**

That’s all for now!

Thank you!

## References
- [Sera Protocol MCP Server Source Code](https://github.com/mashharuki/SeraProtocol-Sample/tree/main/mcp-server)
- [Model Context Protocol Official Documentation](https://modelcontextprotocol.io/)
