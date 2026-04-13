---
title: "Building on Midnight: A Practical Guide to Privacy Smart Contracts with Compact"
published: true
tags: blockchain, cardano, privacy, tutorial
canonical_url: https://zenn.dev/mashharuki/articles/cardano_midnight_1
cover_image: https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/cardano_midnight_1/0.png
---

## Introduction: The "Too Transparent" Problem of Blockchains

Since the Bitcoin whitepaper was published, blockchain technology has transformed many industries thanks to its trustless design and transparency. However, complete transparency can also become a major weakness for enterprises and individuals alike.

[Bitcoin Whitepaper (PDF)](https://bitcoin.org/bitcoin.pdf)

That "too transparent" problem has been one of the biggest barriers preventing public blockchain adoption. To solve this, **Midnight** has emerged from the Cardano ecosystem.

https://www.midnight.network/

> **Note**
> Midnight is a Cardano sidechain focused on data protection and privacy using Zero-Knowledge Proofs (ZKPs).

I recently joined the Midnight Hackathon in London. In this article, I share a hands-on guide: from environment setup to contract implementation and deployment.

If you want a conceptual introduction to Midnight first, check this article:
[The Future of Privacy: A Deep Dive into Midnight](https://zenn.dev/mashharuki/articles/midnight_zkp-1)

## Compact: A Privacy Smart Contract Language with TypeScript-like Syntax

Compact is designed to dramatically lower the barrier to ZK development by using a **TypeScript-based domain-specific language (DSL)**.

### Three data states: Public, Private, Witness

![Data State Diagram](https://mermaid.ink/img/pako:eNptkEELwjAMhf9KyGmv_QMe9CBeB0N62Sls6-pYByP-d9Nt6mByS_LyeS-vSAsrjYILWfscG8YpG-O8D57jEqW3RjUoR7E-jO6M0p8uYg50Tf-Wq0Y_8_Yf_Zat8_96u0S_YI7v6Y_X7GfP6Zp9v_X3_gS17SBy)

*Separation of Public, Private, and Witness states in Compact*

1.  **`public` (public state)**: Data visible on the blockchain (`ledger`).
2.  **`private` (private state)**: Confidential data managed locally.
3.  **`witness` (proof input)**: Input supplied during execution to prove knowledge.

### Counter Smart Contract Example

```typescript
// counter.compact
pragma language_version >= 0.16 && <= 0.25;
import CompactStandardLibrary;

// Public state stored on the on-chain ledger
export ledger round: Counter;

// Transition function that updates public state
export circuit increment(): [] {
    round.increment(1);
}
```

## Hands-on: Set up your Midnight development environment

> **Note**
> As of November 2025, frontend integration is still unstable. This guide focuses on CLI interaction.

### Step 1: Install Compact CLI

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/midnightntwrk/compact/releases/latest/download/compact-installer.sh | sh
compact update 0.25.0
```

### Step 2: Prepare Wallet and Faucet

1.  Install [Lace Midnight Preview](https://chromewebstore.google.com/detail/lace-midnight-preview/hgeekaiplokcnmakghbdfbgnlfheichg).
2.  Get tokens from the [Midnight Testnet Faucet](https://midnight.network/test-faucet).

### Step 3: Start ZK Proof Server

> **Note**
> Docker Desktop must be installed for this step.

```bash
docker run -p 6300:6300 midnightnetwork/proof-server -- 'midnight-proof-server --network testnet'
```

## Implement and test the Counter contract

### Code walkthrough

Compile your contract in `pkgs/contract/src/counter.compact`:

```bash
yarn contract compact
```

### Unit test implementation

Compact lets you simulate contract logic off-chain using Vitest:

```typescript
// pkgs/contract/src/test/counter.test.ts
import { CounterSimulator } from "./counter-simulator.js";
import { NetworkId, setNetworkId } from "@midnight-ntwrk/midnight-js-network-id";
import { describe, it, expect } from "vitest";

setNetworkId(NetworkId.Undeployed);

describe("Counter smart contract", () => {
  it("increments the counter correctly", () => {
    const simulator = new CounterSimulator();
    const nextLedgerState = simulator.increment();
    expect(nextLedgerState.round).toEqual(1n);
  });
});
```

## Deploy and execute from CLI on Testnet

### Set environment variables

Edit `pkgs/cli/.env`:

```bash
# .env
NETWORK_ENV_VAR=testnet
SEED_ENV_VAR=your_seed_here
CONTRACT_ADDRESS=
```

> **Warning**
> Handle your seed with extreme care. Never push it to GitHub.

### Run deployment

```bash
yarn cli deploy
```

On success, you will receive a contract address. Set it in your `.env`.

### Execute `increment`

```bash
yarn cli increment
```

If successful, `Current counter value: 1` will appear in your terminal.

## Current limitations

*   **Performance**: Finality can take time on Testnet.
*   **API changes**: The SDK is under active development.
*   **Frontend**: Stable integration libraries are still being polished.

## Closing thoughts

Midnight is a very ambitious project tackling Web3's most important challenges. I highly recommend trying out the Compact language if you are interested in privacy.

Happy coding! 🔐

## References

*   [Midnight Official Website](https://www.midnight.network/)
*   [Midnight Documentation](https://docs.midnight.network/)
*   {% github midnightntwrk/compact %}
