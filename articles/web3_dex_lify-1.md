---
title: "DEXアグリゲーターLI.FIを試してみた！"
emoji: "💰"
type: "tech" 
topics: ["Web3","blockchain","DEX","typescript","Ethereum"]
published: true
---

# はじめに

先日 **ETH Global**が主催する**HackMoney2026**に参加する機会があり**LI.FI**というDEXアグリゲーターについて調べる機会があったので学びをシェアするための記事を書きました！

https://ethglobal.com/events/hackmoney2026

ぜひ最後まで読んでいってください！

:::message
**DEXアグリゲーターとは？**
 
D複数の分散型取引所（DEX）を横断検索し、最も有利な価格や低い手数料で暗号資産をスワップ（交換）できるツールのこと。ユーザーは各DEXを手動で比較する手間なく、1inchやJupiterなどのサービスを通じて、最適なレートを自動で獲得できます。 
:::

# LI.FIの公式サイト

https://li.fi/

# 今回試したサンプルコード

以下のGitHubリポジトリで公開しています！

https://github.com/mashharuki/lify-sample

# LI.FIでやれること

開発者はLI.FIを利用することで、以下のような機能を簡単にアプリに実装できます。

1. **クロスチェーンスワップ & ブリッジ**
    - 異なるチェーン間での資産移動と交換をワンストップで行えます。
    - 例: Ethereum上の**ETH**を、Base上の**USDC**に直接交換。
  
2. **スマートルーティング**
    - 複数のDEX、ブリッジ、ソルバー（Intentベースの流動性提供者）を比較し、最も有利な手数料やレート、最速のルートを自動的に選定します。

3. **ユニバーサルな流動性アクセス**
    - 35以上のブロックチェーン（EVM、Solana、Bitcoin、SUIなど）に対応。
    - Stargate, Across, Hopなどの主要なブリッジや、Uniswap, 1inchなどのDEXを統合。

      > **対応チェーンの確認方法**
      >
      > 以下のAPIエンドポイントを叩くことで、現在LI.FIがサポートしているチェーンの一覧を確認できます。
      >
      > ```bash
      > curl --request GET --url 'https://li.quest/v1/chains' --header 'accept: application/json'
      > ```

# LI.FIのユースケース

LI.FIを活用することで、Web3アプリケーションのUXを劇的に向上させることができます！

- **クロスチェーン決済**
  - ユーザーが保有する任意のチェーンのトークンで、商品やサービスの支払いを受け付けるシステム。
- **DeFi Zaps (ワンクリック預入)**
  - 面倒なブリッジやスワップの手順を省略し、他のチェーンにある資産をワンクリックで特定のDeFiプロトコル（AaveやMorphoなど）に預け入れる機能。
- **DEX/Bridge アグリゲーション**
  - 自社ウォレットやポートフォリオ管理アプリ内に、最適なレートでの交換機能を組み込む。
- **ガス代の抽象化 (Gas Abstraction)**
  - ガス代（ETHなど）を持っていないユーザーでも、手持ちのUSDCなどでガス代を払いながらトランザクションを実行させる。

# SDKとAPIで提供している機能

LI.FIは主に**API**、**SDK**、**Widget**の3つの形態で機能を提供しています。

### LI.FI API

バックエンドや独自のフロントエンド構築向け。

- **Quote**:   
  スワップやブリッジの見積もりとトランザクションデータの取得。
- **Status**:   
  クロスチェーントランザクションの追跡。
- **Tools**:   
  利用可能なブリッジやDEXの一覧取得。

### LI.FI SDK (`@lifi/sdk`)

TypeScript/JavaScript向けの包括的な開発キット。

- **ウォレット連携**:   
  Viemなどのライブラリと簡単に統合可能。
- **ルート実行 (Execute Route)**:   
  見積もりの取得からトランザクション署名、完了までのフローを関数一つで管理。
- **イベントフック**:   
  トランザクションの進行状況に応じたUI更新が容易。

### LI.FI Widget

Reactなどのフレームワークに埋め込むだけで使える既製のUIコンポーネント。

- 複雑なUI構築なしに、クロスチェーンスワップ機能をアプリに追加可能。

# サンプルコードの動かし方

> **注意事項**
>
> メインネットでしか動かせなかったので試すときは、少額の資産で試すようにしてGOX等に十分注意してください！

## セットアップ

依存関係をインストール

```bash
bun install
```

.env を作成する

```bash
cp .env.example .env
```

WALLET_ADDRESS を自分のアドレスに変更する他、以下の値を埋めます。

今回は **zkSync**から**Base**にUSDCを動かしてみます。

```bash
# Wallet address for quote (used to compute route and fees)
WALLET_ADDRESS=<送金元のアドレス>
TO_ADDRESS=<送信先のアドレス>

FROM_CHAIN=324
TO_CHAIN=8453
FROM_TOKEN=0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4   # USDC on zkSync Era
TO_TOKEN=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913     # USDC on Base
FROM_AMOUNT=500000 # 0.5
SLIPPAGE=0.005

# Optional: execute the transaction returned by /quote
SEND_SWAP=true
RPC_URL=https://mainnet.era.zksync.io
PRIVATE_KEY=<自分の秘密鍵>

# Optional: per-chain RPC URLs (SDK demo uses these for chain switching)
RPC_URL_42161=
RPC_URL_10=
RPC_URL_8453=https://mainnet.base.org
RPC_URL_324=https://mainnet.era.zksync.io
```

ここまで埋められたら準備OKです！

## APIで動かしてみる

APIでクロスチェーンswapする場合には以下のコマンドを実行します

```bash
bun run demo:lifi:swap
```

うまくいけば以下のような結果が返ってきます。

```bash
Request:
https://li.quest/v1/quote?fromChain=324&toChain=8453&fromToken=0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4&toToken=<指定したウォレットアドレス>&fromAmount=500000&fromAddress=<指定したウォレットアドレス>&toAddress=<指定したウォレットアドレス>&slippage=0.005

Quote summary:
{
  id: "c8b3c2ca-bac7-429e-9c93-16e0867aa933:0",
  type: "lifi",
  tool: "relaydepository",
  fromToken: "USDC.e",
  toToken: "USDC",
  fromAmount: "500000",
  toAmount: undefined,
  toAmountMin: "465380",
  approvalAddress: "0x341e94069f53234fe6dabef707ad424830525715",
}

Prepared transactionRequest:
{
  to: "0x341e94069f53234fe6dabef707ad424830525715",
  from: "<指定したウォレットアドレス>",
  data: "0xa344...000",
  value: 0n,
  gasLimit: 4561411n,
  gasPrice: 63090000n,
  maxFeePerGas: undefined,
  maxPriorityFeePerGas: undefined,
  chainId: 324,
}

Sending approve transaction...
{
  hash: "<トランザクションハッシュ値>",
}
Approve confirmed.

Transaction submitted:
{
  hash: "<トランザクションハッシュ値>",
}
```

ソースコードは以下のような感じです。

これだけで最適なルートを選定してSwapしてくれるなので非常に楽ちんです！！

```ts
import "dotenv/config";
import { Contract, JsonRpcProvider, Wallet } from "ethers";

const ERC20_ABI = [
  "function allowance(address owner, address spender) view returns (uint256)",
  "function approve(address spender, uint256 amount) returns (bool)",
];

const API_BASE_URL = "https://li.quest/v1";

const env = process.env;

const requiredWallet = env.WALLET_ADDRESS;
if (!requiredWallet) {
  console.error("Missing WALLET_ADDRESS in environment.");
  console.error("Set it in .env (see .env.example).");
  process.exit(1);
}

const fromChain = env.FROM_CHAIN ?? "42161"; // Arbitrum One
const toChain = env.TO_CHAIN ?? "10"; // Optimism
const fromToken = env.FROM_TOKEN ?? "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"; // USDC on Arbitrum
const toToken = env.TO_TOKEN ?? "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"; // DAI on Optimism
const fromAmount = env.FROM_AMOUNT ?? "1000000"; // 1.0 USDC (6 decimals)
const slippage = env.SLIPPAGE ?? "0.005"; // 0.5%

const params = new URLSearchParams({
  fromChain,
  toChain,
  fromToken,
  toToken,
  fromAmount,
  fromAddress: requiredWallet,
  toAddress: env.TO_ADDRESS ?? requiredWallet,
  slippage,
});

const headers: Record<string, string> = {
  Accept: "application/json",
};

if (env.LIFI_API_KEY) {
  headers["x-lifi-api-key"] = env.LIFI_API_KEY;
}

// LI.FI API does not expose a direct /swap endpoint; execution happens by
// sending the returned transactionRequest from /quote (single-step) or
// /advanced/stepTransaction (multi-step routes). This sample uses /quote.
const url = `${API_BASE_URL}/quote?${params.toString()}`;

console.log("Request:");
console.log(url);

const res = await fetch(url, { headers });
if (!res.ok) {
  const errorText = await res.text();
  console.error(`LI.FI API error: ${res.status} ${res.statusText}`);
  console.error(errorText);
  process.exit(1);
}

const data = (await res.json()) as {
  id?: string;
  type?: string;
  tool?: string;
  action?: {
    fromToken?: { symbol?: string; address?: string };
    toToken?: { symbol?: string; address?: string };
    fromAmount?: string;
    toAmount?: string;
  };
  estimate?: {
    approvalAddress?: string;
    toAmountMin?: string;
  };
  transactionRequest?: {
    to?: string;
    from?: string;
    data?: string;
    value?: string;
    gasLimit?: string;
    gasPrice?: string;
    maxFeePerGas?: string;
    maxPriorityFeePerGas?: string;
    chainId?: number | string;
  };
};

console.log("\nQuote summary:");
console.log({
  id: data.id,
  type: data.type,
  tool: data.tool,
  fromToken: data.action?.fromToken?.symbol ?? data.action?.fromToken?.address,
  toToken: data.action?.toToken?.symbol ?? data.action?.toToken?.address,
  fromAmount: data.action?.fromAmount,
  toAmount: data.action?.toAmount,
  toAmountMin: data.estimate?.toAmountMin,
  approvalAddress: data.estimate?.approvalAddress,
});

if (!data.transactionRequest) {
  console.error("Missing transactionRequest in quote response.");
  process.exit(1);
}

const preparedTx = formatTransactionRequest(data.transactionRequest);

console.log("\nPrepared transactionRequest:");
console.log(preparedTx);

const shouldSend = (env.SEND_SWAP ?? "").toLowerCase() === "true";
if (!shouldSend) {
  console.log(
    "\nSEND_SWAP is not true. Set SEND_SWAP=true and provide RPC_URL and PRIVATE_KEY to send the transaction.",
  );
  process.exit(0);
}

const rpcUrl = env.RPC_URL;
const privateKey = env.PRIVATE_KEY;
if (!rpcUrl || !privateKey) {
  console.error("RPC_URL and PRIVATE_KEY are required to send the swap.");
  process.exit(1);
}

const provider = new JsonRpcProvider(rpcUrl);
const wallet = new Wallet(privateKey, provider);
const walletAddress = await wallet.getAddress();

if (walletAddress.toLowerCase() !== requiredWallet.toLowerCase()) {
  console.warn(
    `Warning: wallet address ${walletAddress} does not match WALLET_ADDRESS ${requiredWallet}.`,
  );
}

const network = await provider.getNetwork();
if (preparedTx.chainId && preparedTx.chainId !== Number(network.chainId)) {
  console.warn(
    `Warning: transactionRequest.chainId ${preparedTx.chainId} does not match RPC chainId ${network.chainId}.`,
  );
}

await ensureApproval({
  fromToken: data.action?.fromToken?.address ?? fromToken,
  owner: walletAddress,
  spender: data.estimate?.approvalAddress,
  amount: data.action?.fromAmount ?? fromAmount,
  wallet,
});

const txResponse = await wallet.sendTransaction({
  to: preparedTx.to,
  data: preparedTx.data,
  value: preparedTx.value,
  gasLimit: preparedTx.gasLimit,
  gasPrice: preparedTx.gasPrice,
  maxFeePerGas: preparedTx.maxFeePerGas,
  maxPriorityFeePerGas: preparedTx.maxPriorityFeePerGas,
});

console.log("\nTransaction submitted:");
console.log({
  hash: txResponse.hash,
});

function formatTransactionRequest(input: {
  to?: string;
  from?: string;
  data?: string;
  value?: string;
  gasLimit?: string;
  gasPrice?: string;
  maxFeePerGas?: string;
  maxPriorityFeePerGas?: string;
  chainId?: number | string;
}) {
  const toBigInt = (value?: string) => (value ? BigInt(value) : undefined);
  const chainIdValue = typeof input.chainId === "string" ? Number(input.chainId) : input.chainId;

  if (!input.to) {
    throw new Error("transactionRequest.to is missing.");
  }

  return {
    to: input.to,
    from: input.from,
    data: input.data ?? "0x",
    value: toBigInt(input.value),
    gasLimit: toBigInt(input.gasLimit),
    gasPrice: toBigInt(input.gasPrice),
    maxFeePerGas: toBigInt(input.maxFeePerGas),
    maxPriorityFeePerGas: toBigInt(input.maxPriorityFeePerGas),
    chainId: chainIdValue,
  };
}

async function ensureApproval(options: {
  fromToken: string;
  owner: string;
  spender?: string;
  amount: string;
  wallet: Wallet;
}) {
  const zeroAddress = "0x0000000000000000000000000000000000000000";
  const { fromToken, owner, spender, amount, wallet } = options;

  if (!spender) {
    console.log("\nNo approvalAddress provided. Skipping approve.");
    return;
  }

  if (fromToken.toLowerCase() === zeroAddress) {
    console.log("\nNative token swap detected. No approve needed.");
    return;
  }

  const token = new Contract(fromToken, ERC20_ABI, wallet);
  const currentAllowance = (await token.allowance(owner, spender)) as bigint;
  const requiredAmount = BigInt(amount);

  if (currentAllowance >= requiredAmount) {
    console.log("\nAllowance is sufficient. No approve needed.");
    return;
  }

  console.log("\nSending approve transaction...");
  const approveTx = await token.approve(spender, requiredAmount);
  console.log({ hash: approveTx.hash });
  await approveTx.wait();
  console.log("Approve confirmed.");
}

```

## SDKで動かしてみる

次にSDKでも試してみます！

```bash
bun run demo:lifi:sdk
```

以下のようになればOKです！

```bash
Quote summary:
{
  fromChain: 324,
  toChain: 8453,
  fromToken: "USDC.e",
  toToken: "USDC",
  fromAmount: "500000",
  toAmount: undefined,
  tool: "relaydepository",
  approvalAddress: "0x341e94069f53234fe6dabef707ad424830525715",
}

Sending approve transaction...
{
  hash: "<トランザクションハッシュ値>",
}
Tx hash (step 1, CROSS_CHAIN): <トランザクションハッシュ値>
Tx hash (step 1, CROSS_CHAIN): <トランザクションハッシュ値>
Tx hash (step 1, CROSS_CHAIN): <トランザクションハッシュ値>
Tx hash (step 1, CROSS_CHAIN): <トランザクションハッシュ値>
Tx hash (step 1, RECEIVING_CHAIN):<トランザクションハッシュ値>
Tx hash (step 1, CROSS_CHAIN): <トランザクションハッシュ値>
Tx hash (step 1, RECEIVING_CHAIN): <トランザクションハッシュ値>

Execution finished:
{
  routeId: undefined,
  status: undefined
}
```

ソースコードは以下のような感じです！

APIを使った時よりもこっちの方がスッキリしますね

```ts
import {
  EVM,
  type QuoteRequest,
  type RouteExtended,
  convertQuoteToRoute,
  createConfig,
  executeRoute,
  getQuote,
  getTokenAllowance,
  setTokenAllowance,
} from "@lifi/sdk";
import "dotenv/config";
import { type Chain, type WalletClient, createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { arbitrum, base, mainnet, optimism, zksync } from "viem/chains";

const ZERO_ADDRESS = "0x0000000000000000000000000000000000000000";

const env = process.env;

const requiredWallet = env.WALLET_ADDRESS;
if (!requiredWallet) {
  console.error("Missing WALLET_ADDRESS in environment.");
  console.error("Set it in .env (see .env.example).");
  process.exit(1);
}

const privateKey = env.PRIVATE_KEY as `0x${string}` | undefined;
if (!privateKey) {
  console.error("Missing PRIVATE_KEY in environment.");
  console.error("Set it in .env (see .env.example).");
  process.exit(1);
}

// 環境変数が設定されていない場合はデフォルト値を設定する
const integrator = env.LIFI_INTEGRATOR ?? "lify-sample";

const fromChain = Number(env.FROM_CHAIN ?? "42161");
const toChain = Number(env.TO_CHAIN ?? "10");
const fromToken = env.FROM_TOKEN ?? "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"; // USDC on Arbitrum
const toToken = env.TO_TOKEN ?? "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"; // DAI on Optimism
const fromAmount = env.FROM_AMOUNT ?? "1000000"; // 1.0 USDC (6 decimals)
const slippage = env.SLIPPAGE ? Number(env.SLIPPAGE) : undefined;

const account = privateKeyToAccount(privateKey);
const walletAddress = account.address;

if (walletAddress.toLowerCase() !== requiredWallet.toLowerCase()) {
  console.warn(
    `Warning: wallet address ${walletAddress} does not match WALLET_ADDRESS ${requiredWallet}.`,
  );
}

const chainMap: Record<number, Chain> = {
  1: mainnet,
  10: optimism,
  42161: arbitrum,
  8453: base,
  324: zksync,
};

const getChain = (chainId: number) => {
  const chain = chainMap[chainId];
  if (!chain) {
    throw new Error(
      `Unsupported chainId ${chainId}. Add it to chainMap or provide a custom Chain definition.`,
    );
  }
  return chain;
};

const getRpcUrl = (chainId: number) => {
  const keyed = env[`RPC_URL_${chainId}`];
  if (keyed) return keyed;
  if (chainId === fromChain && env.RPC_URL) return env.RPC_URL;
  return undefined;
};

// Walletクライアントを作成
let walletClient = createWalletClient({
  account,
  chain: getChain(fromChain),
  transport: http(getRpcUrl(fromChain)),
});

/**
 * EVM Providerを取得する
 */
const evmProvider = EVM({
  getWalletClient: async () => walletClient,
  switchChain: async (chainId: number) => {
    walletClient = createWalletClient({
      account,
      chain: getChain(chainId),
      transport: http(getRpcUrl(chainId)),
    });
    return walletClient;
  },
});

createConfig({
  integrator,
  providers: [evmProvider],
});

// クォートを取得するためのリクエストデータ
const quoteRequest: QuoteRequest = {
  fromChain,
  toChain,
  fromToken,
  toToken,
  fromAmount,
  fromAddress: walletAddress,
  toAddress: env.TO_ADDRESS ?? walletAddress,
  slippage,
};
// クォートを取得する
const quote = await getQuote(quoteRequest);

console.log("Quote summary:");
console.log({
  fromChain,
  toChain,
  fromToken: quote.action?.fromToken?.symbol ?? quote.action?.fromToken?.address,
  toToken: quote.action?.toToken?.symbol ?? quote.action?.toToken?.address,
  fromAmount: quote.action?.fromAmount,
  toAmount: quote.action?.toAmount,
  tool: quote.tool,
  approvalAddress: quote.estimate?.approvalAddress,
});

const route = convertQuoteToRoute(quote);

const shouldSend = (env.SEND_SWAP ?? "").toLowerCase() === "true";
if (!shouldSend) {
  console.log("\nSEND_SWAP is not true. Set SEND_SWAP=true to execute the route.");
  process.exit(0);
}

// approveトランザクションを取得する
await ensureAllowance({
  chainId: fromChain,
  tokenAddress: fromToken,
  ownerAddress: walletAddress,
  spenderAddress: quote.estimate?.approvalAddress,
  amount: BigInt(fromAmount),
  walletClient,
});

// swapを実行
const executedRoute = await executeRoute(route, {
  updateRouteHook: (updatedRoute: RouteExtended) => {
    logTransactionHashes(updatedRoute);
  },
});

console.log("\nExecution finished:");
console.log({
  routeId: executedRoute.routeId,
  status: executedRoute.status,
});

function logTransactionHashes(route: RouteExtended) {
  for (const [index, step] of route.steps.entries()) {
    step.execution?.process?.forEach((process) => {
      if (process.txHash) {
        console.log(`Tx hash (step ${index + 1}, ${process.type}): ${process.txHash}`);
      }
    });
  }
}

async function ensureAllowance(options: {
  chainId: number;
  tokenAddress: string;
  ownerAddress: string;
  spenderAddress?: string;
  amount: bigint;
  walletClient: WalletClient;
}) {
  const { chainId, tokenAddress, ownerAddress, spenderAddress, amount, walletClient } = options;

  if (!spenderAddress) {
    console.log("\nNo approvalAddress provided. Skipping approve.");
    return;
  }

  if (tokenAddress.toLowerCase() === ZERO_ADDRESS) {
    console.log("\nNative token swap detected. No approve needed.");
    return;
  }

  const token = { address: tokenAddress, chainId };
  const allowance = await getTokenAllowance(token, ownerAddress, spenderAddress);

  if (allowance && allowance >= amount) {
    console.log("\nAllowance is sufficient. No approve needed.");
    return;
  }

  console.log("\nSending approve transaction...");
  const txHash = await setTokenAllowance({
    walletClient,
    token,
    spenderAddress,
    amount,
  });
  console.log({ hash: txHash });
}
```

# まとめ

**LI.FI**についてまとめてみました！

触った感じユーザー体験的には**1inch**とさほど変わらないという印象でした。

他にも機能がリリース予定とのことなので今後もウォッチしてリリースされたら新機能を試してみようと思います！！

# 参考文献

- [API ドキュメント](https://docs.li.fi/api-reference/introduction)
- [SDK ドキュメント](https://docs.li.fi/sdk/overview?utm_source=lifi&utm_medium=header_developers_get_started&utm_campaign=lifi_to_docs)
- [Widget ドキュメント](https://docs.li.fi/widget/overview?utm_source=lifi&utm_medium=header_developers_get_started&utm_campaign=lifi_to_docs)