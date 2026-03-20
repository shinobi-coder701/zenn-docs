## 技術ブログ執筆要件
- Stripe社が作ったL1ブロックチェーン Tempo の概要をわかりやすくまとめたい
	- 自分の勉強のためにも非常にわかりやすくしたい
- 図やシーケンス図なども交えて視覚的にもわかりやすくまとめたい
- x402やステーブルコインとの関係性についてもわかりやすく整理したい
- 内容については入門編としつつも網羅的かつ技術的にも正確にまとめたい
- まだ日本人で記事を書いている人が少ないため覇権をとりたい
- 随所に参考文献として渡したリンクを埋め込んでもらいたいです！
- 必要に応じてSKILLの使用も積極的に検討してください。
## 技術ブログ構成案
- はじめに
- Tempoとは？
	- 概要
	- 機能一覧
	- ステーブルコインとの関係性
- 他のブロックチェーンとの違い
	- 機能面
	- 戦略面
- x402との関係性
- まとめ

## 事前調査メモ
# テンポ（Tempo）ブロックチェーン：次世代決済プラットフォームの包括的概要

## エグゼクティブ・サマリー

Tempoは、ステーブルコインによる決済、即時かつ決定論的な決済、そして予測可能な低コストの手数料を実現するために最適化された、汎用目的のブロックチェーンである。Reth SDKを基盤とし、EVM（Ethereum Virtual Machine）との完全な互換性を維持しながら、決済に特化した独自の機能をプロトコルレベルで組み込んでいる。

主な特徴は、決済専用の「ペイメント・レーン」による帯域確保、ステーブルコインで直接支払える手数料システム、32バイトの転送メモによる照合機能、そしてパスキー認証やガス代スポンサーシップを可能にする高度なトランザクション構造である。また、エコシステム内での流動性を確保するための「 enshrined DEX（プロトコル組み込み型分散型取引所）」や、柔軟なコンプライアンス管理を可能にする「TIP-403ポリシーレジストリ」を備えている。これらにより、給与支払い、国際送金、マイクロトランザクション、さらには自律型エージェント間のマシン決済に至るまで、幅広い決済ユースケースに対応する。

--------------------------------------------------------------------------------

## 1. ネットワーク・アーキテクチャとパフォーマンス

Tempoは、決済アプリケーションが要求する高スループットと高速な確定性（ファイナリティ）を提供するために設計されている。

### 技術的基盤

- **EVM互換性:** Ethereumの「Osaka」ハードフォークをターゲットとしており、Solidity、Foundry、Hardhatなどの既存ツールがそのまま利用可能である。
- **Reth SDK:** 最もパフォーマンスの高いEVM実行クライアントであるRethを基盤としている。テストネットでは20,000 TPSをベンチマークしており、メインネットではさらなる向上を目指している。
- **Simplex BFTコンセンサス:** 約0.5秒という極めて短いブロック時間を実現し、決定論的なファイナリティを提供する。これにより、支払いが即座に、かつ不可逆的に確定する。

### 決済専用レーン（Payment Lanes）

DeFi活動や複雑なスマートコントラクトによるネットワーク混雑から決済を保護するため、Tempoはプロトコルレベルで「ペイメント・レーン」を導入している。

- **専用ブロックスペース:** TIP-20トークンの転送などの決済トランザクション用に予約されたスペース。
- **予測可能性:** NFTのミントや市場の混乱による手数料の高騰に左右されず、給与支払いや顧客への払い出しが確実かつ低コスト（目標値：1件あたり0.1セント）で実行できる。

--------------------------------------------------------------------------------

## 2. TIP-20 トークン規格

TIP-20は、決済に最適化されたTempoネイティブのトークン規格であり、従来のERC-20を拡張したものである。

### 主な機能と利点

- **転送メモ:** 32バイトの参照データをトランザクションに付加できる。請求書番号や顧客IDを記録することで、バックエンドシステムとの自動照合が可能になる。
- **報酬分配機能:** トークン保有者に対して、ステーキングを必要とせずに保有量に応じた報酬を効率的に分配できる。
- **通貨宣言:** ISO 4217コード（USD、EURなど）を宣言し、DEXのルーティングや手数料支払いの資格（USDのみ）を定義する。
- **ロールベースのアクセス制御（RBAC）:** 発行（ISSUER）、一時停止（PAUSE）、制限アドレスからのバーン（BURN_BLOCKED）などの権限を個別に管理可能。

--------------------------------------------------------------------------------

## 3. Tempo Transactions（高度なトランザクション機能）

EIP-2718トランザクションタイプを採用し、他のチェーンではサードパーティ製のミドルウェアが必要な機能をネイティブにサポートしている。

|   |   |
|---|---|
|機能|内容|
|**バッチ処理**|複数の操作を1つのトランザクションで原子的に実行。大量の払い出しに最適。|
|**ガス代スポンサーシップ**|アプリケーションがユーザーの代わりに手数料を支払う。ユーザーはガス代を意識せず利用可能。|
|**手数料トークンの選択**|任意のUSD建てTIP-20トークンで手数料を支払える。プロトコルが自動で変換。|
|**スケジュール決済**|実行時間枠を指定し、将来の特定のタイミングでトランザクションを実行。|
|**パスキー認証**|WebAuthnを利用し、Face IDや指紋認証でのセキュアな署名を実現。シードフレーズ不要。|
|**並列トランザクション**|「期限付きナンス（Expiring Nonces）」により、ナンスの衝突を避けつつ同時に複数の取引を送信可能。|

--------------------------------------------------------------------------------

## 4. ステーブルコイン専用DEX（Stablecoin DEX）

Tempoには、ステーブルコイン間の取引に特化した分散型取引所がプリコンパイル契約（0xdec...）として組み込まれている。

### 特徴とメカニズム

- **中央板形式（Orderbook）:** 伝統的なAMMsとは異なり、価格・時間優先のオーダーブックを採用。
- **フリップオーダー（Flip Orders）:** 約定後に反対売買の注文を自動生成する。流動性プールのような挙動を単一の注文で実現する。
- **DEX内バランス:** ユーザーはDEX内にトークンを残すことができ、取引ごとのERC-20転送コストを削減できる。
- **クォート・トークン制:** 各トークンは特定のクォート・トークン（例：pathUSD）に対してのみペアを作成するため、流動性の断片化を防ぎ、ルートを一意に定める。

--------------------------------------------------------------------------------

## 5. コンプライアンスとガバナンス：TIP-403

規制要件を満たすため、共有型のコンプライアンス・インフラストラクチャを提供している。

- **ポリシーレジストリ:** ホワイトリストやブラックリストなどのポリシーを一度作成すれば、複数のトークンで共有可能。
- **一括アップデート:** ポリシーを更新するだけで、そのポリシーを参照しているすべてのトークンに即座にルールが適用される。各トークン契約を個別に更新する必要がない。

--------------------------------------------------------------------------------

## 6. マシン決済（Machine Payments Protocol - MPP）

StripeとTempoが共同で開発したオープン規格で、HTTPリクエストに沿った決済を可能にする。

- **HTTP 402レスポンス:** 支払いが必要なリソースに対し、サーバーが402エラーを返し、クライアントがその場で支払いを完了させるフロー。
- **セッション機能:** 「OAuthの決済版」として機能し、一度の承認でオフチェーンの署名済みバウチャーを用いた継続的なマイクロ支払いを実現。
- **ユースケース:** AIエージェントによるAPI利用、コンテンツ閲覧、従量課金サービスなど。

--------------------------------------------------------------------------------

## 7. エコシステムと開発ツール

Tempoは、開発者や企業が決済ソリューションを構築するための広範なインフラを提供している。

- **開発ツール:** Tempo CLI、SDK（TypeScript, Rust, Go, Python）、Foundry拡張。
- **ウォレット:** Tempo Wallet（パスキー対応）、BitGo（カストディ）、Privy、Safe（近日対応）。
- **ブリッジ & 取引:** LayerZero、Across、Uniswap、0xなど。
- **データ & 分析:** Chainlink（オラクル）、Allium、Artemis、Goldsky、Tenderly（デバッグ）。
- **セキュリティ:** Blockaid、Chainalysis、TRM Labsによる脅威検出とコンプライアンス監視。

### 手数料体系の比較

Tempoはステート作成（アカウント作成、新規ストレージスロットなど）に対して、攻撃を防ぐためにEthereumよりも高いガス代を設定している。

|   |   |   |
|---|---|---|
|操作|Tempo (Gas)|Ethereum (Gas)|
|新規ストレージスロット|250,000|20,000|
|アカウント作成|250,000|0|
|コントラクト作成（1バイトあたり）|1,000|200|

これにより、新規アドレスへの送金は約30万ガスのコストがかかるが、既存のアドレス間の決済は極めて低コストに抑えられる。
## 参考文献
https://docs.tempo.xyz/learn
https://docs.tempo.xyz/learn/tempo
https://docs.tempo.xyz/learn/tempo/native-stablecoins
https://docs.tempo.xyz/learn/tempo/modern-transactions
https://docs.tempo.xyz/learn/tempo/performance
https://docs.tempo.xyz/learn/tempo/fx
https://docs.tempo.xyz/learn/tempo/privacy
https://docs.tempo.xyz/learn/tempo/machine-payments
https://docs.tempo.xyz/guide/getting-funds
https://docs.tempo.xyz/quickstart/faucet
https://docs.tempo.xyz/guide/use-accounts/embed-passkeys
https://github.com/tempoxyz/examples/tree/main
https://docs.tempo.xyz/guide/payments/send-a-payment
https://docs.tempo.xyz/guide/payments/transfer-memos
https://docs.tempo.xyz/guide/payments/pay-fees-in-any-stablecoin
https://docs.tempo.xyz/guide/payments/sponsor-user-fees
https://docs.tempo.xyz/guide/payments/send-parallel-transactions
https://docs.tempo.xyz/guide/issuance/create-a-stablecoin
https://docs.tempo.xyz/guide/issuance/mint-stablecoins
https://docs.tempo.xyz/guide/issuance/use-for-fees
https://docs.tempo.xyz/guide/issuance/distribute-rewards
https://docs.tempo.xyz/guide/issuance/manage-stablecoin
https://docs.tempo.xyz/protocol/exchange/executing-swaps
https://docs.tempo.xyz/protocol/exchange/providing-liquidity
https://docs.tempo.xyz/protocol/exchange/exchange-balance
https://docs.tempo.xyz/sdk/foundry
https://docs.tempo.xyz/sdk/typescript
https://docs.tempo.xyz/quickstart/evm-compatibility#transaction-differences
https://docs.tempo.xyz/guide/tempo-transaction#configurable-fee-tokens
https://docs.tempo.xyz/quickstart/evm-compatibility#vm-layer-differences
https://docs.tempo.xyz/quickstart/predeployed-contracts
https://docs.tempo.xyz/quickstart/wallet-developers
https://docs.tempo.xyz/ecosystem/bridges
https://docs.tempo.xyz/ecosystem/data-analytics
https://docs.tempo.xyz/ecosystem/block-explorers
https://docs.tempo.xyz/ecosystem/smart-contract-libraries
https://docs.tempo.xyz/ecosystem/wallets
https://docs.tempo.xyz/ecosystem/security-compliance
https://docs.tempo.xyz/ecosystem/orchestration
https://docs.tempo.xyz/protocol/tip20/overview
https://docs.tempo.xyz/protocol/tip20/spec
https://docs.tempo.xyz/protocol/tip20-rewards/overview
https://docs.tempo.xyz/protocol/tip403/overview
https://docs.tempo.xyz/protocol/tip403/spec
https://docs.tempo.xyz/protocol/fees
https://docs.tempo.xyz/protocol/fees/spec-fee-amm
https://docs.tempo.xyz/protocol/transactions/spec-tempo-transaction
https://docs.tempo.xyz/protocol/transactions/eip-4337
https://docs.tempo.xyz/protocol/transactions/eip-7702
https://docs.tempo.xyz/protocol/transactions/AccountKeychain
https://docs.tempo.xyz/protocol/blockspace/overview
https://docs.tempo.xyz/protocol/blockspace/payment-lane-specification
https://docs.tempo.xyz/protocol/exchange/spec
https://docs.tempo.xyz/protocol/exchange
