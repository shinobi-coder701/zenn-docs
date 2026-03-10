---
title: "Sera Protocolのチュートリアルに挑戦してみた！"
emoji: "🤑"
type: "tech"
topics: ["ethereum", "dex", "stablecoin", "clob", "defi"]
published: true
---

# はじめに

これまで記事で **Sera Protocol**の概要やGraphQLの使い方を取り上げてきました。

https://zenn.dev/mashharuki/articles/web3_sera_protocol-1

https://zenn.dev/mashharuki/articles/web3_sera_protocol-2

https://zenn.dev/mashharuki/articles/web3_sera_protocol-3

今回の記事では**Sera Protocol**のコントラクトを呼び出すチュートリアルを解説します！

# Sera Protocolのコントラクトについて

**Sera Protocol**のコントラクトで提供されている機能は以下のとおりです！

Sera Protocolのスマートコントラクト群は主に4つのコアコントラクトで構成されています。

それぞれが取引の実行、オーダーブックの管理、価格計算、注文のキャンセルといった特定の役割を担っています。

### 1. Market Router (マーケット・ルーター)

ユーザーが取引を行う際の**主要な入り口（エントリーポイント）**となるコントラクトです。  
直接OrderBookを叩くのではなく、通常はこのルーターを介して操作を行います。

*   **指値注文 (Limit Orders)**:    
  `limitBid`（買い注文）、`limitAsk`（売り注文）、および複数の指値注文を一度に出す `limitOrder` 機能を提供します。

*   **成行注文 (Market Orders)**:   
  即座に約定させる `marketBid` や `marketAsk` を実行します。

*   **利益の請求 (Claiming)**:   
  約定した注文から利益を回収する `claim` 機能を提供します。複数の市場にまたがる請求も可能です。

*   **複合操作**:   
  利益を請求した直後に新しい注文を出す `limitBidAfterClaim` などの、ガス代を節約するための便利な機能も備えています。

*   **市場確認**:   
  `isRegisteredMarket` により、その市場が公式に登録されている正当なものかを確認できます。

### 2. OrderBook (オーダーブック)

各取引ペアごとに個別のコントラクトとして存在し、**注文の保存、マッチング、決済**を管理します。

*   **状態の確認**:   
  `getDepth`（特定価格の板の厚み取得）、`bestPriceIndex`（最良気配値の取得）、`isEmpty`（板が空かどうかの確認）などの参照機能を提供します。

*   **注文詳細の取得**:  
   `getOrder` で特定の注文内容を、`getClaimable` で請求可能な金額や手数料の詳細を確認できます。

*   **シミュレーション**:   
  `getExpectedAmount` を使うことで、成行注文を出した際に期待される入力・出力額をシミュレーションできます。

### 3. PriceBook (プライスブック)

Sera独自の**算術価格モデル（Arithmetic Price Model）**に基づいた計算を専門に行うコントラクトです。

*   **価格変換**:   
  `indexToPrice`（価格インデックスを実際の価格に変換）および `priceToIndex`（実際の価格を最も近いインデックスに変換）機能を提供します。

*   **価格範囲の取得**:   
  `maxPriceIndex`（最大インデックス）、`minPrice`（最小価格）、`priceUpperBound`（最大サポート価格）などを参照できます。

### 4. Order Canceler (オーダー・キャンセラー)
s
複数の市場にまたがる注文を効率的に**一括キャンセル**するためのユーティリティ・コントラクトです。注文はNFT IDによって識別されます。

*   **一括キャンセル**:   
  `cancel`（注文をキャンセルし、資産を自分のアドレスに戻す）および `cancelTo`（資産を特定のアドレスに送る）機能を提供します。

*   **自動請求**:   
  キャンセル時、その注文で既に約定していた分がある場合は、自動的に利益の請求（Claim）も行われます。

### 補足：Order NFT

各指値注文が作成されると、その所有権を表す**NFT**が発行されます。これにより、注文の所有権を別のアドレスに移転したり、他のDeFiプロトコルで再利用したりすることが可能になります。

# サンプルコードを実装してみよう！

今回試すコードは以下のGitHubリポジトリに格納されています！

https://github.com/mashharuki/SeraProtocol-Sample

## このサンプルコードで提供されている機能

- マーケット情報取得（Subgraph）
- Base/Quote 2トークン残高表示
- 板情報（best bid / best ask）取得
- `postOnly` 安全化付き `limitBid` 発注
- 注文状態ポーリング
- 自動 `claim`（claimableがある場合）
- `claim-only` モード（後から単独で claim 可能）

## ファイル構成

- `src/index.ts`:   
  実行フロー（オーケストレーション）
- `src/lib/viem.ts`:   
  viemクライアント生成、approve/place/claim、simulate
- `src/utils/constants.ts`:   
  アドレス、ABI、RPC、chain
- `src/utils/helpers.ts`:   
  CLIパース、GraphQL取得、価格補正などの共通ヘルパー

## セットアップ

Gitリポジトリをクローンしたら環境変数をセットアップします。

今回試すコードは`tutorial`フォルダ配下に存在します。

```bash
cp .env.example .env
```

秘密鍵は**Metamask**からコピペしてきてください。

```bash
PRIVATE_KEY=0xYOUR_PRIVATE_KEY
SEPOLIA_RPC_URL=https://0xrpc.io/sep
```

次に依存関係をインストールしてください。

```bash
bun i
```

## 動かしてみよう！

以下のコマンドを実行すると取引ができます！

```bash
bun run dev
```

以下のようになればOKです！

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

## コードの解説

- `lib/viem.ts`

  このファイルではViemクライアントやコントラクトのメソッドを呼び出すための関数を実装しているファイルです。

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
   * Viemクライアントの作成
   * Bun環境でのイーサリアムクライアントを初期化します。
   * 公開クライアントはチェーンデータの読み取りに使用され、ウォレットクライアントは署名付きトランザクションの送信に使用されます。
   * @param account 
   * @returns 
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

  export async function getTokenBalance(args: {
    publicClient: ReturnType<typeof createPublicClient>;
    account: Address;
    tokenAddress: Address;
  }): Promise<bigint> {
    const { publicClient, account, tokenAddress } = args;

    return publicClient.readContract({
      address: tokenAddress,
      abi: ERC20_ABI,
      functionName: "balanceOf",
      args: [account],
    });
  }

  /**
   * 必要な場合にERC20トークンの承認を行うユーティリティ関数
   * 指定された量のトークンがspenderに対してすでに承認されているかを確認し、必要に応じてapproveトランザクションを送信します。
   * @param args 
   * @returns 
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
   * リミット注文を配置するユーティリティ関数
   * 指定された市場、価格インデックス、数量でリミット注文を作成します。
   * @param args 
   * @returns 
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
        postOnly: true,
        useNative: false,
        baseAmount: 0n,
      },
    ] as const;

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
        throw new Error(
          "limitBid simulation failed: ERC20InsufficientBalance. Your quote token balance is not enough for this order size/price.",
        );
      }
      throw new Error(`limitBid simulation failed: ${reason}`);
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

  /**
   * オーダーを請求するユーティリティ関数
   * 指定された注文が約定している場合に、利益を請求するためのトランザクションを送信します。
   * @param args 
   * @returns 
   */
  export async function claimOrder(args: {
    publicClient: ReturnType<typeof createPublicClient>;
    walletClient: ReturnType<typeof createWalletClient>;
    account: PrivateKeyAccount;
    market: Address;
    order: OpenOrder;
  }): Promise<Hex> {
    const { publicClient, walletClient, account, market, order } = args;
    const deadline = BigInt(Math.floor(Date.now() / 1000) + 600);

    const txHash = await walletClient.writeContract({
      address: ROUTER_ADDRESS,
      abi: ROUTER_ABI,
      functionName: "claim",
      args: [
        deadline,
        [
          {
            market,
            orderKeys: [
              {
                isBid: order.isBid,
                priceIndex: Number(order.priceIndex),
                orderIndex: BigInt(order.orderIndex),
              },
            ],
          },
        ],
      ],
      account,
      chain: sepolia,
    });

    await publicClient.waitForTransactionReceipt({ hash: txHash });
    return txHash;
  }
  ```

- `index.ts`

  このファイルにマーケットの情報取得からオーダー実行までの一連のソースコードが実装してあります！

  ```ts
  import "dotenv/config";
  import { formatUnits, isAddress, type Address } from "viem";
  import { privateKeyToAccount } from "viem/accounts";
  import {
    approveTokenIfNeeded,
    claimOrder,
    createViemClients,
    getTokenBalance,
    placeLimitBid,
  } from "./lib/viem";
  import {
    MARKET_ADDRESS,
    PRIVATE_KEY,
    ROUTER_ADDRESS,
    RPC_URL,
  } from "./utils/constants";
  import {
    getMarketInfo,
    getOrderBook,
    getUserOrders,
    parseCliOptions,
    requirePrivateKey,
    resolvePostOnlyBidPriceIndex,
    sleep,
    type OpenOrder,
  } from "./utils/helpers";

  /**
  * メイン関数
  * Sera Protocolの注文ライフサイクルをデモンストレーションするスクリプトです。
  * 1. 市場情報の取得
  * 2. 注文板の深さの取得
  * 3. 既存の注文の確認
  * 4. リミット注文の配置  
  * 5. GraphQLを介した注文状況の監視
  * 6. 利益の請求（利用可能な場合）
  * 
  * コマンドライン引数:
  * --price-index <number> : 注文の価格インデックス（省略時は最新価格から100下）
  * --raw-amount <bigint> : 注文の原始数量（省略時は1000）
  */
  async function main() {
    console.log("Sera Protocol - Order Lifecycle Demo (Bun + TypeScript + viem)\n");
    const cli = parseCliOptions(process.argv.slice(2));

    const privateKey = requirePrivateKey(PRIVATE_KEY);
    const account = privateKeyToAccount(privateKey);
    const { publicClient, walletClient } = createViemClients(account);

    if (!isAddress(MARKET_ADDRESS) || !isAddress(ROUTER_ADDRESS)) {
      throw new Error("Invalid configured address");
    }

    console.log(`Wallet: ${account.address}`);
    console.log(`RPC: ${RPC_URL}`);

    // 1. Get market info
    const market = await getMarketInfo(MARKET_ADDRESS);
    console.log(`Market: ${market.baseToken.symbol}/${market.quoteToken.symbol}`);
    console.log(
      `Latest: index=${market.latestPriceIndex}, price=${formatUnits(BigInt(market.latestPrice), Number(market.quoteToken.decimals))}`,
    );

    // get token balances
    const baseTokenAddress = market.baseToken.id as Address;
    const quoteTokenAddress = market.quoteToken.id as Address;
    const [baseBalance, quoteBalance] = await Promise.all([
      getTokenBalance({
        publicClient,
        account: account.address,
        tokenAddress: baseTokenAddress,
      }),
      getTokenBalance({
        publicClient,
        account: account.address,
        tokenAddress: quoteTokenAddress,
      }),
    ]);

    console.log(
      `Balances: ${market.baseToken.symbol}=${formatUnits(baseBalance, Number(market.baseToken.decimals))}, ${market.quoteToken.symbol}=${formatUnits(quoteBalance, Number(market.quoteToken.decimals))}`,
    );

    // 2. Get order book depth
    const depth = await getOrderBook(MARKET_ADDRESS);
    console.log(`Depth: bids=${depth.bids.length}, asks=${depth.asks.length}`);
    const bestBid = depth.bids[0]?.priceIndex ?? "-";
    const bestAsk = depth.asks[0]?.priceIndex ?? "-";
    console.log(`Top of book: bestBidIndex=${bestBid}, bestAskIndex=${bestAsk}`);

    // 3. Check existing orders
    const existingOrders = await getUserOrders(account.address, MARKET_ADDRESS);
    console.log(`Your open orders (before): ${existingOrders.length}`);

    if (cli.claimOnly) {
      let targetOrder: OpenOrder | undefined;

      if (cli.claimPriceIndex !== undefined && cli.claimOrderIndex !== undefined) {
        targetOrder = existingOrders.find(
          (order) =>
            Number(order.priceIndex) === cli.claimPriceIndex &&
            BigInt(order.orderIndex) === cli.claimOrderIndex &&
            order.isBid === (cli.claimIsBid ?? true),
        );
      } else {
        targetOrder = existingOrders.find((order) => BigInt(order.claimableAmount) > 0n);
      }

      if (!targetOrder) {
        throw new Error(
          "No claim target found. Use --claim-price-index and --claim-order-index, or wait until claimableAmount > 0.",
        );
      }

      console.log(
        `Claim target: isBid=${targetOrder.isBid}, priceIndex=${targetOrder.priceIndex}, orderIndex=${targetOrder.orderIndex}, claimable=${targetOrder.claimableAmount}`,
      );

      // Claim proceeds
      const claimTx = await claimOrder({
        publicClient,
        walletClient,
        account,
        market: MARKET_ADDRESS,
        order: targetOrder,
      });
      console.log(`Claimed proceeds: ${claimTx}`);
      return;
    }

    // 4. Place a limit order
    const latestPriceIndex = Number(market.latestPriceIndex);
    const requestedPriceIndex = cli.priceIndex ?? Math.max(1, latestPriceIndex - 100);
    // Ensure the price index is valid and won't cause immediate execution
    const priceIndex = resolvePostOnlyBidPriceIndex({
      desiredPriceIndex: requestedPriceIndex,
      bids: depth.bids,
      asks: depth.asks,
    });
    const rawAmount = cli.rawAmount ?? 1000n;
    const approveAmount = rawAmount * BigInt(market.quoteUnit);

    if (priceIndex !== requestedPriceIndex) {
      console.log(
        `Adjusted priceIndex for postOnly safety: requested=${requestedPriceIndex} -> resolved=${priceIndex}`,
      );
    }

    console.log(
      `Placing limit bid: priceIndex=${priceIndex}, rawAmount=${rawAmount.toString()}, approve=${approveAmount.toString()}`,
    );

    // Approve quote token if needed
    const approveTx = await approveTokenIfNeeded({
      publicClient,
      walletClient,
      account,
      tokenAddress: quoteTokenAddress,
      spender: ROUTER_ADDRESS,
      amount: approveAmount,
    });

    if (approveTx) {
      console.log(`Approved quote token: ${approveTx}`);
    } else {
      console.log("Allowance already sufficient; skipping approve");
    }

    // Place limit bid
    const orderTx = await placeLimitBid({
      publicClient,
      walletClient,
      account,
      market: MARKET_ADDRESS,
      priceIndex,
      rawAmount,
    });
    console.log(`Order tx: ${orderTx}`);

    // 5. Monitor order status via GraphQL
    console.log("Monitoring order status...");
    let latestOrders: OpenOrder[] = [];
    for (let i = 1; i <= 6; i += 1) {
      await sleep(3000);
      latestOrders = await getUserOrders(account.address, MARKET_ADDRESS);

      const top = latestOrders[0];
      if (!top) {
        console.log(`[poll ${i}] no orders yet`);
        continue;
      }

      console.log(
        `[poll ${i}] status=${top.status}, filled=${top.rawFilledAmount}/${top.rawAmount}, claimable=${top.claimableAmount}, key={isBid:${top.isBid},priceIndex:${top.priceIndex},orderIndex:${top.orderIndex}}`,
      );
    }

    // 6. Claim proceeds if available
    const claimableOrder = latestOrders.find((order) => BigInt(order.claimableAmount) > 0n);

    if (!claimableOrder) {
      console.log("No claimable order found yet. Try re-running after more fills.");
      const pending = latestOrders[0];
      if (pending) {
        console.log(
          `Pending order key: isBid=${pending.isBid}, priceIndex=${pending.priceIndex}, orderIndex=${pending.orderIndex}`,
        );
        console.log(
          `Claim-only command: bun run start -- --claim-only --claim-price-index ${pending.priceIndex} --claim-order-index ${pending.orderIndex} --claim-is-bid ${pending.isBid}`,
        );
      }
    } else {
      // Claim proceeds
      const claimTx = await claimOrder({
        publicClient,
        walletClient,
        account,
        market: MARKET_ADDRESS,
        order: claimableOrder,
      });
      console.log(`Claimed proceeds: ${claimTx}`);
    }

    const updatedOrders = await getUserOrders(account.address, MARKET_ADDRESS);
    console.log(`Your open orders (after): ${updatedOrders.length}`);
  }

  main().catch((error) => {
    console.error("\nScript failed:");
    console.error(error instanceof Error ? error.message : error);
    process.exit(1);
  });
  ```

今回はここまでになります！