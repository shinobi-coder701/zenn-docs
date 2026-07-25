---
title: "Prediction Markets Show Your Bet Instantly — So I Hid Mine With Zero-Knowledge Proofs"
published: true
tags: web3, cardano, privacy, zeroknowledge
canonical_url: https://zenn.dev/mashharuki/articles/midnight_simple_app-5
cover_image: https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-5/0.jpg
---

## Introduction

**Polymarket**, and on-chain prediction markets like it, kept bothering me for one reason.

{% embed https://polymarket.com/ja %}

**Who bet on what is visible in near real time.**

The moment a whale places a big bet on one outcome, everyone watching piles in behind them, and the odds move accordingly. That's not manipulation — it's just what happens with a public ledger. But it doesn't satisfy the simple wish to not reveal your prediction before everyone else does.

So: could you build a prediction market that keeps your pick hidden until voting closes?

To find out, I built `Hidden League Forecast` on **Midnight**, a privacy-focused blockchain.

It's an MVP where you just guess the winner of a fictional soccer league (the World Cup just ended, so soccer was on my mind).

> **Note**
> **What's a prediction market?**
>
> A mechanism that expresses predictions about future events as prices. Think "which team will win the World Cup match," for example.
>
> If you want to learn more about prediction markets, this resource (Japanese) is a great start:
> https://zenn.dev/barabara/books/prediction-markets-structure

The backend is written in **Compact**, Midnight's smart contract language.

> **Note**
> It combines the commit-reveal pattern with zero-knowledge proofs so that "the content of your prediction stays hidden, while only the aggregate stake becomes public."

In this article, I'll walk through the contract code, showing what stays hidden and what becomes public at each step.

> **Note**
> This app runs on testnet.

## Demo Video

{% youtube G4T-L-rVgzU %}

![Top screen: connect Lace Wallet and choose to deploy or join a market](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-5/0.jpg)
*After connecting Lace Wallet, you see your Shielded Address and balance. From here you can deploy a new market or enter an existing contract address to join one.*

## The Overall Flow

What's actually happening is simple.

```text
OPEN → REVEAL → AWAITING RESULT → RESOLVED → CLAIM
```

1. Connect Lace Wallet, then deploy a market or join an existing one
2. Pick one of 4 teams (Amber Foxes / Cedar Owls / Harbor Whales / Meadow Bears) and stake 10–500 points
3. Once the admin closes predictions, participants "reveal" their picks
4. The admin records the result
5. Participants who picked the winning team claim a pari-mutuel payout (the losing side's stakes get split among the winners)

```text
reward = floor(total_pool × your_stake / winning_team_pool)
```

> **Note**
> **Key point**
>
> At step 2, which team you bet on is never recorded anywhere on-chain. Only the stake amount and a commitment (a hash used to verify the pick later) are recorded.

Nobody — not even the admin — can see it until the reveal in step 3.

## The Smart Contract, Written in Compact

Midnight's Compact lets you declare variables (witnesses) that **"are used inside the proof but never written to the ledger."** Conversely, any value you do write to the ledger must go through `disclose()`.

That guards against the "oops, I accidentally logged a secret value" class of mistake at the type level.

The secret key, the chosen team, and the salt are all defined as witnesses.

```compact
witness local_secret_key(): Bytes<32>;
witness get_selected_team(): Team;
witness get_prediction_salt(): Bytes<32>;
witness store_prediction(team: Team, stake: Uint<64>, salt: Bytes<32>): [];
```

Here's the ledger side.

```compact
export ledger phase:                 MarketPhase;
export ledger admin_key:             Bytes<32>;
export ledger commitments:           Map<Bytes<32>, Bytes<32>>;
export ledger stakes:                Map<Bytes<32>, Uint<64>>;
export ledger participants:          Set<Bytes<32>>;
export ledger revealed:              Set<Bytes<32>>;
// ... per-team pools, etc.
```

`commitments` only holds hashes, and `stakes` only holds amounts. "Who" bet and "how much" is public, but "which team" doesn't exist anywhere yet at this point.

## Commit: Only the Hash Hits the Ledger

Here's the circuit called when you place a bet.

```compact
export circuit commit_prediction(stake: Uint<64>): [] {
  const public_stake = disclose(stake);
  assert(phase == MarketPhase.open, "Predictions are closed");
  assert(public_stake >= 10 && public_stake <= 500, "Stake must be between 10 and 500 points");

  const key = derive_participant_key(local_secret_key());
  assert(!participants.member(disclose(key)), "Participant already committed");
  const team = get_selected_team();
  const salt = get_prediction_salt();
  const commitment = make_prediction_commitment(key, team, public_stake, salt);
  store_prediction(team, public_stake, salt);

  participants.insert(disclose(key));
  commitments.insert(disclose(key), disclose(commitment));
  stakes.insert(disclose(key), public_stake);
  participant_count.increment(1);
  total_pool = (total_pool + public_stake) as Uint<64>;
}
```

`team` is never `disclose()`d here. It's only used as an input to `make_prediction_commitment()`, and only that function's return value (a hash) gets written to the ledger, via `disclose(commitment)`.

```compact
pure circuit make_prediction_commitment(
  participant_key: Bytes<32>,
  team: Team,
  stake: Uint<64>,
  salt: Bytes<32>
): Bytes<32> {
  const team_bytes = ((team as Field) as Bytes<32>);
  const stake_bytes = ((stake as Field) as Bytes<32>);
  return persistentHash<Vector<5, Bytes<32>>>([
    pad(32, "forecast:pick:v1"), participant_key, team_bytes, stake_bytes, salt
  ]);
}
```

Mixing the fixed string `"forecast:pick:v1"` into the first slot of `persistentHash` is a standard trick called domain separation. Tagging each circuit's hash inputs differently prevents an accidental collision where two different circuits produce the same hash for the same underlying values. The participant key derivation (`derive_participant_key`) uses its own tag, `"forecast:participant:v1"`.

> **Note**
> The salt isn't there because the stake only ranges from 10 to 500. `stake` is already written to `stakes` as plaintext at `commit_prediction` time, so it's public information an observer doesn't even need to guess.
>
> The real weak point is that `team` only has 4 possible values. Without a salt, an observer could take the (already public) participant key and stake, hash all 4 team candidates, and instantly find which one matches the on-chain commitment. Mixing in a random 256-bit salt makes that 4-way brute force infeasible.

On screen, you pick a team and a stake (Confidence points), then hit "Seal my forecast."

At this point, the team breakdown on the left is still frozen.

![Committing a prediction: about to press Seal my forecast](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-5/2.jpg)
*Staking 370 points on Harbor Whales. The team list on the left still just shows "SEALED" — nothing about the breakdown is public yet.*

Pressing "Seal my forecast" kicks off ZK proof generation, and you'll see a toast like this while it runs.

![Toast reading "Midnight is sealing your forecast…" while the proof is generated](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-5/5.jpg)
*The browser is generating a proof for the `commit_prediction` circuit. Behind the scenes, the witnesses (`get_selected_team` / `get_prediction_salt`) read their values out of local private state.*

## Reveal: Prove It, Then Publish It

After the deadline, participants "reveal" their prediction.

```compact
export circuit reveal_prediction(): [] {
  assert(phase == MarketPhase.reveal, "Market is not accepting reveals");
  const key = derive_participant_key(local_secret_key());
  const public_key = disclose(key);
  assert(participants.member(public_key), "Participant did not commit");
  assert(!revealed.member(public_key), "Prediction already revealed");

  const team = get_selected_team();
  const salt = get_prediction_salt();
  const stake = stakes.lookup(public_key);
  const expected = make_prediction_commitment(key, team, stake, salt);
  assert(disclose(expected == commitments.lookup(public_key)), "Prediction commitment mismatch");

  if (disclose(team == Team.amber_foxes)) { amber_foxes_pool = (amber_foxes_pool + stake) as Uint<64>; }
  // ... same for the other teams
  revealed.insert(public_key);
  revealed_count.increment(1);
}
```

All this circuit does is recompute the exact same hash from the values read back out of the witnesses, and prove it matches the hash already sitting on the ledger. Only once that matches does a comparison like `if (disclose(team == Team.amber_foxes))` finally turn the team into public information and add the stake to that team's pool.

This guarantees that "the team you're revealing really is the one you picked at commit time." Rewriting the locally stored `selectedTeam` or `salt` afterward to switch to a more favorable team gets rejected by this assert. There's actually a Vitest simulator test for exactly this case:

```ts
it("rejects a modified private prediction", () => {
  market.setPrediction("alice", Team.amber_foxes, 100n, 11);
  market.commit("alice", 100n);
  market.closePredictions();
  market.setPrediction("alice", Team.cedar_owls, 100n, 99);
  expect(() => market.reveal("alice")).toThrow();
});
```

Rewriting the local selection to `cedar_owls` after committing, then trying to reveal, gets rejected as expected. Without this check, the whole point of the privacy mechanism — preventing after-the-fact switching to whichever side looks better — would collapse. I consider this the single most important test in the suite, unglamorous as it is.

As reveals come in, the per-team breakdown that was invisible at commit time finally starts showing up on screen.

![Reveal screen after some reveals: Cedar Owls at 22%, Meadow Bears at 77%](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-5/7.jpg)
*"YOUR POSITION" on the right shows your own prediction (Cedar Owls, 100pt) as "revealed, awaiting the match result." The list on the left updates its per-team breakdown (% and points) as more reveals come in.*

## Verifying Division Without Doing Division

The pari-mutuel payout formula, `floor(total_pool × stake / winning_team_pool)`, was a genuinely annoying part to get right. I didn't want to write division directly inside a ZK circuit, so the design instead has the client compute the division result, and the circuit only verifies that the result is correct.

Before the division check, though, there's actually a "is this person even allowed to claim?" section. Here's the whole circuit, nothing omitted.

```compact
export circuit claim_reward(reward: Uint<64>): [] {
  const public_reward = disclose(reward);
  assert(phase == MarketPhase.resolved && result_set, "Market is not resolved");
  const key = derive_participant_key(local_secret_key());
  const public_key = disclose(key);
  assert(revealed.member(public_key), "Prediction was not revealed");
  assert(!claimed.member(public_key), "Reward already claimed");
  const team = get_selected_team();
  const salt = get_prediction_salt();
  const stake = stakes.lookup(public_key);
  const expected = make_prediction_commitment(key, team, stake, salt);
  assert(disclose(expected == commitments.lookup(public_key)), "Prediction commitment mismatch");
  assert(disclose(team == winning_team), "Prediction did not win");

  const winning_pool = pool_for(winning_team);
  const payout_numerator = total_pool * stake;
  assert(public_reward * winning_pool <= payout_numerator, "Reward exceeds pari-mutuel entitlement");
  assert((public_reward + 1) * winning_pool > payout_numerator, "Reward is below floor-rounded entitlement");
  assert(total_claimed_rewards + public_reward <= total_pool, "Reward conservation violated");
  rewards.insert(public_key, public_reward);
  claimed.insert(public_key);
  total_claimed_rewards = (total_claimed_rewards + public_reward) as Uint<64>;
}
```

The first five lines repeat the same pattern as `reveal_prediction` — recompute the commitment from values read back out of the witnesses, and check it against the ledger. That's what stops anyone from claiming with someone else's `stake` or `team`. On top of that, `revealed.member` checks that the prediction was actually revealed, `!claimed.member` checks it hasn't already been claimed, and `team == winning_team` checks the caller actually picked the winner. All four asserts together are what prevent double claims and stealing someone else's winnings.

> **Note**
> Even though `total_pool` and `stake` are both `Uint<64>`, a multiplication like `total_pool * stake` doesn't silently wrap around at 64 bits — Compact's type system carries the full product range (`Uint<0..(2^64-1)^2>`) through the expression. I confirmed this by compiling a small overflow test with `compact compile`. In the actual contract, `as Uint<64>` casts only appear where a value is deliberately narrowed back down.

`r = floor(n / p)` is equivalent to the inequality `r × p ≤ n < (r + 1) × p`. That's exactly what these two asserts check, using only multiplication and comparison to validate "is this the correct floor-division result." Whether the caller supplies a suspiciously large `reward` or a suspiciously small one, one of these two inequalities catches it.

The last check, `total_claimed_rewards + public_reward <= total_pool`, is a conservation rule: even summing every winner's claim, the total can never exceed the pool. Any remainder left over from floor rounding simply stays in the pool unclaimed by design — I confirmed this with a test that covers the multiple-winners case too.

Once a market resolves, participants who picked the winning team see a computed reward amount and a "Claim forecast points" button.

![Post-resolution screen: Estimated reward 440 pts, Claim forecast points button enabled](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-5/11.jpg)
*A 100pt bet on Cedar Owls paid off, for an estimated reward of 440pts. That 440 is only a number the frontend computed — what actually lands on the ledger is whatever value you pass into `claim_reward` and gets past the two asserts above.*

## Private State Only Lives in the Browser

For the commitment check to work at all, `selectedTeam` and `salt` have to survive in the browser from commit time through reveal time. Here's the frontend implementation (`pkgs/app/src/lib/prediction-market.ts`):

```ts
export const savePrediction = async (
  providers: PredictionMarketProviders,
  team: Team,
  stake: bigint,
): Promise<void> => {
  const current =
    (await providers.privateStateProvider.get(PredictionMarketPrivateStateId)) ?? initialPrivateState;
  const salt = current.salt ?? crypto.getRandomValues(new Uint8Array(32));
  const next: PredictionMarketPrivateState = { ...current, selectedTeam: team, stake, salt };
  await providers.privateStateProvider.set(PredictionMarketPrivateStateId, next);
};
```

Before calling the circuit, the chosen team and a random salt get saved to the local private state store first. The `get_selected_team` and `get_prediction_salt` witnesses just read those values back out of that local store at proof-generation time.

The flip side is that if this local store gets wiped, you're locked out for good. The README carries this warning as-is:

> **Warning**
> This app has a constraint if you want to use multiple markets at once. `PredictionMarketPrivateStateId` is a fixed key scoped per network + wallet — not per contract address. That means committing to a second market with the same wallet overwrites the `selectedTeam` / `salt` that the first market needs, and you lose the ability to reveal your first prediction.
>
> On top of that, `derive_participant_key` is derived purely from `local_secret_key()`, so the same wallet produces the same `participant_key` (and the same public `admin_key`, if you're the deployer) across every market. Within a single market, who bet on what stays hidden — but the fact that the same wallet is involved in multiple markets does not. That's an acceptable tradeoff for a single-market demo, but real multi-market use would need `privateStateId` scoped per contract address, plus market-specific data mixed into the key derivation.

> **Warning**
> Clearing your browser data, or switching devices, between committing and revealing means that prediction can never be revealed again.
>
> Neither the secret key nor the salt is backed up anywhere server-side, so this is a genuine UX gap, not an oversight.

This is deliberately "temporary privacy," not "permanent anonymity." Revealing is something you choose to do, and once you reveal, that team becomes public information as a matter of course. The design doesn't try to preserve anonymity past the point where the market ends.

This "it only exists locally" feeling is easiest to see by putting two screens side by side.

![Right after committing: only this browser remembers picking Harbor Whales](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-5/4.jpg)
*In the browser that committed, "Forecast: Harbor Whales" is right there. That's not read from the ledger — this tab is just displaying its own private state.*

![A different browser/wallet opening the same resolved market shows nothing stored](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-5/1.jpg)
*Same resolved market, but a browser profile that never predicted just shows "No personal forecast is stored in this browser profile." The ledger only has the public result (Amber Foxes won) — who picked what is known only to whoever holds that private state.*

## Actually Running It

Just staring at the code, it's hard to tell whether the commit-reveal check is really doing its job. If you're curious, the fastest way to find out is to run the simulator tests yourself.

> A devcontainer config is included — I'd recommend using it.

Prerequisites:

- Bun 1.2.x
- Compact CLI 0.30.0

```bash
bun install
bun run contract compact   # generate circuits, proving keys, and ZKIR from .compact
bun run test                # contract simulator tests
```

Example test output:

```text
✓ src/test/prediction-market.test.ts (10 tests) 1142ms

 Test Files  1 passed (1)
      Tests  10 passed (10)
```

Those 10 tests include the cases mentioned earlier:

- **"rewriting local state before revealing gets rejected"**
- **"stakes outside the allowed range, or duplicate commits, get rejected"**
- **"a team with zero winning pool can't be selected as the result"**
- **"floor division across multiple winners never pays out more than the pool"**

If you want to see it running in a browser, deploy the contract, run `bun run build` and then `bun run dev` to start the Vite dev server, and connect Lace Wallet to the Preview network — that's the quickest way to try it.

The bundled headless CLI's (`bun run cli standalone`) "Show market state" command lets you follow the same 4 phases from a terminal too.

<details><summary>Watching phase transitions from the CLI (open → reveal → awaiting_result → resolved)</summary>

![CLI Show market state: Phase: open, Participants: 2, Total pool: 560](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-5/6.jpg)
*Right after committing. 2 participants, 560 points total in the pool, but every per-team pool is still 0.*

![CLI Show market state: Phase: reveal, Revealed: 2, Team pools: cedar=100, meadow=340](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-5/8.jpg)
*Both participants have revealed. This is the first time the per-team pools (cedar=100, meadow=340) get filled in.*

![CLI Show market state: Phase: awaiting_result](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-5/9.jpg)
*The admin ran Close reveal, moving the market into the awaiting-result phase.*

![CLI Show market state: Phase: resolved, Result: cedar_owls](https://raw.githubusercontent.com/mashharuki/zenn-docs/main/images/midnight_simple_app-5/10.jpg)
*The admin ran Resolve market, recording Cedar Owls as the winner. From here, only winners can call `claim_reward`.*

</details>

## What This Design Doesn't Cover

Since this is a prototype, there are several things missing before it could become a real prediction market app — including anything that ingests outside information.

- **Trusts a single admin (steward).** Whoever deployed the market has full authority to finalize the result. There's no external oracle or dispute-resolution mechanism.
- Phase transitions only go one way — `open → reveal → awaiting_result → resolved` — **with no undo or rollback**. In particular, if reveals get closed while zero predictions have been revealed, that market becomes permanently unclaimable. That's a known area for future improvement.
- What's at stake isn't a real asset — it's **demo points specific to this app**. There's no secondary market and no permissionless market creation.

Building a real privacy-preserving prediction market on this pattern would require multisig or optimistic-oracle result finalization, explicit deadline management, proper asset custody design, and an external audit.

This project's scope stops at "actually get hands-on with commit-reveal plus zero-knowledge proofs and understand it," since that's what I set out to learn.

## Wrap-up

Following up on the anonymous rock-paper-scissors app, I built a prediction market app on Midnight too.

Midnight also just released an Agent Skill for AI coding tools, which makes development a lot smoother.

https://midskills.sevryn.xyz/

If you're looking for something to build, give Midnight a try.

Everything is open source, so if anything caught your interest, go read the code while running `bun run test`.

{% github mashharuki/midnight-prediction-market-sample-app %}

Thanks for reading!

## References

- [Midnight Network](https://midnight.network/)
- [This article's repository (contract, frontend, CLI)](https://github.com/mashharuki/midnight-prediction-market-sample-app)
