---
title: "Mathematically Prohibiting 'Cheating' in On-Chain RPS: A Midnight × ZK dApp Case Study"
published: true
tags: web3, cardano, privacy, zero-knowledge
canonical_url: https://zenn.dev/mashharuki/articles/midnight_simple_app-4
cover_image: https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-4/0.png
---

## Introduction

Implementing Rock-Paper-Scissors (RPS) on-chain is surprisingly tricky.

The moment you choose "Rock" and send a transaction, your opponent can read your move from the public ledger. The game is over before it even starts.

I tried implementing a commit-reveal pattern manually, but managing salts, preventing front-running, and ensuring fair judging logic... it quickly became a rabbit hole.

That's when I turned to **Midnight**. I built a full-stack RPS dApp where "cheating" (looking at the opponent's move before playing) is mathematically impossible!

In this article, I'll share the ZK circuit design using Midnight's smart contract language, **Compact**, and the hurdles I faced during development.

> **Note**
> **What ZK protects**: The ZK proof ensures "confidentiality of the move during the commit phase" (fairness). After the reveal, both moves are recorded on the public ledger.

Here is what the dApp looks like:

![RPS dApp Hero](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-4/0.png)

## What You'll Learn

- Designing the "Hidden" vs. "Visible" split in Midnight.
- Mastering the commit-reveal pattern with the Compact language.
- Frontend UX strategies for handling ZK proof generation time (the 10-second hurdle).
- Robust provider configuration with the Midnight JS SDK.

## Repository

You can find the full source code here:
{% github mashharuki/midnight-rps-sample-app %}

---

## Quick Start

Here are the steps to get the app running locally.

To be honest, **it takes about 15-20 minutes** including ZK circuit compilation and the initial Docker image pull. Get your coffee ready!

### Environment

Tested with the following:

```bash
Docker version 27.4.0
compact 0.2.0
bun 1.3.13
node 23.3.0
```

### 0. Clone the Repository

```bash
git clone https://github.com/mashharuki/midnight-rps-sample-app.git
```

### 1. Install Dependencies

```bash
bun install
```

### 2. Compile and Build Contracts

```bash
# Generate ZK circuit assets (This takes the most time)
bun contract compact  

# Build CLI and Frontend
bun cli build
bun app build
```

> The `bun contract compact` step is where the Compact compiler generates the ZK proving and verification keys.

### 3. Start the Proof Server (Initial Pull: ~3 mins)

We need to run the server that handles ZK proof generation via Docker. 

Without this server, you won't be able to deploy contracts or send commit/reveal transactions.

> Version `8.0.3` is verified with Compact `0.2.0`. 
> Ensure your SDK and Proof Server versions match, or proof generation will fail.

```bash
docker run -d -p 127.0.0.1:6300:6300 midnightntwrk/proof-server:8.0.3 midnight-proof-server
```

---

## The Essence of Midnight Architecture: "Localizing" Information

Developing with Midnight requires a different mindset compared to **Solidity**. 

As mentioned in my previous articles, Midnight has **two types of states**:

- **Public State**: Visible to everyone (on-chain ledger).
- **Private State**: Visible only to you (local storage).

The **Compact** ZK circuits act as the bridge between these two.

### App Architecture

![RPS Architecture](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-4/1.png)

---

## Code Deep Dive: Mathematically Preventing Cheating

### 1. Security Core: Domain Separation

When deriving a public key from a secret key, Midnight recommends using domain separation:

```rust
pure circuit derive_pk(sk: Bytes<32>): Bytes<32> {
  // Domain separation with a fixed string "rps:pk:v1"
  return persistentHash<Vector<2, Bytes<32>>>([pad(32, "rps:pk:v1"), sk]);
}
```

If you use the secret key as-is, using the same key in another app would result in the same public key, risking data leakage. By adding a prefix like "app name + version", we ensure that the public keys derived from the same secret key are unique to each app.

### 2. The Commit-Reveal Circuits

#### Commit Phase (Declaring a move while keeping it hidden)

```rust
export circuit commit(): [] {
  assert(!game_over,                 "Game is already over");
  assert(state == GameState.waiting, "Not in waiting state");

  const sk         = local_secret_key(); // witness: private input
  const pk         = derive_pk(sk);
  const my_move    = get_my_move();
  const my_salt    = get_my_salt();
  const commitment = make_commit(my_move, my_salt);
  store_move_and_salt(my_move, my_salt); // ⭐ Save move and salt to private state

  if (!p1_joined) {
    p1_key    = disclose(pk);
    p1_commit = disclose(commitment);
    p1_joined = true;
  } else {
    assert(!p2_joined, "Both players already committed");
    p2_key    = disclose(pk);
    p2_commit = disclose(commitment);
    p2_joined = true;
    state     = GameState.committed; // Transition to 'committed' when both joined
  }
}
```

Pay close attention to **`store_move_and_salt`**. 

This is a witness function that saves the selected move and salt to the browser's IndexedDB (private state). To prove that the move revealed later is the same one committed earlier, this step is absolutely necessary.

The use of `disclose()` is also critical. It allows developers to explicitly control which results of private computations are written to the public ledger.

#### Game State Transitions

The coordination between commit and reveal phases is managed by these states:

![State Transitions](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-4/4.png)

### 3. Reveal Phase: Where ZK Proofs Shine

> If the commit is the "declaration," the reveal is the "proof."

This is where Midnight's ZK stack really pays off.

```rust
export circuit reveal(): [] {
  assert(!game_over,                   "Game is already over");
  assert(state == GameState.committed, "Not in committed state");

  const sk      = local_secret_key();
  const pk      = derive_pk(sk);
  const my_move = get_my_move();   // Restore from private state
  const my_salt = get_my_salt();   // Restore from private state
  const computed = make_commit(my_move, my_salt);

  const is_p1 = disclose(p1_key == pk);
  const is_p2 = disclose(p2_key == pk);
  assert(is_p1 || is_p2, "Caller is not a registered player");

  if (is_p1) {
    assert(!p1_revealed, "Player 1 already revealed");
    assert(disclose(computed == p1_commit), "Commitment mismatch for P1");
    p1_move     = disclose(my_move); // Move is written to ledger only now
    p1_revealed = true;
  }
  if (is_p2) {
    assert(!p2_revealed, "Player 2 already revealed");
    assert(disclose(computed == p2_commit), "Commitment mismatch for P2");
    p2_move     = disclose(my_move);
    p2_revealed = true;
  }

  if (disclose(p1_revealed && p2_revealed)) {
    result    = who_wins(p1_move, p2_move); // Judge winner
    game_over = true;
    state     = GameState.finished;
  }
}
```

The line `assert(disclose(computed == p1_commit), "Commitment mismatch for P1")` is the heart of the logic:

- `my_move` and `my_salt` exist only in your local private state.
- `make_commit(my_move, my_salt)` is re-calculated, and the ZK circuit verifies it matches the `p1_commit` recorded on-chain during the commit phase.
- You mathematically prove that "this move is the one I committed to" **without revealing the move itself until the proof is valid.**

Once the reveal is successful, `p1_move` and `p2_move` are finally written on-chain, and `who_wins()` determines the outcome.

During the commit phase, your move is hidden by ZK and remains unknown to the opponent until it is revealed. This is the mechanism that **"mathematically prohibits cheating."**

---

## Overcoming the ZK dApp UX Hurdle

The biggest challenge during implementation was handling the **"ZK proof generation time."**

![ZK Proof Loading](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-4/2.png)

### Filling the 10-Second Silence

In Midnight, before sending a transaction, you must generate a proof on your machine (or the Proof Server). This takes about 5-10 seconds.

UX improvements are essential to prevent users from thinking the app has frozen:

- **Optimistic UI Updates**: Switch the UI state to "Generating Proof..." as soon as the process starts to communicate clearly what is happening.
- **Persistent Providers**: Use `levelPrivateStateProvider` to ensure that even if the user reloads the browser during proof generation, the generated data and chosen moves are not lost.

![Waiting for Opponent](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-4/3.png)

```typescript
// Example levelPrivateStateProvider configuration
privateStateProvider: levelPrivateStateProvider({ 
  accountId, 
  namespace: "rpsPrivateState", // Separate namespace for each game
  privateStoragePasswordProvider: () => storagePassword // Secure storage
}),
```

---

## Sequence: From Commit to Game End

Let's recap the full flow:

![Game Sequence](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-4/5.png)

---

## Remaining Challenges

There's still a lot to learn by building with Midnight and Compact. Here are some issues I'm still working on:

**1. The Abandonment Problem (Griefing Attack)**

If Player 1 commits and Player 2 never joins, the contract stays locked. I need to implement a timeout/cancel mechanism in a future update.

**2. Version Management of Build Assets**

ZK circuit assets (proving keys) generated by `bun contract compact` can become invalid with even minor updates to the Compact version or compiler. 

I actually ran into this during development. If you're building a similar app, double-check your library and Proof Server versions!

Solving these two will open up even more possibilities for ZK dApps on **Midnight**.

---

## Conclusion

Implementing this "fair" RPS app taught me three key lessons:

1. **Verify Versions**: Proof generation can fail due to mismatched Proof Server versions.
2. **Don't Forget `store_move_and_salt`**: Saving private state is mandatory for the reveal phase.
3. **UX is Priority #1**: Designing a UI that handles the unique "waiting time" of ZK is critical.

Next, I'm planning to tackle multi-round support and timeout handling!

If you're interested in Midnight's privacy tech, check out the repository and my other technical blogs!

Thanks for reading!

## Follow me on X!

https://x.com/haruki_web3

---

## References

*   [Midnight Documentation](https://docs.midnight.network/)
*   [Compact Language Reference](https://docs.midnight.network/develop/reference/compact/lang-ref)
*   [Midnight RPS Sample Code (GitHub)](https://github.com/mashharuki/midnight-rps-sample-app)
