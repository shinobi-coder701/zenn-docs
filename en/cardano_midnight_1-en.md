---
title: "[Hands-on] Midnight Deep Dive: Start Building Smart Contracts with Compact"
emoji: "🔐"
type: "tech"
topics: ["blockchain", "cardano", "typescript", "privacy", "zkp"]
published: false
publication_name: "midnight"
---

![](/images/cardano_midnight_1/0.png)

## Introduction: The "Too Transparent" Problem of Blockchains

Since the Bitcoin whitepaper was published, blockchain technology has transformed many industries, from finance to supply chains, thanks to its trustless design, transparency, and tamper resistance.

https://bitcoin.org/bitcoin.pdf

The idea that anyone can validate the same distributed ledger and form a trust network without centralized administrators was truly revolutionary.

But complete transparency can also become a major weakness.

- What if confidential enterprise data is exposed to competitors?
- What if personal transaction history is visible to the entire world?
- What if private medical records or voting behavior can be inspected by anyone?

That "too transparent" problem has been one of the biggest barriers preventing public blockchain technology from being widely adopted in enterprise and daily consumer use cases.

To solve this dilemma, a breakthrough project has emerged from the Cardano ecosystem.

That project is **Midnight**.

https://www.midnight.network/

:::message
Midnight is a Cardano sidechain focused on data protection and privacy.
:::

By leveraging cutting-edge cryptography known as Zero-Knowledge Proofs (ZKPs)[^1], Midnight enables us to prove only the facts we need, without revealing anything else.

:::message
ZKPs are often discussed in the context of privacy, but they can also reduce computational overhead depending on how they are used.

Representative examples include **ZkEVM** and **INTMAX**, both of which use ZK-based approaches for EVM-related scaling.

https://intmax.io/
:::

I recently joined the Midnight Hackathon in London and spent a lot of time exploring Compact. In this article, I share what I learned in a hands-on format: from environment setup to contract implementation, testing, and deployment.

https://midnightsummit.io/

If you want a conceptual introduction to Midnight first, check this article:

https://zenn.dev/mashharuki/articles/midnight_zkp-1

> [^1]: Zero-Knowledge Proof (ZKP) is a cryptographic method that lets you prove a statement is true without revealing any additional information (including why it is true).

## Compact: A Privacy Smart Contract Language with TypeScript-like Syntax

Another core pillar behind Midnight's innovation is its smart contract language, **Compact**.

:::message
"Isn't zero-knowledge technology only for cryptography experts?"
:::

Compact is designed to dramatically lower that barrier.

### TypeScript-based syntax

The biggest feature of Compact is that it is a **TypeScript-based domain-specific language (DSL)**.

That means a large number of web developers can build privacy-preserving applications with familiar syntax, instead of learning an entirely new language from scratch.

The Compact compiler translates your logic into the cryptographic components needed for zero-knowledge proofs, so you do not have to deal with the underlying math directly.

### Three data states: Public, Private, Witness

The core of data handling in Compact is clear separation of privacy levels.

Data is mainly handled in three states:

```mermaid
graph TD
    subgraph "User off-chain environment"
        A[🔏 private: Private state<br>e.g. user's personal counter] --> B;
    end
    subgraph "Transaction input"
        B[🤝 witness: Proof input<br>e.g. "my previous value was 5"] --> C{Circuit execution};
    end
    subgraph "Midnight blockchain (on-chain)"
         D[📢 public: Public state<br>e.g. total update count] --> C;
    end
    C --> E[New Public State];
    C --> F[New Private State];
    E --> D;
    F --> A;
```

1. **`public` (public state)**
   - Data visible on the blockchain.
   - Similar to state variables in conventional smart contracts.
   - Defined with the `ledger` keyword.

2. **`private` (private state)**
   - Confidential data managed only in a user's local (off-chain) environment.
   - The raw private data itself is not recorded on-chain.
   - Defined with the `private` keyword.

3. **`witness` (proof input)**
   - Input supplied during transaction execution to prove, "I know this data."
   - Used as evidence when updating private state.
   - Defined with the `witness` keyword.

### Basic syntax and a Counter smart contract example

Let's look at these concepts through a simple Counter contract.

This contract only increments a number, and is also introduced in official tutorials.

It includes:

- A state variable stored on the public ledger
- A method to increment that state

```typescript:counter.compact
pragma language_version >= 0.16 && <= 0.25;
import CompactStandardLibrary;

// Public state stored on the on-chain ledger
export ledger round: Counter;

// Transition function that updates public state
export circuit increment(): [] {
    round.increment(1);
}
```

- **`ledger`**:
  A publicly visible on-chain state variable.
- **`circuit`**:
  A transaction-invoked state transition function where validation and updates happen.

With Compact, you can write logic in TypeScript-like syntax while controlling data privacy in detail and proving correctness intuitively.

## Hands-on: Set up your Midnight development environment

Now let's move from theory to practice.

In this section, we build the environment needed to run `counter.compact`.

:::message
As of November 2025, frontend integration is still unstable.

So in this hands-on, the goal is to deploy a smart contract and interact with it via CLI.
:::

Required components:

1. **Compact CLI**
   Command-line tool for compiling and testing smart contracts.
2. **Lace Midnight Preview Wallet**
   Browser extension wallet for Midnight Testnet.
3. **Testnet Faucet**
   Service to get test tokens.
4. **ZK Proof Server**
   Local server for generating and verifying zero-knowledge proofs.
5. **Sample repository**
   Source code used in this tutorial.

### Step 1: Install Compact CLI

First, install the `compact` CLI compiler:

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/midnightntwrk/compact/releases/latest/download/compact-installer.sh | sh
```

Then pin a specific version (`0.25.0` in this article):

```bash
compact update 0.25.0
```

Check installation:

```bash
compact --version
# compact 0.2.0 or similar
compact compile --version
# 0.25.0
```

If `compact compile --version` returns `0.25.0`, you're good.

### Step 2: Prepare Lace Wallet and get Testnet tokens

Next, set up a wallet and receive test tokens.

1. **Install Lace Wallet**
   Add [Lace Midnight Preview](https://chromewebstore.google.com/detail/lace-midnight-preview/hgeekaiplokcnmakghbdfbgnlfheichg) from the Chrome Web Store.
2. **Create your wallet**
   Follow the setup wizard. Store your recovery phrase securely.
3. **Copy your address**
   From the wallet home screen, click "Receive" and copy your address.
4. **Request faucet funds**
   Open [Midnight Testnet Faucet](https://midnight.network/test-faucet), paste your address, and click "Request funds". After a short wait, test `tDUST` tokens should arrive.

### Step 3: Start ZK Proof Server

Private processing (including proof generation) is handled through a local Proof Server.

We'll start the official Midnight Docker image:

:::message
Docker Desktop must be installed for this step.
:::

```bash
docker run -p 6300:6300 midnightnetwork/proof-server -- 'midnight-proof-server --network testnet'
```

If logs start streaming, it launched successfully. Keep this terminal running.

You can also verify with:

```bash
curl -X GET "http://localhost:6300"
```

Expected response:

```bash
We're alive 🎉!
```

### Step 4: Prepare sample repository

Finally, set up the repository used in this article:

https://github.com/mashharuki/midnight-sample

```bash
# Clone your own fork
# (fork the repository first)
git clone https://github.com/<user-name>/midnight-sample.git
cd midnight-sample

# Install dependencies
yarn
```

:::message
Replace the `git clone` URL with your actual repository URL.
:::

Environment setup is now complete.

Next, let's implement and test the smart contract.

## Implement and test the Counter contract

With the environment ready, let's build and test.

### Code walkthrough

Put this contract in `pkgs/contract/src/counter.compact`:

```typescript:pkgs/contract/src/counter.compact
pragma language_version >= 0.16 && <= 0.25;
import CompactStandardLibrary;

// Public state stored on the on-chain ledger
export ledger round: Counter;

// Transition function that updates public state
export circuit increment(): [] {
    round.increment(1);
}
```

Then compile with `compact` CLI:

```bash
yarn contract compact
```

Under the hood:

```bash
compact compile ./src/counter.compact ./src/managed/counter
```

On success, you will see output like:

```bash
Fetching public parameters for k=10 [====================] 192.38 KiB / 192.38 KiB
  circuit "increment" (k=10, rows=29)
Overall progress [====================] 1/1
```

### Unit test implementation

Compact lets you simulate contract logic off-chain for testing.

See `pkgs/contract/src/test/counter.test.ts`:

```typescript:pkgs/contract/src/test/counter.test.ts
import { CounterSimulator } from "./counter-simulator.js";
import {
  NetworkId,
  setNetworkId
} from "@midnight-ntwrk/midnight-js-network-id";
import { describe, it, expect } from "vitest";

setNetworkId(NetworkId.Undeployed);

/**
 * Unit tests for the Counter contract
 */
describe("Counter smart contract", () => {
  it("generates initial ledger state deterministically", () => {
    const simulator0 = new CounterSimulator();
    const simulator1 = new CounterSimulator();
    expect(simulator0.getLedger()).toEqual(simulator1.getLedger());
  });

  it("properly initializes ledger state and private state", () => {
    const simulator = new CounterSimulator();
    const initialLedgerState = simulator.getLedger();
    expect(initialLedgerState.round).toEqual(0n);

    const initialPrivateState = simulator.getPrivateState();
    expect(initialPrivateState).toEqual({ privateCounter: 0 });
  });

  it("increments the counter correctly", () => {
    const simulator = new CounterSimulator();
    const nextLedgerState = simulator.increment();
    expect(nextLedgerState.round).toEqual(1n);

    const nextPrivateState = simulator.getPrivateState();
    expect(nextPrivateState).toEqual({ privateCounter: 0 });
  });
});
```

These tests verify three scenarios:

1. Contract initialization is deterministic.
2. Initial ledger value is `0`.
3. `increment` updates the counter correctly.

### Run tests

Run:

```bash
yarn contract test
```

If all tests pass, output looks like:

```bash
RUN  v4.0.8 /workspaces/midnight-sample/my-mn-app/pkgs/contract

 ✓ test/counter.test.ts (3 tests) 44ms
   ✓ Counter smart contract (3)
     ✓ generates initial ledger state deterministically 36ms
     ✓ properly initializes ledger state and private state 3ms
     ✓ increments the counter correctly 4ms

 Test Files  1 passed (1)
      Tests  3 passed (3)
   Start at  08:27:47
   Duration  421ms (transform 95ms, setup 0ms, collect 233ms, tests 44ms, environment 0ms, prepare 13ms)

JUNIT report written to /workspaces/midnight-sample/my-mn-app/pkgs/contract/reports/report.xml
Done in 1.34s.
```

Now that we know the logic works, let's create the CLI flow to deploy on Testnet.

## Deploy and execute from CLI on Testnet

After local testing, it's time to deploy.

The `pkgs/cli` package contains scripts for deployment and contract interaction.

### Generate TypeScript API

First, build the `contract` package:

```bash
yarn contract build
```

This runs commands like:

```bash
rm -rf dist && tsc --project tsconfig.build.json && cp -Rf ./src/managed ./dist/managed && cp ./src/counter.compact ./dist
```

This generates typed APIs so circuits like `increment` can be called safely from the `cli` package.

### Set environment variables

Deploying to Testnet requires the wallet seed used to sign transactions.

Create `.env` from template in `pkgs/cli`:

```bash
cp pkgs/cli/.env.example pkgs/cli/.env
```

Edit `pkgs/cli/.env`:

```:pkgs/cli/.env
NETWORK_ENV_VAR=testnet
SEED_ENV_VAR=
INITIAL_COUNTER_ENV_VAR=
CACHE_FILE_ENV_VAR=
CONTRACT_ADDRESS=
```

:::message
Handle your seed with extreme care.

Make sure this file is excluded by `.gitignore` and never pushed to GitHub.
:::

### CLI unit test walkthrough

There are also unit tests for the CLI layer.

```ts
// This file is part of midnightntwrk/example-counter.
// Copyright (C) 2025 Midnight Foundation
// SPDX-License-Identifier: Apache-2.0
// Licensed under the Apache License, Version 2.0 (the "License");
// You may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { type Resource } from '@midnight-ntwrk/wallet';
import { type Wallet } from '@midnight-ntwrk/wallet-api';
import path from 'path';
import * as api from '../api';
import { type CounterProviders } from '../utils/common-types';
import { currentDir } from '../config';
import { createLogger } from '../utils/logger-utils';
import { TestEnvironment } from './commons';
import { describe, it, expect, beforeAll, afterAll } from 'vitest';

const logDir = path.resolve(currentDir, '..', 'logs', 'tests', `${new Date().toISOString()}.log`);
const logger = await createLogger(logDir);

describe('API', () => {
  let testEnvironment: TestEnvironment;
  let wallet: Wallet & Resource;
  let providers: CounterProviders;

  beforeAll(
    async () => {
      api.setLogger(logger);
      testEnvironment = new TestEnvironment(logger);
      const testConfiguration = await testEnvironment.start();
      wallet = await testEnvironment.getWallet();
      providers = await api.configureProviders(wallet, testConfiguration.dappConfig);
    },
    1000 * 60 * 45,
  );

  afterAll(async () => {
    await testEnvironment.saveWalletCache();
    await testEnvironment.shutdown();
  });

  it('should deploy the contract and increment the counter [@slow]', async () => {
    const counterContract = await api.deploy(providers, { privateCounter: 0 });
    expect(counterContract).not.toBeNull();

    const counter = await api.displayCounterValue(providers, counterContract);
    expect(counter.counterValue).toEqual(BigInt(0));

    await new Promise((resolve) => setTimeout(resolve, 2000));

    const response = await api.increment(counterContract);
    expect(response.txHash).toMatch(/[0-9a-f]{64}/);
    expect(response.blockHeight).toBeGreaterThan(BigInt(0));

    const counterAfter = await api.displayCounterValue(providers, counterContract);
    expect(counterAfter.counterValue).toEqual(BigInt(1));
    expect(counterAfter.contractAddress).toEqual(counter.contractAddress);
  });
});
```

Run these tests on both local and testnet environments.

#### Run unit tests locally

```bash
yarn cli test-api
```

Expected:

```bash
Test Files  1 passed (1)
      Tests  1 passed (1)
   Start at  08:41:12
   Duration  200.97s (transform 180ms, setup 72ms, collect 1.11s, tests 199.62s, environment 0ms, prepare 10ms)
```

#### Run unit tests against testnet

```bash
yarn cli test-against-testnet
```

Expected:

```bash
✓ src/test/counter.api.test.ts (1 test) 151857ms
  ✓ API (1)
    ✓ should deploy the contract and increment the counter [@slow]  125059ms

Test Files  1 passed (1)
    Tests  1 passed (1)
  Start at  08:47:54
  Duration  153.65s (transform 205ms, setup 93ms, collect 1.56s, tests 151.86s, environment 0ms, prepare 8ms)
```

### Deployment script walkthrough

`pkgs/cli/scripts/deploy.ts` deploys the contract to Testnet.

It uses libraries such as `@midnight-ntwrk/midnight-sdk` and performs the following steps:

- Load wallet seed from `.env`.
- Build wallet object from the seed.
- Configure providers for Testnet connection.
- Execute deployment via `api.deploy`.

### Run deployment

Deploy with:

```bash
yarn cli deploy
```

On success, the deployed contract address appears in terminal output:

```bash
[12:16:24.603] INFO (39506): Deploying counter contract...
[12:17:27.488] INFO (39506): Deployed contract at address: 020050e6bdae4c9e65023a252a6aba74323c1d9c1ba6e520f00e84a5fc1c75b100f3
[12:17:27.488] INFO (39506): Deployment transaction: 00000000c408a293e4e287285649623774b2be950bf0d385a20117ce79a99eb7315aa547
[12:17:27.489] INFO (39506): Contract address: 020050e6bdae4c9e65023a252a6aba74323c1d9c1ba6e520f00e84a5fc1c75b100f3
Counter contract deployed at: 020050e6bdae4c9e65023a252a6aba74323c1d9c1ba6e520f00e84a5fc1c75b100f3
[12:17:27.489] INFO (39506): Not saving cache as sync cache was not defined
Done in 90.16s.
```

Set that value in `CONTRACT_ADDRESS` inside your `.env`.

### Execute `increment`

Finally, call the deployed contract's `increment` circuit.

Run:

```bash
yarn cli increment
```

This script reads `CONTRACT_ADDRESS` from `.env`, connects to the existing contract with `api.joinContract`, then calls `api.increment`.

If successful, you should see transaction info and the current counter value:

```bash
[12:33:37.176] INFO (47085): Incrementing...
[12:34:34.270] INFO (47085): Transaction 000000000202acbcd05e9f19e5144acc5f97953255840b8b932fc71b84520e715b7ca900 added in block 2485067
[12:34:34.271] INFO (47085): Increment transaction: 000000000202acbcd05e9f19e5144acc5f97953255840b8b932fc71b84520e715b7ca900 (block 2485067)
Counter incremented. txId=000000000202acbcd05e9f19e5144acc5f97953255840b8b932fc71b84520e715b7ca900 block=2485067
[12:34:34.271] INFO (47085): Checking contract ledger state...
[12:34:34.462] INFO (47085): Ledger state: 1
[12:34:34.463] INFO (47085): Current counter value: 1
[12:34:34.463] INFO (47085): Current counter value: 1
Current counter value: 1
[12:34:34.463] INFO (47085): Not saving cache as sync cache was not defined
Done in 128.20s.
```

If `Current counter value: 1` appears, your public counter was incremented successfully.

This completes the hands-on section.

## Current limitations and what's next

As of November 2025, Midnight is still in **developer Testnet** phase, and Mainnet has not launched yet.

So keep the following in mind:

- **Performance**
  Finality on Testnet can take time.
- **API changes**
  SDK/CLI behavior may change during active development. Check official docs regularly.
- **Feature scope**
  Available tooling is still limited, though development is moving quickly with community feedback.
- **Frontend integration**
  This was the area that took me the most research time during the hackathon. I also confirmed with the Midnight team onsite that stable frontend-contract integration libraries were not yet available at that time, so CLI was the practical path.

Midnight is a very ambitious project tackling one of Web3's most important challenges: privacy.

With Cardano's strong security model and community behind it, this ecosystem is definitely worth watching.

## Closing thoughts

In this article, we walked through **Midnight**, Cardano's privacy-focused sidechain, and **Compact**, its smart contract language, in a practical hands-on format.

- Midnight's approach to the blockchain "too transparent" problem.
- Compact language for intuitive private DApp development with TypeScript-like syntax.
- Data modeling with `public`, `private`, and `witness`.
- Full flow from environment setup to implementation, testing, and Testnet deployment.

I am very excited to see how this evolves.

The hackathon itself was also an amazing experience, so I will keep following upcoming updates.

Thanks for reading.

## References

- [Midnight official website](https://www.midnight.network/)
- [Midnight documentation](https://docs.midnight.network/)
- [Compact GitHub repository](https://github.com/midnightntwrk/compact)
- [Midnight Awesome DApps](https://github.com/midnightntwrk/midnight-awesome-dapps)
- [Lace Midnight Preview Wallet](https://chromewebstore.google.com/detail/lace-midnight-preview/hgeekaiplokcnmakghbdfbgnlfheichg)
- [Midnight Testnet Faucet](https://midnight.network/test-faucet)
- [Midnight Hackathon (Devpost)](https://midnight-hackathon.devpost.com/)
