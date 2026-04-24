---
title: "Build a Simple App That Connects to Midnight Lace Wallet"
published: true
tags: web3, cardano, privacy, tutorial
canonical_url: https://zenn.dev/mashharuki/articles/midnight_simple_app-2
cover_image: https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-2/1.png
---

# Introduction

Hello everyone!

In this article, we will look at **Midnight**, a privacy-focused blockchain, and its dedicated wallet, **Lace Wallet**.

https://www.lace.io/

The official documentation explains how to deploy and run contracts, but I could not find clear guidance on connecting **Lace Wallet** to a frontend app. I ran into a few tricky points while trying it, so I created a simple beginner-friendly sample app.

I hope you enjoy it!

## What You Will Learn

- A quick overview of Lace Wallet
- How to build a simple app that connects to Lace Wallet

# What Is Lace Wallet?

**Lace Wallet** is a lightweight wallet for storing and managing Cardano-related digital assets. It was announced by **IOG**, the team behind Cardano, on June 9, 2022.

It can manage digital assets on blockchains in the Cardano ecosystem, including **Midnight**.

Even though it is lightweight, it offers rich features such as staking and asset transfers.

It is currently optimized for the Cardano ecosystem, and it appears support for other ecosystems is planned in the future.

# Build a Simple App That Connects to Lace Wallet

## Prerequisites

Before running the sample code, make sure you have the following:

- The [Lace Wallet](https://www.lace.io/) browser extension installed (a version with Midnight support)
- **PreProd** selected in Lace network settings

## Sample Code Repository

https://github.com/mashharuki/midnight-lace-react-sample-app

## App Preview

This sample app is intentionally simple: connect Lace Wallet and display balances.

![](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-2/1.png)

![](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-2/2.png)

## Feature List

| Feature | Description |
|---|---|
| Lace Wallet connection | Detects and connects to `window.midnight.mnLace` using 100ms polling |
| Version check | Confirms Connector API version is `>=1.0.0` |
| Network validation | Automatically tries PreProd / mainnet / undeployed / preview in order |
| Address display | Shows a copyable shielded address |
| Balance display | Shows Shielded / Unshielded / Dust balances in tDUST |
| Language switch | Instantly toggles Japanese ⇆ English from the top-right button (persisted via localStorage) |

## Tech Stack

| Category | Library / Tool |
|---|---|
| Framework | React 19 + TypeScript |
| Build | Vite 8 |
| Styling | Tailwind CSS v4 (`@tailwindcss/vite`) |
| UI Components | shadcn/ui (Button, Badge, Card) + Lucide React |
| Internationalization | i18next 26 + react-i18next 17 |
| Wallet Integration | `@midnight-ntwrk/dapp-connector-api` |
| Async Processing | RxJS 7 |
| Package Manager | Bun |
| Formatter | Biome |

## Key Source Code Explanations

The overall architecture is similar to many other blockchain apps.

If you understand the SDK and API specifications, you can build a working connection app quickly.

The key SDK in this project is `@midnight-ntwrk/dapp-connector-api`.

It is used to implement the wallet connection logic.

All important connection-related logic is consolidated in the file below.

A key point is around line 103.

```ts
// Attempt connection. If a network mismatch occurs, fall back to the next candidate.
walletAPI = await connector.connect(networkId);
// Lace v4: getConfiguration() is on walletAPI (not connector)
const walletRaw = walletAPI as unknown as Record<string, unknown>;
```

From `walletRaw`, you can extract wallet information such as addresses.

```ts
let address = "";
let coinPublicKey = "";
let encryptionPublicKey = "";

if (typeof walletRaw.getShieldedAddresses === "function") {
  // getShieldedAddresses() may return an array (old versions) or a single object (new versions), so handle both cases
  const result = await (
    walletRaw.getShieldedAddresses as () => Promise<Record<string, unknown>>
  )();
  // Lace v4 returns a single object (not array):
  // { shieldedAddress, shieldedCoinPublicKey, shieldedEncryptionPublicKey }
  const entry = (Array.isArray(result) ? result[0] : result) as
    | Record<string, unknown>
    | undefined;
  if (entry) {
    address = String(entry.shieldedAddress ?? entry.address ?? "");
    coinPublicKey = String(
      entry.shieldedCoinPublicKey ?? entry.coinPublicKey ?? "",
    );
    encryptionPublicKey = String(
      entry.shieldedEncryptionPublicKey ?? entry.encryptionPublicKey ?? "",
    );
  }
}
```

Balance retrieval is implemented as a dedicated React hook.

The most important part is the `fetchBalances` function.

It fetches balances from three wallet-related methods:

- `raw.getShieldedBalances`
- `raw.getUnshieldedBalances`
- `raw.getDustBalance`

```ts
import { formatBalance } from "@/lib/utils";
import type { BalanceState } from "@/utils/types";
import type { DAppConnectorWalletAPI } from "@midnight-ntwrk/dapp-connector-api";
import { useCallback, useState } from "react";

export type { BalanceState };

/**
 * Fetch shielded / unshielded / dust balances in parallel from the wallet API.
 *
 * The Lace SDK type definitions do not include these balance methods,
 * so this function casts to unknown and checks method availability dynamically.
 * Promise.allSettled allows us to receive remaining results even if one call fails.
 */
async function fetchBalances(walletAPI: DAppConnectorWalletAPI): Promise<{
  shielded: string;
  unshielded: string;
  dust: string;
}> {
  const raw = walletAPI as unknown as Record<string, unknown>;

  // Try fetching balances in parallel. If a method is unavailable, return null.
  const [shieldedResult, unshieldedResult, dustResult] =
    await Promise.allSettled([
      typeof raw.getShieldedBalances === "function"
        ? (raw.getShieldedBalances as () => Promise<unknown>)()
        : Promise.resolve(null),
      typeof raw.getUnshieldedBalances === "function"
        ? (raw.getUnshieldedBalances as () => Promise<unknown>)()
        : Promise.resolve(null),
      typeof raw.getDustBalance === "function"
        ? (raw.getDustBalance as () => Promise<unknown>)()
        : Promise.resolve(null),
    ]);

  return {
    shielded:
      shieldedResult.status === "fulfilled"
        ? formatBalance(shieldedResult.value)
        : "--",
    unshielded:
      unshieldedResult.status === "fulfilled"
        ? formatBalance(unshieldedResult.value)
        : "--",
    dust:
      dustResult.status === "fulfilled"
        ? formatBalance(dustResult.value)
        : "--",
  };
}

/**
 * Custom hook to manage loading and refreshing balances.
 *
 * @param walletAPI - Connected wallet API. If null, no action is taken.
 * @returns balanceState: current balance state / refresh: manual refresh trigger
 */
export function useBalance(walletAPI: DAppConnectorWalletAPI | null) {
  const [balanceState, setBalanceState] = useState<BalanceState>({
    status: "idle",
  });

  /**
   * Fetch balances from the wallet API and update state.
   * If walletAPI is null, do nothing.
   * Set status to "loading" while fetching, "loaded" on success with balances,
   * and "error" if anything fails.
   */
  const refresh = useCallback(async () => {
    if (!walletAPI) return;
    setBalanceState({ status: "loading" });
    try {
      const balances = await fetchBalances(walletAPI);
      setBalanceState({ status: "loaded", ...balances });
    } catch (e: unknown) {
      console.error("[useBalance] Failed to fetch balances:", e);
      setBalanceState({ status: "error" });
    }
  }, [walletAPI]);

  return { balanceState, refresh };
}
```

# How to Run the App

## Clone

```bash
git clone https://github.com/mashharuki/midnight-lace-react-sample-app.git

# Move to the frontend app directory
cd app
```

## Install

```bash
bun install
```

## Build

```bash
bun run build
```

## Start

```bash
bun run dev
```

# Conclusion

That is all for this tutorial.

Now you have a clear path to connect a **React + Vite** app with **Lace Wallet**, which is a solid step toward building a full-stack Midnight application.

In a future article, I plan to cover how to call functions on a smart contract deployed on **Midnight** and continue toward a full-stack implementation.

Thank you for reading!

## References

- [Midnight Official Website](https://www.midnight.network/)
- [Midnight Documentation](https://docs.midnight.network/)
- [What Is Lace, the New Lightweight Wallet Developed by IOG?](https://nagamaru-panda.blog/?p=828)
