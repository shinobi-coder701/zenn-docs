---
title: "UniswapV4に対応したオリジナルHookを作ってみよう！"
emoji: "🦄"
type: "tech"
topics: ["Web3","blockchain","DEX","solidity","Ethereum"]
published: false
---

# はじめに

先日 **ETH Global**が主催する**HackMoney2026**に参加する機会があり**UniswapV4**を使ったHookを開発する機会がありました。

https://ethglobal.com/events/hackmoney2026

調べる中で色々と分かったことがあるので学びをシェアするために記事を書きました。

ぜひ最後まで読んでいってください！

# Uniswapとは

**Uniswap** は、Ethereum ブロックチェーン上に構築された **分散型取引所（DEX）** です。2018年に **Hayden Adams** 氏によって開発され、現在では DeFi（分散型金融）エコシステムの中核を担う存在となっています！

https://app.uniswap.org/

数あるWeb3プロダクトの中でも最も成功したものの一つとして君臨し続けています。

Uniswap の最大の特徴は、**AMM（Automated Market Maker / 自動マーケットメーカー）** という仕組みを採用している点です。

従来の取引所のように「買い手」と「売り手」が直接マッチングするオーダーブック方式ではなく、**流動性プール** と呼ばれるスマートコントラクトにトークンを預けることで、誰でもトークンの交換（スワップ）が可能になります。

## Uniswapの歴史

Uniswap は以下のように進化を遂げてきました。

| バージョン | リリース年 | 主な特徴 |
|-----------|-----------|---------|
| **V1** | 2018年 | ETH⇔ERC-20トークンのペアのみ。AMM の基本概念を実証 |
| **V2** | 2020年 | ERC-20⇔ERC-20 の直接ペアに対応。フラッシュスワップ導入 |
| **V3** | 2021年 | **集中流動性（Concentrated Liquidity）** を導入。資本効率が飛躍的に向上 |
| **V4** | 2025年 | **Hooks**、**シングルトン設計**、**Flash Accounting** 等で柔軟性とガス効率を大幅改善 |

## AMMの仕組み

Uniswap の AMM は **定積公式（Constant Product Formula）** に基づいています。

$$x \times y = k$$

- $x$ = プール内のトークンAの量
- $y$ = プール内のトークンBの量  
- $k$ = 定数（流動性追加/削除時以外は変わらない）

例えば、プールに 10 ETH と 30,000 USDC がある場合、$k = 10 \times 30{,}000 = 300{,}000$ です。

ユーザーが 1 ETH を投入すると、プールは $k$ が一定になるように USDC を払い出します。

$$11 \times y = 300{,}000 \quad \Rightarrow \quad y \approx 27{,}273$$

つまり、約 2,727 USDC を受け取れる計算です（実際には手数料も発生します）。

## 流動性プロバイダー（LP）

Uniswap では、誰でも **流動性プロバイダー（LP）** としてトークンペアをプールに預けることができます。LP は取引手数料の一部を報酬として受け取ります。

:::message
**初心者向けポイント**: 

流動性を提供するとスワップ手数料が得られますが、**インパーマネントロス（変動損失）** というリスクもあります。これは預けたトークンの価格比率が変動した場合に発生する一時的な損失です。
:::

# DEXとは

## DEX（分散型取引所）の基本

**DEX（Decentralized Exchange）** とは、中央管理者を持たない、ブロックチェーン上のスマートコントラクトによって運営される取引所です。

## CEX vs DEX の比較

| 観点 | CEX（中央集権型取引所） | DEX（分散型取引所） |
|------|----------------------|-------------------|
| **管理者** | 企業が運営 | スマートコントラクトが自動運営 |
| **資産の管理** | 取引所が保管（カストディアル） | ユーザー自身が管理（ノンカストディアル） |
| **KYC/本人確認** | 必須 | 不要（ウォレット接続のみ） |
| **取引速度** | 高速 | ブロックチェーンの速度に依存 |
| **上場プロセス** | 取引所の審査が必要 | **パーミッションレス**（誰でもプール作成可能） |
| **透明性** | 内部ロジックは非公開 | コードがオープンソース |
| **リスク** | ハッキング、取引所の破綻 | スマートコントラクトの脆弱性 |
| **代表例** | Binance, Coinbase | Uniswap, SushiSwap, Curve |

## DEXの主な種類

### 1. AMM型（自動マーケットメーカー）

流動性プールとアルゴリズムで価格を決定する方式です。Uniswap、Curve、Balancer がこのタイプに該当します。

### 2. オーダーブック型

従来の取引所と同様に買い注文と売り注文をマッチングさせる方式です。dYdX などがこのタイプです。

### 3. アグリゲーター型

複数の DEX から最も有利なレートを探して取引をルーティングします。1inch や Paraswap、LI.FIが該当します。

https://1inch.com/ja

https://li.fi/

# UniswapV4でできるようになったこと

Uniswap V4 は 2025年にリリースされた最新バージョンです。V3 の集中流動性を継承しつつ、**Hooks** による拡張性と **ガス最適化** を実現した大型アップグレードです。

https://docs.uniswap.org/contracts/v4/overview

V4の主要な新機能を以下の6つのカテゴリーで解説します。

## 1. Hooks（フック） — 最大の目玉機能

**Hooks** は、Uniswap V4 で導入された最も革新的な機能です。これは流動性プールにカスタムロジックを追加できる**外部スマートコントラクト**のことです。

https://docs.uniswap.org/contracts/v4/concepts/hooks

### Hooksの仕組み

- 各プールには **1つのHookコントラクト** をアタッチ可能（オプション）
- 1つのHookコントラクトは **複数のプール** に紐付け可能
- プール作成時（`PoolManager.initialize`）にHookのアドレスを指定

### Hook関数の種類

Hooks はスワップや流動性操作の **前後** にカスタムロジックを差し込めます。  
すべてを実装する必要はなく、必要なものだけを選んで使えます。

```bash
┌───────────────────────────────────────────────────────────────┐
│                   Hook Functions                              │
├───────────────────────────────────────────────────────────────┤
│ プール初期化     │ beforeInitialize / afterInitialize           │
├───────────────────────────────────────────────────────────────┤
│ 流動性追加       │ beforeAddLiquidity / afterAddLiquidity       │
├───────────────────────────────────────────────────────────────┤
│ 流動性削除       │ beforeRemoveLiquidity / afterRemoveLiquidity │
├───────────────────────────────────────────────────────────────┤
│ スワップ         │ beforeSwap / afterSwap                      │
├───────────────────────────────────────────────────────────────┤
│ 寄付（Donate）   │ beforeDonate / afterDonate                  │
└───────────────────────────────────────────────────────────────┘
```

### Hooksで実現できるユースケース

Hooks の導入により、Uniswap V4 上で以下のような高度なDeFiプロトコルを構築できるようになりました。

- **指値注文（Limit Orders）**: 特定の価格に達したら自動的にスワップを実行
- **カスタムオラクル**: プール独自のオラクルを実装
- **カスタムAMM曲線**: $x \times y = k$ 以外の価格曲線を実装可能
- **動的手数料**: 市場状況に応じて手数料を自動調整
- **自動流動性管理**: 条件に応じて流動性を自動リバランス
- **イールドファーミング**: 流動性提供に追加のインセンティブを付与
- **レンディング連携**: Uniswap V4 のプールと融合したレンディングプロトコル

:::message
**開発者へのインパクト**: 

Hooks を使えば、まったく新しいDeFiプロトコルのコードベースをゼロから作る必要がなくなります。Uniswap V4 の堅牢なインフラ上にカスタムロジックを載せることで、**開発スピードの向上**と**監査コストの削減**が期待できます。
:::

## 2. シングルトン設計（Singleton Design）

### V3の課題

V3 では、プールごとに **個別のスマートコントラクト** がデプロイされていました（Factory パターン）。

これには以下の問題がありました。

- プール作成時のガスコストが高い（コントラクトデプロイが必要）
- マルチホップスワップ時にプール間でトークンを都度転送する必要がある

### V4の解決策

V4 では、すべてのプールの状態とロジックを **1つの `PoolManager` コントラクト** に集約しました。

```
V3: Factory → Pool A コントラクト
             → Pool B コントラクト
             → Pool C コントラクト  (それぞれ独立)

V4: PoolManager (シングルトン)
    ├── Pool A の状態
    ├── Pool B の状態
    └── Pool C の状態  (1つのコントラクトで管理)
```

**メリット**:

- **プール作成コストの大幅削減**: コントラクトデプロイが不要。状態の更新のみで済む
- **マルチホップスワップの効率化**: 同一コントラクト内なので中間トークンの実転送が不要
- **よりシンプルなアーキテクチャ**: 開発者にとってインテグレーションが容易

## 3. Flash Accounting（フラッシュアカウンティング）

**Flash Accounting** は、シングルトン設計と **EIP-1153（Transient Storage）** を活用した革新的な最適化機能です。

https://docs.uniswap.org/contracts/v4/concepts/flash-accounting

### V3 の問題

V3 では、マルチホップスワップで中間ステップごとにトークンの実際の転送（`transfer()`）が発生していました。

```
V3: ETH→USDC スワップ → USDC transfer() → USDC→DAI スワップ → DAI transfer()
    （中間のトークン転送が毎回発生）
```

### V4 の仕組み

V4 では、一連の操作中は **内部的な残高（delta）の記録のみ** を行い、**最後にまとめて精算** します。

```
V4: unlock() → swap(ETH→USDC) → swap(USDC→DAI) → settle(ETH支払い) + take(DAI受取り)
    （中間のUSDC転送は不要！入力と出力の2回だけ）
```

### ロッキングメカニズム

Flash Accounting は以下の3ステップで動作します。

1. **`unlock()`** で PoolManager のロックを解除
2. **`unlockCallback`** 内でスワップや流動性操作を実行（この間はdeltaのみ記録）
3. コールバック終了時にすべての **delta が0 に精算** されていることを確認

:::message alert
**重要**: `unlockCallback` から制御が PoolManager に戻る際、すべての残高変更（delta）が解決されている必要があります。未決済の残高が残っているとトランザクションは失敗します。
:::

### ガス削減の効果

この最適化は **ホップ数が増えるほど効果が大きく** なります。  
何ホップのスワップでも、実際のトークン転送は **入力トークンと出力トークンの2回だけ** です。

## 4. ネイティブETHサポート

V3 では ETH を使ったスワップを行うには、まず ETH を **WETH（Wrapped ETH）** に変換する必要がありました。これには以下のデメリットがありました。

- ラッピング/アンラッピングのガスコスト
- ユーザー体験の複雑化

V4 では **ネイティブの ETH** をそのままプールペアで使用できるようになりました。これにより、WETH への変換ステップが不要になり、ガスコスト削減とUXの向上が実現しています。

## 5. ERC-6909 トークン規格

Uniswap V4 は **ERC-6909** という新しいトークン規格を採用しています。これは ERC-1155 の軽量版ともいえる規格で、1つのコントラクトから複数のERC-20トークンを効率的に管理できます。

https://eips.ethereum.org/EIPS/eip-6909

### ERC-6909 の利点

| 比較項目 | ERC-1155 | ERC-6909 |
|---------|----------|----------|
| インターフェース | 複雑 | **シンプル** |
| 転送委任 | 非効率 | **効率的** |
| ガスコスト | 高め | **低い** |
| コントラクトサイズ | 大きい | **小さい** |

### 仕組み

トークンを PoolManager に預けたままにし、代わりに **ERC-6909 のクレームトークン** を受け取ることができます。次回の操作時にはこのクレームトークンを使用できるので、ERC-20 の外部コントラクト呼び出しが不要になります。

**活用例**:
- **高頻度トレーダー / MEV ボット**: 短時間に多数のスワップを行うパワーユーザーに最適
- **流動性マネージャー**: 頻繁にポジションを開閉するユーザーに有利

## 6. ダイナミックフィー（Dynamic Fees）

V3 では手数料は固定のティア（0.05%、0.30%、1.0%）から選択する方式でした。V4 では **Hooks を使って手数料を動的に変更** できるようになりました。

https://docs.uniswap.org/contracts/v4/concepts/dynamic-fees

### 主なユースケース

1. **ボラティリティベース**: 価格変動が激しい時は手数料を上げてLPを保護
2. **ボリュームベース**: 取引量が多い時は手数料を下げてトレーダーを誘引
3. **時間ベース**: 時間帯や曜日に応じた手数料設定
4. **ガス価格連動**: ネットワーク混雑時に手数料を調整
5. **クロスプールアービトラージ緩和**: 有害なアービトラージを抑制
6. **価格オラクル連動**: 外部オラクル価格との乖離に応じて調整

### 更新方法

ダイナミックフィーは以下の2つの方法で更新できます。

1. **`PoolManager.updateDynamicLPFee()`** を定期的に呼び出す
2. **`beforeSwap` Hook** でスワップごとに手数料を返す

## V3 vs V4 まとめ

最後に、V3 と V4 の違いを一覧表でまとめます。

| 機能 | V3 | V4 |
|------|----|----|
| **集中流動性** | ✅ | ✅（継承） |
| **アーキテクチャ** | Factory + 個別Pool | **シングルトン（PoolManager）** |
| **カスタムロジック** | ❌ | ✅ **Hooks** |
| **中間トークン転送** | 毎ホップで必要 | **Flash Accounting で不要** |
| **ネイティブETH** | ❌（WETH必須） | ✅ |
| **手数料** | 固定ティア | **ダイナミックフィー対応** |
| **トークン規格** | — | **ERC-6909** |
| **プール作成コスト** | 高い（コントラクトデプロイ） | **低い（状態更新のみ）** |
| **ステーキング** | NFT転送が必要 | **Subscribers で転送不要** |

# UniswapV4に対応したオリジナルHookを作ってみよう！

それでは早速オリジナルHookを作ってみましょう！

以下の学習コンテンツがとても参考になりました！

https://updraft.cyfrin.io/courses/uniswap-v4

## サンプルコード

https://github.com/mashharuki/defi-uniswap-v4

## 動かし方

### Devcontainerを立ち上げる

まずはDevcontainerを起動させましょう！  
これで必要なツール群がインストールされた環境が用意できます！

### インストール

git submoduleを使っているのでリポジトリをクローンしてきたら以下のコマンドを実行します。

```bash
git submodule update --init --recursive
```

以降のコマンドは`foundry`フォルダ配下で実行します。

### ビルド

```bash
forge build
```

### 事前準備

- Alchemy等のRPCプロバイダーでEthereumメインネット用のAPIキーを発行すること

    https://www.alchemy.com/

- 上記値を環境変数にセットする。

    ```bash
    FORK_URL=
    ```

    そして環境変数有効化させます

    ```bash
    source .env
    ```

- 次に以下のコマンドで最新ブロック高を取得する

    ```bash
    FORK_BLOCK_NUM=$(cast block-number --rpc-url $FORK_URL)
    echo $FORK_BLOCK_NUM
    ```

- 次に以下のコマンドでSaltを発行する

    ```bash
    forge test --match-path test/FindHookSalt.test.sol -vvv
    ```

    ここで得られたSALTを環境変数にセットする

    ```bash
    SALT=
    ```

    そして再度有効化させます。

    ```bash
    source .env
    ```

    これで準備OKです！

### テスト

それではテストしてみましょう！

```bash
forge test
```

以下のように1機能ずつテストしていく

#### CounterHook

```bash
forge test --fork-url $FORK_URL --fork-block-number $FORK_BLOCK_NUM --match-path test/CounterHook.test.sol -vvv
# 回答の方を実行する場合は FOUNDRY_PROFILE=solutionをつける
FOUNDRY_PROFILE=solution forge test --fork-url $FORK_URL --fork-block-number $FORK_BLOCK_NUM --match-path test/CounterHook.test.sol -vvv
```

テスト実行結果例

```bash
Suite result: ok. 3 passed; 0 failed; 0 skipped; finished in 44.85s (42.33s CPU time)

Ran 1 test suite in 50.55s (44.85s CPU time): 3 tests passed, 0 failed, 0 skipped (3 total tests)
```

#### フラッシュローン

```bash
forge test --fork-url $FORK_URL --fork-block-number $FORK_BLOCK_NUM --match-path test/Flash.test.sol -vvv
```

```bash
Logs:
  Borrowed amount: 1e9 USDC

Suite result: ok. 1 passed; 0 failed; 0 skipped; finished in 1.10s (101.25ms CPU time)
```

# まとめ

以上 UniswapV4についての解説記事になります！

Uniswap V4 は、**Hooks** による圧倒的な拡張性、**シングルトン設計**と**Flash Accounting** によるガス最適化、**ネイティブETH対応**や**ERC-6909**、**ダイナミックフィー** といった多数の革新的機能を導入しました。

Swapする前後や流動性の追加・削除に伴ってカスタムロジックを呼び出せることでuniswapの仕組みを応用したアプリが開発しやすくなっていました。

特にHooksは、Uniswap V4 上にまったく新しいDeFiプロトコルを構築する道を開いたという点で、ブロックチェーンエコシステム全体にとって大きなインパクトがあります。

皆さんもぜひお試しあれ！

ここまで読んでいただきありがとうございました！

# 参考文献

- [Uniswap V4 公式ドキュメント](https://docs.uniswap.org/contracts/v4/overview)
- [Uniswap V4 ホワイトペーパー](https://app.uniswap.org/whitepaper-v4.pdf)
- [Uniswap V4 Hooks](https://docs.uniswap.org/contracts/v4/concepts/hooks)
- [Flash Accounting](https://docs.uniswap.org/contracts/v4/concepts/flash-accounting)
- [PoolManager](https://docs.uniswap.org/contracts/v4/concepts/PoolManager)
- [Dynamic Fees](https://docs.uniswap.org/contracts/v4/concepts/dynamic-fees)
- [ERC-6909](https://docs.uniswap.org/contracts/v4/concepts/erc6909)
- [V4 vs V3](https://docs.uniswap.org/contracts/v4/concepts/v4-vs-v3)
- [Uniswap V4 Core リポジトリ](https://github.com/Uniswap/v4-core)
- [Uniswap V4 Periphery リポジトリ](https://github.com/Uniswap/v4-periphery)
- [EIP-1153: Transient Storage](https://eips.ethereum.org/EIPS/eip-1153)
- [EIP-6909: Minimal Multi-Token Interface](https://eips.ethereum.org/EIPS/eip-6909)