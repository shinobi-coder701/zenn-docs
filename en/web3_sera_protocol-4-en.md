---
title: "Hands-on with Sera Protocol Tutorial: Mastering On-Chain Trade Execution!"
emoji: "🤑"
type: "tech"
topics: ["ethereum", "dex", "stablecoin", "clob", "defi"]
published: true
---

# Introduction

In my previous articles, I’ve covered the overview of **Sera Protocol**, how to use its GraphQL API, and how to build a basic data retrieval script.

- [Part 1: Why Sera Protocol Replaced AMM with CLOB](https://zenn.dev/mashharuki/articles/web3_sera_protocol-1-en)
- [Part 2: Hands-on with Sera Protocol's GraphQL API](https://zenn.dev/mashharuki/articles/web3_sera_protocol-2-en)
- [Part 3: Building a Script to Retrieve Data](https://zenn.dev/mashharuki/articles/web3_sera_protocol-3-en)

In this article, we’ll take it to the next level: **Executing trades by calling Sera Protocol's smart contracts!**

# Understanding Sera Protocol's Core Contracts

The Sera Protocol ecosystem is powered by four primary core contracts, each designed for a specific role in trade execution, order management, and price calculation.

### 1. Market Router
The **main entry point** for all user interactions. Instead of interacting with individual order books directly, users typically go through the Router.

*   **Limit Orders**: Provides functions like `limitBid` (Buy), `limitAsk` (Sell), and `limitOrder` (for placing multiple orders at once).
*   **Market Orders**: Executes `marketBid` or `marketAsk` for immediate fills.
*   **Claiming**: Provides the `claim` function to collect profits from filled orders, supporting claims across multiple markets simultaneously.
*   **Composite Operations**: Includes gas-saving utilities like `limitBidAfterClaim`, which allows you to place a new order immediately after claiming profits.
*   **Market Verification**: Use `isRegisteredMarket` to verify if a market is officially registered and valid.

### 2. OrderBook
Each trading pair has its own dedicated OrderBook contract responsible for **storing, matching, and settling orders**.

*   **State Queries**: Check liquidity with `getDepth`, find the best current price with `bestPriceIndex`, or verify if the book is empty with `isEmpty`.
*   **Order Details**: Use `getOrder` to fetch specific order data and `getClaimable` to check fill amounts and fee details.
*   **Simulation**: Use `getExpectedAmount` to simulate the input/output amounts expected for a market order before executing it.

### 3. PriceBook
A specialized contract that handles calculations based on Sera's unique **Arithmetic Price Model**.

*   **Price Conversion**: Provides `indexToPrice` (converts price index to actual price) and `priceToIndex` (converts actual price to the nearest index).
*   **Price Boundaries**: Provides metadata such as `maxPriceIndex`, `minPrice`, and `priceUpperBound`.

### 4. Order Canceler
A utility contract designed for **batch canceling orders** efficiently across multiple markets. Orders are identified by their NFT IDs.

*   **Batch Cancel**: Provides `cancel` (returns assets to your address) and `cancelTo` (sends assets to a specified address).
*   **Auto-Claim**: When an order is canceled, any already-filled portion is automatically claimed.

### Bonus: Order NFT
Every limit order issued on Sera is represented by an **NFT**. This allows order ownership to be transferred to other addresses or reused within other DeFi protocols as a composable asset.

# Let's Implement the Sample Code!

The code we’ll be using is available in the following GitHub repository:

[https://github.com/mashharuki/SeraProtocol-Sample](https://github.com/mashharuki/SeraProtocol-Sample)

## Features Included in This Sample

- Market Info Retrieval (via Subgraph)
- Base/Quote Token Balance Display
- Order Book Depth Retrieval (Best Bid / Best Ask)
- `limitBid` Execution with `postOnly` safety
- Order Status Polling
- Automatic `claim` (if claimable amount exists)
- `claim-only` mode (to claim independently later)

## File Structure

- `src/index.ts`: The main execution flow (Orchestration).
- `src/lib/viem.ts`: Viem client initialization, approve/place/claim/simulate logic.
- `src/utils/constants.ts`: Addresses, ABIs, RPC URLs, and Chain configurations.
- `src/utils/helpers.ts`: CLI parsing, GraphQL fetching, price index adjustments, etc.

## Setup

Clone the repository and set up your environment variables. The tutorial code is located in the `tutorial` folder.

```bash
cp .env.example .env
```

Paste your private key from **Metamask** (or your preferred wallet).

```bash
PRIVATE_KEY=0xYOUR_PRIVATE_KEY
SEPOLIA_RPC_URL=https://0xrpc.io/sep
```

Next, install the dependencies:

```bash
bun i
```

## Running the Demo

Execute the following command to start the trade lifecycle:

```bash
bun run dev
```

If everything is configured correctly, you should see output like this:

```bash
Sera Protocol - Order Lifecycle Demo (Bun + TypeScript + viem)

Wallet: 0x51908F598A5e0d8F1A3bAbFa6DF76F9704daD072
RPC: https://0xrpc.io/sep
Market: MYRC/AUDD
Latest: index=20260, price=368386000000
Balances: MYRC=10000000, AUDD=9998000
Depth: bids=2, asks=1
Top of book: bestBidIndex=20260, bestAskIndex=20262
Your open orders (before): 2
Claim target: isBid=true, priceIndex=20260, orderIndex=1, claimable=0
Claimed proceeds: 0x6d78b2c3a6a9b1669fcd2b97a763cee0a5ddb315c5ae82cb73395cfd777cf421
```

# Code Deep Dive

### 1. `lib/viem.ts`
This file contains the functions for initializing Viem clients and interacting with smart contract methods.

```ts
import {
  createPublicClient,
  createWalletClient,
  http,
  type Address,
  type Hex,
  type PrivateKeyAccount,
} from "viem";
import {
  ERC20_ABI,
  ROUTER_ABI,
  ROUTER_ADDRESS,
  RPC_URL,
  UINT16_MAX,
  UINT64_MAX,
  sepolia,
} from "../utils/constants";
import type { OpenOrder } from "../utils/helpers";

/**
 * Initializes Viem clients.
 * The Public Client is used for reading chain data, 
 * while the Wallet Client is used for sending signed transactions.
 */
export function createViemClients(account: PrivateKeyAccount) {
  const publicClient = createPublicClient({
    chain: sepolia,
    transport: http(RPC_URL),
  });

  const walletClient = createWalletClient({
    account,
    chain: sepolia,
    transport: http(RPC_URL),
  });

  return { publicClient, walletClient };
}

/**
 * Utility function to approve ERC20 tokens if needed.
 */
export async function approveTokenIfNeeded(args: {
  publicClient: ReturnType<typeof createPublicClient>;
  walletClient: ReturnType<typeof createWalletClient>;
  account: PrivateKeyAccount;
  tokenAddress: Address;
  spender: Address;
  amount: bigint;
}): Promise<Hex | null> {
  const { publicClient, walletClient, account, tokenAddress, spender, amount } = args;

  const allowance = await publicClient.readContract({
    address: tokenAddress,
    abi: ERC20_ABI,
    functionName: "allowance",
    args: [account.address, spender],
  });

  if (allowance >= amount) {
    return null;
  }

  const approvalHash = await walletClient.writeContract({
    address: tokenAddress,
    abi: ERC20_ABI,
    functionName: "approve",
    args: [spender, amount],
    account,
    chain: sepolia,
  });

  await publicClient.waitForTransactionReceipt({ hash: approvalHash });
  return approvalHash;
}

/**
 * Function to place a Limit Bid.
 */
export async function placeLimitBid(args: {
  publicClient: ReturnType<typeof createPublicClient>;
  walletClient: ReturnType<typeof createWalletClient>;
  account: PrivateKeyAccount;
  market: Address;
  priceIndex: number;
  rawAmount: bigint;
}): Promise<Hex> {
  const { publicClient, walletClient, account, market, priceIndex, rawAmount } = args;

  // Validation
  if (priceIndex < 0 || priceIndex > UINT16_MAX) {
    throw new Error(`priceIndex out of uint16 range: ${priceIndex}`);
  }
  if (rawAmount <= 0n || rawAmount > UINT64_MAX) {
    throw new Error(`rawAmount out of uint64 range: ${rawAmount.toString()}`);
  }

  const deadline = BigInt(Math.floor(Date.now() / 1000) + 3600);
  const callArgs = [
    {
      market,
      deadline,
      claimBounty: 0,
      user: account.address,
      priceIndex,
      rawAmount,
      postOnly: true, // Safety flag to ensure the order is placed on the book
      useNative: false,
      baseAmount: 0n,
    },
  ] as const;

  // Simulation check before execution
  try {
    await publicClient.simulateContract({
      address: ROUTER_ADDRESS,
      abi: ROUTER_ABI,
      functionName: "limitBid",
      args: callArgs,
      account,
      chain: sepolia,
      value: 0n,
    });
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    if (reason.includes("0xe450d38c")) {
      throw new Error("Simulation failed: ERC20InsufficientBalance.");
    }
    throw new Error(`Simulation failed: ${reason}`);
  }

  const txHash = await walletClient.writeContract({
    address: ROUTER_ADDRESS,
    abi: ROUTER_ABI,
    functionName: "limitBid",
    args: callArgs,
    account,
    chain: sepolia,
    value: 0n,
  });

  const receipt = await publicClient.waitForTransactionReceipt({ hash: txHash });
  console.log(`Order placed in block ${receipt.blockNumber}`);
  return txHash;
}
```

### 2. `index.ts`
This is the core script that orchestrates the entire flow from fetching market info to executing the order.

```ts
/**
 * Main Execution Logic:
 * 1. Fetch Market Info
 * 2. Get Order Book Depth
 * 3. Check Existing User Orders
 * 4. Place a Limit Order
 * 5. Monitor Order Status via GraphQL
 * 6. Claim Profits (if available)
 */
async function main() {
  console.log("Sera Protocol - Order Lifecycle Demo
");
  const cli = parseCliOptions(process.argv.slice(2));

  const privateKey = requirePrivateKey(PRIVATE_KEY);
  const account = privateKeyToAccount(privateKey);
  const { publicClient, walletClient } = createViemClients(account);

  // 1. Get market info
  const market = await getMarketInfo(MARKET_ADDRESS);
  console.log(`Market: ${market.baseToken.symbol}/${market.quoteToken.symbol}`);

  // 2. Get order book depth
  const depth = await getOrderBook(MARKET_ADDRESS);
  console.log(`Top of book: bestBidIndex=${depth.bids[0]?.priceIndex}, bestAskIndex=${depth.asks[0]?.priceIndex}`);

  // 3. Place a limit order
  const priceIndex = resolvePostOnlyBidPriceIndex({
    desiredPriceIndex: cli.priceIndex ?? Number(market.latestPriceIndex) - 100,
    bids: depth.bids,
    asks: depth.asks,
  });
  
  const orderTx = await placeLimitBid({
    publicClient,
    walletClient,
    account,
    market: MARKET_ADDRESS,
    priceIndex,
    rawAmount: cli.rawAmount ?? 1000n,
  });
  console.log(`Order Transaction: ${orderTx}`);

  // 4. Monitor via GraphQL
  console.log("Monitoring order status...");
  // ... (Polling logic to check status)

  // 5. Claim proceeds
  // ... (Claim logic if rawFilledAmount > 0)
}
```

# Conclusion

That’s all for this tutorial! 

By completing this hands-on guide, you’ve mastered the fundamental lifecycle of trading on **Sera Protocol**—from querying market states to executing and claiming orders via code.

This foundation is crucial for anyone looking to build automated bots, arbitrage tools, or custom interfaces for the next generation of on-chain FX.

Happy building!
