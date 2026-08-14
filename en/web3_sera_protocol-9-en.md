---
title: "Selective Privacy: What On-Chain FX Actually Needs (A Design Proposal for Sera Protocol)"
emoji: "🪙"
type: "idea"
topics: ["ethereum", "privacy", "zkp", "stablecoin", "erc20"]
published: true
---

# A Transparent Market Is Not Always a Fair Market

## The "Selective Privacy" On-Chain FX Needs, and a Design Proposal for Sera Protocol

On-chain FX lets you exchange and transfer currencies atomically in a single transaction using stablecoins like USDC. Unlike traditional cross-border remittance, which routes through multiple banks and leaves a time gap where only one leg of the trade has settled, on-chain FX settles both currency legs simultaneously — or not at all.

[Stripe's explanation of on-chain FX](https://stripe.com/resources/more/onchain-fx-as-a-faster-clearer-model-for-international-payments) frames this structure as the foundation for faster, clearer international settlement.

But I believe that carrying the properties of a public chain directly into enterprise FX, unmodified, creates a new set of problems.

Suppose a company hedges a large JPY/USD position at a specific time, at a specific acceptable price, moving funds to a specific wallet — and all of it is observable. That's not just a transaction record. It's information about cash flow, procurement, overseas expansion, M&A activity, payroll, and risk tolerance — information that matters enormously for competitive position.

The value of a blockchain shouldn't be that it makes everything public.

I believe the real value lies in **letting a third party verify correctness**. What on-chain FX needs isn't full anonymization — it's selective privacy that proves the soundness of a trade while minimizing the leakage of trading intent.

This is close to the selective disclosure that Verifiable Credentials (VCs) already pursue with things like SD-JWT.

> **A premise for this article**: As of this writing, Sera Protocol's public contracts and public API spec show no ZK-based mechanism for concealing orders, amounts, or balances. The privacy integration discussed in the latter half of this piece is a design proposal based on compatibility and risk considerations — not something Sera Protocol's team has announced or endorsed.

## FX Has More Than One Thing Worth Protecting

Treating privacy as merely "hiding the address" isn't enough. On-chain FX needs to design across at least three distinct layers.

| Layer | What it protects | Impact if leaked | Property to aim for |
| --- | --- | --- | --- |
| Order layer | Currency pair, size, acceptable price, execution time, counterparty | Front-running, copy trading, inferring hedging intent | Disclose only to the parties needed for execution |
| Settlement layer | Balances, senders/receivers, chains of fund movement | Inferring trading relationships, financial position, beneficiaries | Settlement validity is verifiable; relationships stay minimally exposed |
| Oversight layer | KYC, sanctions, AML/CFT, audit records | Missed illicit activity, or excessive personal data exposure | Prove eligibility, disclose only to authorized parties when needed |

The first is order information. If the currency pair, size, minimum receive amount, and execution timing of a large order are visible, others can front-run it. In thin markets, that leakage translates directly into worse execution prices.

The second is settlement information. Continuously observing sender/receiver addresses and amounts lets outsiders infer a company's trading relationships and estimate its balances. A public ledger makes auditing easy, but in a commercial context it starts to resemble "a financial database anyone can browse."

The third is oversight information. Privacy here isn't the opposite of oversight — it's a different mechanism for it. Legitimate participants should be able to prove facts like "not a sanctioned entity," "identity verification complete," or "within the defined trading limit," without disclosing unnecessary personal data or trade history. The FATF applies AML/CFT requirements to virtual assets and VASPs, and positions travel-rule implementation as an international priority. [FATF's targeted update](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/targeted-update-virtual-assets-vasps-2024.html)

FX trade surveillance combines private trading data with market data to detect anomalous behavior and market misconduct. [LSEG's trade surveillance for FX](https://www.lseg.com/en/fx/reporting-compliance-clearing/trade-surveillance-for-fx) What's needed isn't "everyone reads the full history" — it's that a properly authorized party can verify what it needs to, within its authority.

## What zERC20 Actually Solves

zERC20 is a standard developed by the **INTMAX** team. It tries to sever the link between sender and receiver while keeping an operating experience close to a normal ERC-20 transfer.

https://zerc20.io/

The recipient generates a burn address derived from a secret value — one nobody holds the private key to — and the sender transfers tokens there. The recipient later proves in zero-knowledge that they know the secret, and receives an equivalent amount of tokens.

In the public implementation, transfer state is committed to a SHA-256 hash chain, and state transitions built off-chain are verified with either a Nova IVC or a Groth16 proof. The design distinguishes between a single lightweight withdrawal and a withdrawal that aggregates multiple transfers, and it also supports cross-chain transfers via **LayerZero V2**.

That said, there are two caveats worth flagging.

1. The EIP that zERC20 references, [EIP-7503](https://eips.ethereum.org/EIPS/eip-7503), is not an adopted standard — it currently sits at **Stagnant**. A similar token-wrapper spec, [ERC-8065](https://eips.ethereum.org/EIPS/eip-8065), is still at **Draft**.
2. zERC20's public implementation includes a `Blocklist` that blocks sanctioned addresses — but that's a sender/receiver-address blocking mechanism. It's not a "proof of innocence" that uses ZK to prove the soundness of a fund's provenance, nor does it independently satisfy travel-rule information-sharing requirements on its own.

This distinction matters: a technology that weakens the linkage of fund flows is not the same thing as a technology that cryptographically satisfies the regulatory requirement to explain eligibility and provenance.

## What Sera Protocol's Smart Contract Design Tells Us

Sera's smart contracts combine off-chain signatures with on-chain settlement in an order-book / smart-order-router design. [Sera Orderbook Contract v2](https://github.com/sera-cx/orderbook-contract-v2)

- `SeraSOR.executeIntent()` verifies an EIP-712-signed Intent — containing the input/output tokens, maximum input amount, minimum output amount, recipient, and deadline — and atomically executes a route across multiple legs.
- `Vault.sol` manages per-address token balances as a ledger, and rejects Vault operations involving blacklisted addresses.
- Sera MCP handles quotes and EIP-712 Intents, and can enforce policies such as allowed tokens, recipients, trade limits, and slippage. [Sera for Agents documentation](https://agents.sera.cx/docs/)

This architecture is well suited to institutional controls and atomic FX settlement. But the input/output assets, upper/lower bounds, and recipient contained in an Intent are all information required for public execution — even connecting zERC20 wouldn't conceal the intent of the order itself.

## Three Realistic Stages for Integrating Privacy into Sera

### Stage 1: Improve Recipient Privacy

The first integration candidate is whitelisting zERC20-compatible tokens on Sera and designating a one-time burn address as the final recipient.

Because Sera's SOR can bind the final leg's recipient within the Intent, that recipient can be swapped for an address the recipient themselves generated.

What this stage protects is mainly **the direct link between a public address and the ultimate beneficiary**. What it does *not* protect is **the order's currency pair, size, price condition, or execution time**. So this shouldn't be labeled "private FX" in general — it should be positioned specifically as a **private receiving rail**.

### Stage 2: Introduce ZK Eligibility Proofs into the Policy Layer

Next, incorporate ZK credential proofs into Sera's policy layer. The prerequisite: users can prove they're KYC-verified, not sanctioned, authorized to trade on behalf of their entity, and within trading limits — without disclosing the underlying credentials themselves.

What gets verified on-chain, for example, could be a minimal set of public inputs like this:

```text
policyRoot        : commitment to the set of valid credentials
credentialProof   : ZK proof of membership in that set, and non-revocation
nullifier         : a value preventing improper reuse of the same credential
complianceFlags   : bits indicating only that the required eligibility is met
```

The important thing here is not to assume that replacing blocklist matching with a ZK proof is a done deal. You still need to operationally design for sanctions-list update frequency, the freshness of the set used in the proof, remediation for false positives, revocation and reissuance, and audit-time disclosure procedures.

### Stage 3: Protect Order Intent

The highest-value and hardest problem is **protecting order information itself**. One approach: distribute encrypted quote/order details as an off-chain RFQ to eligible market makers only, and leave on-chain only a commitment or proof that the execution constraints were satisfied.

This approach requires designing several things simultaneously:

- How to evaluate and audit best execution
- How much information to disclose to market makers
- How to handle RFQ expiry, re-quoting, and partial fills
- Whether proof-generation time exceeds the price's validity window
- Whether concealing order flow weakens market-misconduct detection

"Just encrypting the order" isn't sufficient. Post-trade correlation of amount, timing, gas usage, and recipient address can still allow re-identification, so operational countermeasures — batching, temporal separation, amount splitting, relayer use — are also necessary.

## Privacy Is Not the Same as Unauditability

What Sera needs isn't a universal master key. It's a design where trading counterparties, regulated intermediaries, and independent auditors can each obtain only the minimum information necessary, under different levels of authority.

| Party | What they should generally see | What they generally should not see |
| --- | --- | --- |
| General public | Settlement finality, verifiable proofs, system health | Trading intent, real identities, trading relationships, full balances |
| Market makers | Order information needed to quote | Unnecessary personal information, other firms' order history |
| Compliance officers | Eligibility, alerts, required audit trail | The full content and attributes of every routine transaction |
| Auditors / law enforcement | Information necessary under legal basis and process | Bulk access beyond the stated purpose |

In Japan, fiat-pegged stablecoins are institutionalized as electronic payment instruments under the Payment Services Act, and operators handling them are subject to a framework covering information provision and business management. [FSA materials](https://www.fsa.go.jp/singi/singi_kinyu/soukai/siryou/20260203/2-2.pdf) FX itself, meanwhile, is a financial instrument carrying both loss risk and operator regulation. [Financial Futures Association of Japan's investor advisory](https://www.ffaj.or.jp/investors/fx/)

That's exactly why technical concealment must never be treated as "a feature for evading regulation." The goal is to preserve necessary oversight capability while reducing excessive information disclosure to unrelated third parties.

## Conclusion: Preserve Verifiability, Protect Trading Intent

The future of on-chain FX isn't a binary choice between full visibility and full anonymity.

The market Sera should aim for is one where trading intent is protected, settlement is verifiable, and legal compliance can be demonstrated in zero-knowledge. Technology like zERC20 is a strong candidate for improving that settlement layer. But without designing order-information protection, eligibility proofs, and selective disclosure for audits as distinct problems, on-chain FX won't reach a bar that institutions can actually rely on.

Privacy is not the opposite of transparency. It's a design principle for delivering the right transparency, to the right party, to the extent actually needed.

---

## References

- [Sera Protocol / orderbook-contract-v2](https://github.com/sera-cx/orderbook-contract-v2)
- [Sera for Agents docs](https://agents.sera.cx/docs/)
- [Sera MCP](https://github.com/sera-cx/sera-mcp)
- [zERC20](https://zerc20.io/)
- [zERC20 GitHub repository](https://github.com/kbizikav/zERC20)
- [EIP-7503: Zero-Knowledge Wormholes](https://eips.ethereum.org/EIPS/eip-7503)
- [ERC-8065: Zero Knowledge Token Wrapper](https://eips.ethereum.org/EIPS/eip-8065)
- [FATF: Virtual Assets Targeted Update](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/targeted-update-virtual-assets-vasps-2024.html)
- [Japan FSA: Working Group Materials on the Crypto-Asset System](https://www.fsa.go.jp/singi/singi_kinyu/soukai/siryou/20260203/2-2.pdf)
- [LSEG: Trade Surveillance for FX](https://www.lseg.com/en/fx/reporting-compliance-clearing/trade-surveillance-for-fx)
