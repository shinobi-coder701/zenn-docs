---
title: "Building a Full-Stack ZK-Privacy App on Midnight: A Step-by-Step Guide"
published: true
tags: web3, cardano, privacy, typescript
canonical_url: https://zenn.dev/midnight/articles/midnight_simple_app-3
cover_image: https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-3/0.png
---

## Introduction

Hello everyone! 🚀

In this post, we are diving deep into **Midnight**, the privacy-focused blockchain!

Previously, we covered how to connect a frontend application to **Lace Wallet**. Now, we’re taking the next big step: **connecting to a smart contract!** 

Implementing a full-stack ZK (Zero-Knowledge) application can be tricky, but I’ve navigated the pitfalls and version mismatches so you don't have to. Let’s get started!

### What You Will Learn

- How to develop a full-stack application on Midnight.
- Concrete source code for calling smart contract functions via Lace Wallet.
- Real-world "gotchas" and how to solve them.

---

## The Sample App: A Full-Stack Counter

We’ll build a simple app that connects to Lace Wallet, displays balances, and interacts with a **Counter** smart contract.

### Prerequisites

- [Lace Wallet](https://www.lace.io/) browser extension (Midnight-compatible version).
- **PreProd** network selected in Lace settings.
- Some test **NIGHT** tokens from the [official faucet](https://midnight-tmnight-preprod.nethermind.dev/).
- Docker installed (for running the Proof Server).

### GitHub Repository

Check out the full source code here:
[https://github.com/mashharuki/midnight-sample-fullstack-app](https://github.com/mashharuki/midnight-sample-fullstack-app)

### Application Preview

![](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-3/0.png)

---

## Technical Features

| Category | Feature | Description |
| :--- | :--- | :--- |
| **Contract** | Build | Compiles Compact files into WASM/ZKIR/Managed Code. |
| **Contract** | Simulator | Logic verification using `CounterSimulator` without a live network. |
| **CLI** | Deploy | Deploys to Standalone/TestNet and retrieves the contract address. |
| **CLI** | Interaction | Direct CLI commands to increment and check counter values. |
| **App** | Wallet Connect | Integration with Lace Wallet extension to fetch account data. |
| **App** | Sync | Automatically joins and fetches current state from a contract address. |
| **App** | ZK Increment | One-click UI to generate ZK proofs and send transactions. |

### Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 19, Vite 5, Tailwind CSS v4, Lucide React, RxJS |
| **Contract** | Compact (Midnight's ZK DSL) |
| **SDK** | `@midnight-ntwrk/*` (SDK v2 / DApp Connector API v4) |
| **Infrastructure** | Midnight Node, Indexer, Proof Server (via Docker) |
| **Tooling** | Bun, Biome, Vitest, TypeScript |

---

## Deep Dive: Key Implementation Logic

The core logic resides in `src/lib/counter.ts` and `src/hooks/useCounter.ts`. This was the most challenging part of the build due to SDK version transitions and compatibility issues with Lace Wallet.

### `src/lib/counter.ts`

This file handles the contract instance creation, state querying, and transaction calls.

#### 1. Contract Instance Creation
We use the SDK to wrap the compiled Compact contract.

```typescript
import * as CompactJs from "@midnight-ntwrk/compact-js";

// Initialize the compiled contract instance
export const counterContractInstance: CounterContract = (CompactJs.CompiledContract.make(
  "counter",
  Counter.Contract as any,
) as any).pipe(
  CompactJs.CompiledContract.withVacantWitnesses,
);
```

#### 2. Querying State
Using `queryContractState`, we can fetch the ledger data (in this case, the `round` number of our counter).

```typescript
export const getCounterValue = async (
  providers: CounterProviders,
  contractAddress: ContractAddress,
): Promise<bigint | null> => {
  assertIsContractAddress(contractAddress);
  
  const contractState = await providers.publicDataProvider.queryContractState(
    contractAddress,
  );
  
  return contractState != null
    ? Counter.ledger(contractState.data as any).round
    : null;
};
```

#### 3. Calling Updates (Transactions)
The magic happens in `callTx`. This triggers the ZK proof generation and requests a signature from Lace Wallet.

```typescript
export const incrementCounter = async (
  counterContract: DeployedCounterContract,
): Promise<void> => {
  // Call the increment() method on the contract
  await (counterContract as any).callTx.increment();
};
```

---

## Getting Started: Run it Locally

### 1. Clone & Install
```bash
git clone https://github.com/mashharuki/midnight-lace-react-sample-app.git
cd midnight-lace-react-sample-app
bun install
```

### 2. Start the Proof Server
Midnight requires a **Proof Server** to generate ZK Proofs locally before sending transactions to the network.

```bash
cd pkgs/cli
# Start the Proof Server (Ensure it's version 8.0.3)
docker compose -f standalone.yml up -d
```

### 3. Build & Deploy the Contract
```bash
bun contract build

# Deploy to the PreProd network
bun cli preprod
```
*Note: Copy the contract address displayed in the terminal!*

### 4. Setup & Start the Frontend
```bash
# Set environment variables
cp pkgs/app/.env.local.example pkgs/app/.env

# Build and start
bun app build
bun app dev
```

Visit `localhost:5173`. You should see the following:

![](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-3/1.png)

1. Connect your wallet.
2. Enter your deployed contract address and click **Join**.
3. Click **Increment**. You will be prompted to sign the transaction.

![](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-3/3.png)

Wait a few moments for the ZK proof generation and network finalization. Once done, refresh to see the updated value!

---

## Sequence Diagrams

Unlike traditional blockchains, Midnight involves a local **ZK Proof** generation step in every state-changing transaction.

### Contract Deployment Flow

[![](https://mermaid.ink/img/pako:eNptkt9v2jAQx_8Vyw9TJ6UIktAQP1TqYJtQ12oalSZVefHsI1hN7MyxEQzxv-9MEtSW8hAud5_v_codqDASKKMt_PWgBSwULy2vC03w13DrlFAN144sYEt4G_6gMg1YcjX_sfx8yf3mVQUuoKvFff92ST1i1cA8KKlVuekcl9hSS9hhrddk7yt0h2ND17e3-GRkbvRalWQEeks-kW9eyzf1O7LzMCKhqcweJc5y4a6E8dqBXerWcVxDPxhG1JY7eJOns1-l-uU1mSsrvHJY9ztosEHzfE9-WmPW71RhUkZW_k-N-JPlug1VTD-OhA9rBtH1MOfTjtwJAY0DOUQRN1tcVOCiYUWMfKmMeMHVaad0ib2dAmh2sh475115zNq2IZ1aK8FDVygadkTupLQYpxGtwdZcSbybQ0hVULeBGgrK0JTcvhS00EfkfCNxkq9SOWMpW_OqhYhy78xqrwVlznoYoP7wBiecNA_dcZ5uNKLW-HJzToMH8mzMWVDa0E9nW8DJ7Dx8UsryE0rZge4oy7JRPEtv8kmW5DdJlqQR3VMWJ9kom6TjSZKn01k6TY4R_XfKPRmNx3E-izEynWXpOE6O_wELMw1I?type=png)](https://mermaid.live/edit#pako:eNptkt9v2jAQx_8Vyw9TJ6UIktAQP1TqYJtQ12oalSZVefHsI1hN7MyxEQzxv-9MEtSW8hAud5_v_codqDASKKMt_PWgBSwULy2vC03w13DrlFAN144sYEt4G_6gMg1YcjX_sfx8yf3mVQUuoKvFff92ST1i1cA8KKlVuekcl9hSS9hhrddk7yt0h2ND17e3-GRkbvRalWQEeks-kW9eyzf1O7LzMCKhqcweJc5y4a6E8dqBXerWcVxDPxhG1JY7eJOns1-l-uU1mSsrvHJY9ztosEHzfE9-WmPW71RhUkZW_k-N-JPlug1VTD-OhA9rBtH1MOfTjtwJAY0DOUQRN1tcVOCiYUWMfKmMeMHVaad0ib2dAmh2sh475115zNq2IZ1aK8FDVygadkTupLQYpxGtwdZcSbybQ0hVULeBGgrK0JTcvhS00EfkfCNxkq9SOWMpW_OqhYhy78xqrwVlznoYoP7wBiecNA_dcZ5uNKLW-HJzToMH8mzMWVDa0E9nW8DJ7Dx8UsryE0rZge4oy7JRPEtv8kmW5DdJlqQR3VMWJ9kom6TjSZKn01k6TY4R_XfKPRmNx3E-izEynWXpOE6O_wELMw1I)

### Increment Function Call Flow

[![](https://mermaid.ink/img/pako:eNptkl1P2zAUhv-K5atOCpULSWh8gTTBNKGNKSKrkFBuvOQ0sUjszHH4WNX_jo9dSkfxjY_sx6_f87Ghla6BcjrC3wlUBVdSNEb0pSJuDcJYWclBKEtWIxgixrDP7uAPWV1_OcZ-igoQ8_ud6Dqwx9DXYUCmxn12C6KynyjlBTK50XpNCjCPYI6ZX848UjeyVrJpw0GpAohOTy4u3CecXHayeiAlvVaVgR6ULWmA3K1j0C0nt1iD0ZLfz6SQjRJ2MhAovD9xHEpyUrT6CR8a_Sg6kuthGv77MagF4IOAN4PiUJMrYcWhibx4txDS_g4KjLBSKzK7_xEOd5XKi73cjnKKHjiUxHK4_0DVmNSTtO0hg7fvWV3qSVnX29VQezHXmHUHFYZSYbNpRHswvZC1m5cNSpTUtq6aJeUurIV5wKpuHTd5jW-1tNpQvhbdCBEVk9XFi6oot2aCN2g3cHsK_KObMJV-OCNq9NS0e8J1_l7r_k2mMWgoxMZlCsZnQvk58yzlG_pMebaYJyyLGVskWZbF2TKiL5SfptmcnSUsTrMkSTHYRvSfV2fz5XmapXG8XLAzxrLT7Suq3QUO?type=png)](https://mermaid.live/edit#pako:eNptkl1P2zAUhv-K5atOCpULSWh8gTTBNKGNKSKrkFBuvOQ0sUjszHH4WNX_jo9dSkfxjY_sx6_f87Ghla6BcjrC3wlUBVdSNEb0pSJuDcJYWclBKEtWIxgixrDP7uAPWV1_OcZ-igoQ8_ud6Dqwx9DXYUCmxn12C6KynyjlBTK50XpNCjCPYI6ZX848UjeyVrJpw0GpAohOTy4u3CecXHayeiAlvVaVgR6ULWmA3K1j0C0nt1iD0ZLfz6SQjRJ2MhAovD9xHEpyUrT6CR8a_Sg6kuthGv77MagF4IOAN4PiUJMrYcWhibx4txDS_g4KjLBSKzK7_xEOd5XKi73cjnKKHjiUxHK4_0DVmNSTtO0hg7fvWV3qSVnX29VQezHXmHUHFYZSYbNpRHswvZC1m5cNSpTUtq6aJeUurIV5wKpuHTd5jW-1tNpQvhbdCBEVk9XFi6oot2aCN2g3cHsK_KObMJV-OCNq9NS0e8J1_l7r_k2mMWgoxMZlCsZnQvk58yzlG_pMebaYJyyLGVskWZbF2TKiL5SfptmcnSUsTrMkSTHYRvSfV2fz5XmapXG8XLAzxrLT7Suq3QUO)

## Summary

Building with ZK-privacy is a paradigm shift. While there were hurdles—especially around SDK versions and wallet compatibility—overcoming them allows you to build applications that truly respect user privacy.

I even created a custom AI Agent skill to help debug the Midnight SDK logic, which made the final stretch much smoother! You can find my Claude skills in the repo if you're interested.

Happy coding, and see you in the next one where we might tackle some hackathon challenges! 🛡️✨

### References

- [Midnight Official Site](https://www.midnight.network/)
- [Midnight Documentation](https://docs.midnight.network/)
