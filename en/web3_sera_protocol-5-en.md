---
title: "Full-Throttle Sera Protocol: Building a Professional DeFi Dashboard with React"
emoji: "📈"
type: "tech"
topics: ["ethereum", "react", "tailwindcss", "web3", "defi"]
published: true
---

# Introduction

So far in this series, we’ve covered everything from the basics of **Sera Protocol** and how to use its GraphQL Subgraph to executing trades via the CLI.

https://zenn.dev/mashharuki/articles/web3_sera_protocol-1-en

https://zenn.dev/mashharuki/articles/web3_sera_protocol-2-en

https://zenn.dev/mashharuki/articles/web3_sera_protocol-3-en

https://zenn.dev/mashharuki/articles/web3_sera_protocol-4-en

But let’s be real—the true soul of DeFi is in the interaction.

While there’s a certain "hardcore" appeal to staring at a black terminal screen and typing CLI commands, most users want something more intuitive. They want to **visualize the OrderBook in real-time and place trades with a satisfying click**.

That’s why for this installment, I’ve built a **"Battle-Ready" DeFi Dashboard** using React.js that hooks directly into Sera Protocol’s core features.

In this article, I’ll share the insights and "dirty details" I gathered during the development process. Let's dive in.

# The Sample Code

You can find the full source code for this project here:

https://github.com/mashharuki/SeraProtocol-Sample

# Design Concept: Designing "Trust"

For this dashboard, I deliberately avoided the typical "AI-generated purple gradient" look common in modern DeFi.

Instead, I aimed for a **"Bloomberg Terminal" or "Nikkei Newspaper" aesthetic**—prioritizing information density, readability, and a sense of professional reliability.

![Dashboard Overview](/images/web3_sera_protocol-5/0.png)
*A dashboard layout optimized for data density and clarity.*

:::message
**Technical Stack**
- **Frontend**: React 19 + Vite
- **Styling**: Tailwind CSS v4 (Leveraging the new `@theme` features)
- **Web3**: Ethers.js + Reown (AppKit)
- **Data**: Apollo Client (Subgraph)
:::

# Key Implementation Details

Calling a smart contract is the easy part. The real challenge is ensuring users can trade safely and intuitively. Here are the three pillars I focused on.

## 1. The "Adaptive Button" Logic

The #1 reason users drop off from Web3 apps is the **"What do I do now?"** moment.

Is the wallet not connected? Is it the wrong network? Do I need to approve the token?

To eliminate this friction, I implemented a logic in `OrderForm.tsx` where **a single button automatically cycles through four different states** based on the user's status.

![Trade Page](/images/web3_sera_protocol-5/1.png)
*An order form integrated with the OrderBook. The button role changes dynamically.*

```tsx
// Excerpt from src/components/trading/OrderForm.tsx
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

By doing this, the user never has to guess what the "next step" is.

## 2. Post-Only Safety: Frontend Wisdom to Save Fees

In a Central Limit Order Book (CLOB) like Sera Protocol, the standard play is to act as a **Maker (Limit Order)** to minimize fees or earn rebates.

However, if you mistype the price and cross the current Best Ask/Bid, your order will execute immediately as a **Taker (Market Order)**.

To prevent this, I built a **"Post Only" auto-correction logic** into the frontend. If the Post Only flag is ON, the system automatically adjusts the price index to ensure it doesn't cross the spread.

![Order Placement Flow](/images/web3_sera_protocol-5/2.png)
*The order placement flow, including safety-first index correction.*

```typescript
// Excerpt from src/hooks/usePlaceOrder.ts
function resolvePostOnlyPriceIndex(params: PlaceOrderParams): number {
  if (!params.postOnly) return params.priceIndex;

  let resolved = params.priceIndex;
  const bestBid = params.bestBidIndex ? Number.parseInt(params.bestBidIndex, 10) : undefined;
  const bestAsk = params.bestAskIndex ? Number.parseInt(params.bestAskIndex, 10) : undefined;

  // Correction for Bid orders to avoid crossing into the Ask side
  if (params.isBid && Number.isInteger(bestAsk) && resolved >= (bestAsk as number)) {
    resolved = (bestAsk as number) - 1;
  }
  // ...Similar correction for Ask orders
  return resolved;
}
```

This is the "financial app" mindset: The system should cover for the user's potential mistakes.

## 3. Humanizing Errors: Translating `execution reverted`

If you display raw smart contract errors, they look like cryptic spells (e.g., `execution reverted: 0x...`). I implemented a parser to translate these into "human-readable" language.

```typescript
// Excerpt from src/hooks/usePlaceOrder.ts
function parseContractError(err: unknown): string {
  if (!(err instanceof Error)) return "Transaction failed";
  const msg = err.message;

  if (msg.includes("user rejected")) return "Cancelled by user";
  if (msg.includes("insufficient funds")) return "Insufficient ETH for gas";
  if (msg.includes("execution reverted")) {
    return "Contract error. Please check your balance or price settings.";
  }
  return msg.slice(0, 100) + "...";
}
```

![Error Handling](/images/web3_sera_protocol-5/4.png)
*Navigating the user with clear language even when things go wrong.*

This small extra effort is what separates a "demo" from a "product."

# Project Structure

I kept the architecture as clean as possible to ensure maintainability.

![My Orders Page](/images/web3_sera_protocol-5/3.png)
*Real-time updates for order status and claimable amounts.*

- `hooks/`: Encapsulates complex Web3 logic (Wallets, Tokens, Orders).
- `components/`: UI components using Tailwind v4 `@layer` and `theme` for consistency.
- `lib/`: Pure utilities like Subgraph queries and formatters.

Specifically, `useOrders.ts` polls the Subgraph for the user's order history, reflecting **"Filled"** or **"Claimable"** statuses in real-time.

# Conclusion

The Sera Protocol smart contracts provide a incredibly refined interface.

The dashboard I built this time isn't just something that "works"—it’s a pursuit of a tool that feels "right" for trading. Building a superior UI/UX layer on top of the "Trust Foundation" that is blockchain.

I believe this is the only path to Mass Adoption for Web3.

I hope this inspires you to build your own ultimate DeFi frontend!

---

**References**
- [Sera Protocol Official Docs](https://sera-protocol.gitbook.io/)
- [Sample Code (Frontend)](https://github.com/your-repo/sera-frontend)
