---
title: "AI AgentでDeFAIを作ってみて分かったこと！"
emoji: "🔨"
type: "tech"
topics: ["AIAgent", "OpenAI", "Web3", "LangChain", "TypeScript"]
published: true
---

![0.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1299653/0b1e29d0-2657-44b1-83c7-02026e65e7af.jpeg)

## はじめに

皆さん、こんにちは！

先日、AI Agent を使って **DeFAI** のプロダクトを開発する機会がありましたのでその時に分かったことなどを記事にしてまとめてみました！

このあたりについて技術的に深掘りされた日本語の記事はまだ少ないと思いますのでぜひ最後まで読んでみてください！

## DeFAI とは

まず、 **DeFAI** というキーワードについて解説したいと思います。

Web3 界隈にいない方は馴染みないワードだと思います。

**DeFAI** とは **DeFi** と **AI** を組み合わせた新しい用語です！

https://coinpost.jp/?p=591072

24 年の秋頃から、市場では Crypto×AI の分野の注目度が高まり、関連のトークンが価格上昇を見せています。これまでは AI Agent といえば X で自律的にコンテンツを投稿していくエンタメ的な側面に注目されがちでしたが、ユーザー体験を大きく向上させるものとして DeFi などのアプリケーションへの応用が注目を集めていました。

## プロジェクト概要

ではここから作ったプロダクトの概要について共有していきたいと思います。

出場したハッカソンの情報や GitHub リポジトリは以下にまとめさせていただきました。

:::message
出場したハッカソン
:::

**Eth Global - Agentic Ethereum**

https://ethglobal.com/events/agents

**Google AI Agent Hackathon**

https://cloud.google.com/blog/ja/products/ai-machine-learning/lets-create-the-future-with-the-generative-ai-hackathon

:::message
GitHub リポジトリ
:::

https://github.com/mashharuki/AgenticEthereum2025

:::message
Live demo
:::

https://agentic-ethereum2025.vercel.app/

:::message
デモ動画
:::

約 3 分のデモ動画です

https://youtu.be/Iz8RTY9Y5O4

:::message
プレゼンスライド
:::

https://www.canva.com/design/DAGefDFBArA/_xcY_cQQbtkpVvVb0DZBLg/view?utm_content=DAGefDFBArA&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h830ea1c854

### 概要

今回、ハッカソンで作ったのはマルチ AI Agent でライブディスカッションを行わせて資産を最大化するための DeFi 操作を選定してもらい、そのトランザクションの実行までを自動的に実施してもらうというものです。

AI Agent には 6 つの役割を与えて実装してみました。

- **ソーシャルトレンド収集スペシャリスト**
- **ニュースと基本情報のスペシャリスト**
- **リスク管理エージェント**
- **パフォーマンスモニタリングエージェント**
- **分析と戦略エージェント**
- **実行と運用エージェント**

基本的には、情報を収集してリスク分析やパフォーマンスを監視させた後に実行する処理を決めさせています。

### なぜ作ろうと思ったのか？

**DeFi** におけるユーザー体験の向上を目的に作ろうと思ったことがきっかけです。

まず、 **DeFi** にはかなり専門知識が求められます。

Web3 の技術的な知識、最新のトレンド情報以外にも金融の知識やそれに関する世論の情勢など複数の領域に対して深い知識が必要となります。

そのため、新規のユーザーがいきなり使い始めるのには非常にハードルが高くなってしまっています。

そのギャップを埋めるために仕組みが必要だと感じていました。

その解決策として AI Agent が使えないかと思って試してみたというのが動機です。

ただ単にトランザクションを自動で実行するだけでなく、マルチ AI Agent にインタラクティブに議論させて自分の資産を最も効率よく増やす方法を議論してもらい、その結果として最適な DeFi 操作を選定してもらうという部分まで AI Agent に担当してもらうことでユーザー体験を向上させることができるのではないかと考えました。

ニコニコ動画の生配信みたくエンタメ性も持たせてみたというのも挑戦の部分です。

AI 達がどんな結論を出すのかというワクワク感も持たせてみました。

## アーキテクチャと技術スタック

:::message
アーキテクチャ
:::

今回開発したプロダクトのアーキテクチャ図は以下の通りです。

![architecture.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1299653/90f134d2-e574-4da0-8439-2a0399114d70.png)

AI Agent 系の処理は Hono で作った API で実行させるようにしています！

API の実行環境として、 **Google Cloud** の **Cloud Run** を使っています！

https://cloud.google.com/run?hl=ja

**Fargate** よりも簡単にセットアップできるのでおすすめです！

AI Agent 用のウォレットの情報は、 **Privy** の **server wallet** の機能を使っています！

流石に環境変数で秘密鍵を埋め込むのはセキュリティ的によろしくないなと思ったのでこのような実装としています！

:::message
技術スタック一覧
:::

今回、採用した技術スタックの一覧です！

Web3、AI 以外にも **Cluod Run** など Web2 のスタックも沢山使いました！！

| カテゴリ      | 使用技術                                                                                         |
| :------------ | :----------------------------------------------------------------------------------------------- |
| Frontend      | TypeScript<br/> OnChain Kit<br/> Next.js<br/> Tailwind CSS<br/> Vercel                           |
| Backend       | TypeScript<br/> Cloud Run<br/> Hono                                                              |
| IasC          | CDK for Terraform                                                                                |
| LLM           | OpenAI<br/> Claude<br/> llama<br/> Gemini in Vertex AI                                           |
| AI Agent Kit  | LangChain<br/> LangGraph<br/> Groq Agent Kit<br/> Vertex AI                                      |
| Web3 Library  | viem<br/> wagmi<br/> Coinbase AgentKit<br/> Privy Server Wallet<br/> Autonome<br/> CoinGekko API |
| DeFi Protocol | Uniswap<br/> AAVE<br/> Lido<br/> EigenLayer                                                      |

**Autonome** は AI Agent 用のインスタンスをホスティングできるサービスで、公式に用意されているテンプレート(Docker Container イメージ)以外にもオリジナルのコンテナイメージを共有することができます！

以下は、実際にプッシュしてみたテンプレートです！

https://apps.autono.meme/autonome/new?template=e57de5de-00e6-47c2-8e5e-ebdfbcda589b

Docker Hub にもイメージをプッシュしています！

https://hub.docker.com/repository/docker/haruki31067/autonome-cdp-custom/general

動くコンテナイメージを作るのに苦労しましたが、一度動いてしまえば非常に使いやすいサービスでした！

## 課題と解決策

統合プロセスで直面した課題と、それをどのように克服したかを強調します。技術的な障害、デザインの考慮事項、プロジェクト管理の問題などを含めます。

## 主な学び

今回のプロダクトを作ってみて大きな学びが 2 つありました！

:::message
**DeFi 用の AI Agent ツールの実装方法の習得**
**プロンプトチェイニングの重要性の再認識**
:::

この 2 つですね。

Web3 用の AI Agent ツールの数は圧倒的に少ないというのが現状です。そのため、今回のハッカソンでは AI Agent 用のツールを揃える部分から始めなくてはなりませんでした。

その実装方法がわかるまで苦労したのですが、なんとかその方法を理解し、最終的に 4 つの DeFi プロトコル用のツールを作ることができたのでその詳細もこの後共有させていただきます！

プロンプトチェイニングの重要性も再認識できました。

複数の AI Agent がそれぞれ与えた役割をしっかりとこなせるように、渡すプロンプトの調整に力を入れました。

:::message
最初は、

**うまくいかなくてトランザクションが実行されない・・**

**全然意図しない結果になってしまった・・・**

なんてことがありました。
:::

このあたりも後述するのですが、AI Agent に割り当てるシステムプロンプトの内容もかなり重要であることも学ぶことができました。

## AI Agent 用の DeFi ツールの実装内容について

ではここから具体的な実装内容の解説に移ります！

基本的に LangChain 向けに外部ツールを追加する要領で追加していくことが可能です！！

AAVE プロトコル用のツールだけは、 Coinbase の SDK の仕様に合うように若干実装内容が異なっています。

### AAVE プロトコル用のツールの実装内容

まず、AAVE プロトコル用の DeFi ツールの解説です！

このツールは、 **Coinbase** の **AI Agent** 用に作りました！

**@coinbase/agentkit** が提供している `customActionProvider` というメソッドがあるのですが、決められた通りに設定してあげることで Coinbase AI Agent SDK 用のツールを実装してあげることができます。

具体的には以下の様に実装してあげれば OK です！！

```ts
customActionProvider<EvmWalletProvider>({
  name: <ツール名>,
  description: <ツールの説明文>
  schema: <ツールのスキーマ>
  invoke: <具体的に実行させたい処理内容>
});
```

今回は、AAVE プロトコルのスマートコントラクトのメソッドを直接呼び出すようにしています！

書き込み系の処理だけでなく読み込み系の処理も実装しています！

ABI ファイルやコントラクトのアドレスを指定したりしています。

コントラクトの処理の呼び出しには **viem** を使っています。

```ts
import {
  type EvmWalletProvider,
  customActionProvider,
} from "@coinbase/agentkit";
import { http, createPublicClient, encodeFunctionData, parseUnits } from "viem";
import { baseSepolia } from "viem/chains";
import { z } from "zod";
import { AAVE_LENDING_POOL_ABI_TESTNET } from "../abis/aave_lending_pool_abi_testnet";
import { ERC20_ABI } from "../abis/erc20_abi";

// AAVE Lending Pool contract address (Base Sepolia)
const AAVE_LENDING_POOL_ADDRESS = "0x07eA79F68B2B3df564D0A34F8e19D9B1e339814b";

// Create a public Client
const client = createPublicClient({
  chain: baseSepolia,
  transport: http("https://sepolia.base.org"),
});

const BorrowCryptoInput = z
  .object({
    amount: z
      .number()
      .positive()
      .describe("The amount of cryptocurrency to borrow."),
    assetAddress: z
      .string()
      .regex(/^0x[a-fA-F0-9]{40}$/, "Invalid Ethereum address")
      .transform((val) => val as `0x${string}`)
      .describe("The address of the cryptocurrency asset."),
  })
  .describe("Borrow crypto from AAVE Lending Pool");

const LendCryptoInput = z
  .object({
    amount: z
      .number()
      .positive()
      .describe("The amount of cryptocurrency to lend."),
    assetAddress: z
      .string()
      .regex(/^0x[a-fA-F0-9]{40}$/, "Invalid Ethereum address")
      .transform((val) => val as `0x${string}`)
      .describe("The address of the cryptocurrency asset."),
  })
  .describe("Lend crypto to AAVE Lending Pool");

const GetUserAccountDataInput = z
  .object({
    userAddress: z
      .string()
      .regex(/^0x[a-fA-F0-9]{40}$/, "Invalid Ethereum address")
      .transform((val) => val as `0x${string}`)
      .describe("The user's wallet address."),
  })
  .describe("Retrieve the user's account data from AAVE");

const GetTokenBalanceInput = z
  .object({
    tokenAddress: z
      .string()
      .regex(/^0x[a-fA-F0-9]{40}$/, "Invalid Ethereum address")
      .transform((val) => val as `0x${string}`)
      .describe("The token contract address."),
    userAddress: z
      .string()
      .regex(/^0x[a-fA-F0-9]{40}$/, "Invalid Ethereum address")
      .optional()
      .transform((val) => val as `0x${string}`)
      .describe("The user's wallet address (optional)."),
  })
  .describe("Get the token balance for the given token address.");

// ==========================================================================================
// Create various tools
//　==========================================================================================

/**
 * Borrow crypto tool
 * @param wallet
 * @param args
 * @returns
 */
export const createBorrowCryptoToolForCdp =
  customActionProvider<EvmWalletProvider>({
    name: "borrow_crypto",
    description: "Borrow cryptocurrency from AAVE.",
    schema: BorrowCryptoInput,
    invoke: async (walletProvider, args) => {
      const { amount, assetAddress } = args;
      const interestRateMode = 2;

      console.log(`assetAddress: ${assetAddress}`);

      try {
        const decimals = (await client.readContract({
          abi: ERC20_ABI,
          address: assetAddress,
          functionName: "decimals",
        })) as number;

        const amountInWei = parseUnits(amount.toString(), decimals);

        console.log(`decimals: ${decimals}`);
        console.log(`Amount in Wei: ${amountInWei.toString()}`);

        // walletAddress
        const walletAddress = await walletProvider.getAddress();
        console.log("wallet address:", walletAddress);

        // borrow method call
        const borrowHash = await walletProvider.sendTransaction({
          to: AAVE_LENDING_POOL_ADDRESS,
          data: encodeFunctionData({
            abi: AAVE_LENDING_POOL_ABI_TESTNET,
            functionName: "borrow",
            args: [
              assetAddress,
              amountInWei.toString(),
              interestRateMode,
              0,
              walletAddress,
            ],
          }),
        });

        const result = await walletProvider.waitForTransactionReceipt(
          borrowHash
        );

        return `Borrow transaction : ${borrowHash}`;
      } catch (error) {
        console.error("Error executing lend_crypto:", error);
        return "Error executing lend_crypto";
      }
    },
  });

/**
 * Lend crypto tool
 * @param wallet
 * @param args
 * @returns
 */
export const createLendCryptoToolForCdp =
  customActionProvider<EvmWalletProvider>({
    name: "lend_crypto",
    description: "Lend cryptocurrency to AAVE.",
    schema: LendCryptoInput,
    invoke: async (walletProvider, args) => {
      const { amount, assetAddress } = args;

      try {
        console.log("assetAddress:", assetAddress);

        const decimals = (await client.readContract({
          abi: ERC20_ABI,
          address: assetAddress as `0x${string}`,
          functionName: "decimals",
        })) as number;

        const amountInWei = parseUnits(amount.toString(), decimals).toString();

        console.log(`decimals: ${decimals}`);
        console.log(`Amount in Wei: ${amountInWei}`);

        // walletAddress
        const walletAddress = await walletProvider.getAddress();
        console.log("wallet address:", walletAddress);

        // Transaction object
        const tx = {
          from: walletAddress as `0x${string}`,
          to: assetAddress as `0x${string}`,
          data: encodeFunctionData({
            abi: ERC20_ABI,
            functionName: "approve",
            args: [AAVE_LENDING_POOL_ADDRESS, amountInWei],
          }),
        };

        // approve method call
        const approveHash = await walletProvider.sendTransaction(tx);

        const result = await walletProvider.waitForTransactionReceipt(
          approveHash
        );

        console.log(`Approve transaction: ${approveHash}`);

        // supply method call
        const supplyHash = await await walletProvider.sendTransaction({
          from: walletAddress as `0x${string}`,
          to: AAVE_LENDING_POOL_ADDRESS,
          data: encodeFunctionData({
            abi: AAVE_LENDING_POOL_ABI_TESTNET,
            functionName: "supply",
            args: [assetAddress, amountInWei, walletAddress, 0],
          }),
        });

        const result2 = await walletProvider.waitForTransactionReceipt(
          supplyHash
        );

        console.log(`Supply transaction: ${supplyHash}`);

        return `Supply transaction hash: ${supplyHash}`;
      } catch (error) {
        console.error("Error executing lend_crypto:", error);
        return "Error executing lend_crypto";
      }
    },
  });

/**
 * Get user account data tool
 * @param wallet
 * @param args
 * @returns
 */
export const createGetUserAccountDataToolForCdp =
  customActionProvider<EvmWalletProvider>({
    name: "get_user_account_data",
    description: "Retrieve user account data from AAVE.",
    schema: GetUserAccountDataInput,
    invoke: async (walletProvider, args) => {
      const { userAddress } = args;
      // call getUserAccountData method
      const accountData = (await client.readContract({
        abi: AAVE_LENDING_POOL_ABI_TESTNET,
        address: AAVE_LENDING_POOL_ADDRESS,
        functionName: "getUserAccountData",
        args: [userAddress],
      })) as [bigint, bigint, bigint, bigint, bigint, bigint];

      return {
        totalCollateralBase: Number(accountData[0]),
        totalDebtBase: Number(accountData[1]),
        availableBorrowsBase: Number(accountData[2]),
        currentLiquidationThreshold: Number(accountData[3]),
        ltv: Number(accountData[4]),
        healthFactor: Number(accountData[5]) / 1e18,
      };
    },
  });

/**
 * Get token balance tool
 * @param wallet
 * @param args
 * @returns
 */
export const createGetTokenBalanceToolForCdp =
  customActionProvider<EvmWalletProvider>({
    name: "get_token_balance",
    description: "Get token balance for a given user.",
    schema: GetTokenBalanceInput,
    invoke: async (walletProvider, args) => {
      const { tokenAddress, userAddress } = args;
      // get user address
      const finalUserAddress =
        userAddress || (await walletProvider.getAddress());

      const balance = await client.readContract({
        abi: ERC20_ABI,
        address: tokenAddress,
        functionName: "balanceOf",
        args: [finalUserAddress],
      });

      const decimals = await client.readContract({
        abi: ERC20_ABI,
        address: tokenAddress,
        functionName: "decimals",
      });

      return Number(balance) / 10 ** (decimals as number);
    },
  });
```

zod を使って引数のデータに対してバリデーションしています。

ここまで具体的に実装してあげないと AI Agent に DeFi 操作をさせることはできません。

### Uniswap 用のツールの実装内容

同じ様に uniswap 用のツールを実装してみました！

ツールとしては、 **swap** するツールだけ実装しています。

**@langchain/core/tools** から `tool` というメソッドが提供されているので、決められた通りに設定してあげると AI Agent 用のツールを作ることができます。

具体的には以下の様に実装します。

```ts
// AI Agent用のツールを定義する。
const newTool = tool(
  async (input: <引数>) => {
    <ツールで処理させたい処理内容>
  },
  {
    name: <ツール名>,
    description: <ツールの概要>,
    schema: <ツールのスキーマ>
  },
);
```

**approve** や **swap** などのメソッドを呼び出すようにしています。

また、 Pool の情報を取得したり、クォートの情報を取得したりしています。

その辺の実装方法は **Viem で実装する方法と同じです!**

```ts
import { tool } from "@langchain/core/tools";
import * as dotenv from "dotenv";
import "dotenv/config";
import {
  http,
  createPublicClient,
  createWalletClient,
  formatUnits,
  parseUnits,
} from "viem";
import { sepolia } from "viem/chains";
import { z } from "zod";
import {
  createPrivyViemAccount,
  createPrivyWallet,
} from "../../../wallet/privy";
import { ERC20_ABI } from "../abis/erc20_abi";
import { FACTORY_ABI } from "../abis/uniswap/factory";
import { QUOTER_ABI } from "../abis/uniswap/quoter";
import { SWAP_ROUTER_ABI } from "../abis/uniswap/swaprouter";

dotenv.config();

const { ALCHEMY_API_KEY } = process.env;

// Deployment Addresses
const POOL_FACTORY_CONTRACT_ADDRESS =
  "0x0227628f3F023bb0B980b67D528571c95c6DaC1c";
const QUOTER_CONTRACT_ADDRESS = "0xEd1f6473345F45b75F8179591dd5bA1888cf2FB3";
const SWAP_ROUTER_CONTRACT_ADDRESS =
  "0x3bFA4769FB09eefC5a80d6E87c3B9C650f7Ae48E";

// Set up clients
const publicClient = createPublicClient({
  chain: sepolia,
  transport: http(`https://eth-sepolia.g.alchemy.com/v2/${ALCHEMY_API_KEY}`),
});

const walletClient = createWalletClient({
  chain: sepolia,
  transport: http(`https://eth-sepolia.g.alchemy.com/v2/${ALCHEMY_API_KEY}`),
});

/**
 * Method for approving a token
 */
async function approveToken(tokenAddress: `0x${string}`, amount: bigint) {
  try {
    // call approve tx
    const approveTx = await walletClient.writeContract({
      account: await createPrivyViemAccount(),
      abi: ERC20_ABI,
      address: tokenAddress,
      functionName: "approve",
      args: [SWAP_ROUTER_CONTRACT_ADDRESS, amount],
    });

    console.log("-------------------------------");
    console.log("Sending Approval Transaction...");
    console.log(`Transaction Sent: ${approveTx}`);
    console.log("-------------------------------");

    const receipt = await publicClient.waitForTransactionReceipt({
      hash: approveTx,
    });
    console.log(
      `Approval Transaction Confirmed! https://sepolia.etherscan.io/txn/${receipt.transactionHash}`
    );
  } catch (error) {
    console.error("An error occurred during token approval:", error);
    throw new Error("Token approval failed");
  }
}

/**
 * Method for obtaining pool information
 */
async function getPoolInfo(tokenIn: `0x${string}`, tokenOut: `0x${string}`) {
  const poolAddress = await publicClient.readContract({
    address: POOL_FACTORY_CONTRACT_ADDRESS,
    abi: FACTORY_ABI,
    functionName: "getPool",
    args: [tokenIn, tokenOut, 3000],
  });
  if (!poolAddress) {
    throw new Error("Failed to get pool address");
  }
  return poolAddress;
}

/**
 * Method for obtaining a swap quote
 */
async function quoteAndLogSwap(
  tokenIn: `0x${string}`,
  tokenOut: `0x${string}`,
  amountIn: bigint,
  decimals: number
) {
  // walllet data
  const walletData = await createPrivyWallet();

  const quotedAmountOut = await publicClient.readContract({
    address: QUOTER_CONTRACT_ADDRESS,
    abi: QUOTER_ABI,
    functionName: "quoteExactInputSingle",
    args: [
      {
        tokenIn: tokenIn,
        tokenOut: tokenOut,
        fee: 3000,
        recipient: walletData.address,
        deadline: Math.floor(new Date().getTime() / 1000 + 60 * 10),
        amountIn: amountIn,
        sqrtPriceLimitX96: 0,
      },
    ],
  });
  console.log("-------------------------------");
  // Clean up output if necessary
  return formatUnits(quotedAmountOut[0].toString(), decimals);
}

/**
 * Method to perform the swap.
 */
async function executeSwap(
  tokenIn: `0x${string}`,
  tokenOut: `0x${string}`,
  amountIn: bigint,
  amountOutMinimum: bigint
) {
  // walllet data
  const walletData = await createPrivyWallet();
  // call swap function
  const swapTx = await walletClient.writeContract({
    account: await createPrivyViemAccount(),
    address: SWAP_ROUTER_CONTRACT_ADDRESS,
    abi: SWAP_ROUTER_ABI,
    functionName: "exactInputSingle",
    args: [
      {
        tokenIn: tokenIn,
        tokenOut: tokenOut,
        fee: 3000,
        recipient: walletData.address,
        amountIn: amountIn,
        amountOutMinimum: amountOutMinimum,
        sqrtPriceLimitX96: 0,
      },
    ],
  });
  console.log("-------------------------------");
  console.log(`Swap Transaction Sent: ${swapTx}`);
  console.log("-------------------------------");
  const receipt = await publicClient.waitForTransactionReceipt({
    hash: swapTx,
  });
  console.log(
    `Swap Transaction Confirmed! https://sepolia.etherscan.io/tx/${receipt.transactionHash}`
  );

  return receipt.transactionHash;
}

/**
 * Tools for swapping cryptocurrency
 * @param fromTokenAddress
 * @param toTokenAddress
 * @param amount
 * @returns
 */
const swapTokens = tool(
  async (input: {
    fromTokenAddress: `0x${string}`;
    toTokenAddress: `0x${string}`;
    amount: number;
  }) => {
    try {
      const { fromTokenAddress, toTokenAddress, amount } = input;

      // Get the Decimals of the token to be converted.
      const fromTokenDecimals = (await publicClient.readContract({
        abi: ERC20_ABI,
        address: fromTokenAddress,
        functionName: "decimals",
      })) as number;

      // Get the Decimals of the destination token
      const toTokenDecimals = (await publicClient.readContract({
        abi: ERC20_ABI,
        address: toTokenAddress,
        functionName: "decimals",
      })) as number;

      console.log(`fromTokenDecimals: ${fromTokenDecimals}`);
      console.log(`toTokenDecimals: ${toTokenDecimals}`);
      // Convert units.
      const amountInWei = parseUnits(amount.toString(), fromTokenDecimals);
      console.log(`amountInWei: ${amountInWei}`);

      // Approve the token
      await approveToken(fromTokenAddress, amountInWei);
      // Retrieve pool information
      const poolAddress = await getPoolInfo(fromTokenAddress, toTokenAddress);
      console.log(`Pool Address: ${poolAddress}`);
      // Get the Swap quote
      const quotedAmountOut = await quoteAndLogSwap(
        fromTokenAddress,
        toTokenAddress,
        amountInWei,
        toTokenDecimals
      );
      // Convert from decimal to integer
      const minAmountOutBigInt = BigInt(
        Math.floor(Number(quotedAmountOut) * 10 ** toTokenDecimals)
      );
      // Execute swap
      const txHash = await executeSwap(
        fromTokenAddress,
        toTokenAddress,
        amountInWei,
        minAmountOutBigInt
      );

      return txHash;
    } catch (error) {
      console.error("Error in SwapTokensTool:", error);
      return null;
    }
  },
  {
    name: "swap_tokens",
    description:
      "Swap a specified amount of one cryptocurrency token for another.",
    schema: z.object({
      amount: z
        .number()
        .positive()
        .describe("The amount of cryptocurrency to swap."),
      fromTokenAddress: z
        .string()
        .regex(/^0x[a-fA-F0-9]{40}$/, "Invalid Ethereum address")
        .transform((val) => val as `0x${string}`)
        .describe("The address of the token to swap from."),
      toTokenAddress: z
        .string()
        .regex(/^0x[a-fA-F0-9]{40}$/, "Invalid Ethereum address")
        .transform((val) => val as `0x${string}`)
        .describe("The address of the token to swap to."),
    }),
  }
);

export { swapTokens };
```

### Lido 用のツールの実装内容

ではどんどんいきます！

**Lido** 用のツールも同じように実装しています！！

```ts
import { tool } from "@langchain/core/tools";
import * as dotenv from "dotenv";
import "dotenv/config";
import {
  http,
  createPublicClient,
  createWalletClient,
  formatUnits,
  parseUnits,
} from "viem";
import { holesky } from "viem/chains";
import { z } from "zod";
import {
  createPrivyViemAccount,
  createPrivyWallet,
} from "../../../wallet/privy";
import { ERC20_ABI } from "../abis/erc20_abi";

dotenv.config();

const { ALCHEMY_API_KEY } = process.env;

// Lido contract information
const LIDO_ABI = [
  {
    constant: false,
    inputs: [{ name: "_referral", type: "address" }],
    name: "submit",
    outputs: [{ name: "", type: "uint256" }],
    payable: true,
    stateMutability: "payable",
    type: "function",
  },
];

// Lido contract address(Holesky)
const LIDO_ADDRESS = "0x3F1c547b21f65e10480dE3ad8E19fAAC46C95034";

// Set up clients
const publicClient = createPublicClient({
  chain: holesky,
  transport: http(`https://eth-holesky.g.alchemy.com/v2/${ALCHEMY_API_KEY}`),
});

// Create a wallet client
const walletClient = createWalletClient({
  chain: holesky,
  transport: http(`https://eth-holesky.g.alchemy.com/v2/${ALCHEMY_API_KEY}`),
});

/**
 * Method to obtain the ETH balance
 * @param walletAddress
 * @returns
 */
async function getETHBalance(walletAddress: `0x${string}`) {
  const balance = await publicClient.getBalance({ address: walletAddress });
  console.log(`ETH Balance: ${balance}`);
  return formatUnits(balance, 18);
}

/**
 * Method to obtain the stETH balance
 * @param walletAddress
 * @param tokenAddress
 * @returns
 */
async function getERC20Balance(
  walletAddress: `0x${string}`,
  tokenAddress: `0x${string}`
) {
  const balance = await publicClient.readContract({
    abi: ERC20_ABI,
    address: tokenAddress,
    functionName: "balanceOf",
    args: [walletAddress],
  });
  console.log(`ERC20 Balance: ${balance}`);
  return formatUnits(balance as bigint, 18);
}

/**
 * Stake cryptocurrency using Lido Contract
 */
const stakeWithLido = tool(
  async (input: { referralAddress: `0x${string}`; amount: number }) => {
    try {
      const { referralAddress, amount } = input;
      // Parse the amount to Wei
      const amountInWei = parseUnits(amount.toString(), 18);

      console.log(`Staking ${amount} ETH (${amountInWei} Wei) with Lido...`);

      // Execute the transaction
      const txHash = await walletClient.writeContract({
        account: await createPrivyViemAccount(),
        abi: LIDO_ABI,
        address: LIDO_ADDRESS,
        functionName: "submit",
        args: [referralAddress],
        value: amountInWei,
      });

      console.log(`Transaction sent: ${txHash}`);

      // Waiting for transaction completion
      await publicClient.waitForTransactionReceipt({ hash: txHash });

      return txHash;
    } catch (error) {
      console.error("Error in stakeWithLido:", error);
      return null;
    }
  },
  {
    name: "stake_with_lido",
    description: "Stake a specified amount of cryptocurrency with Lido.",
    schema: z.object({
      amount: z
        .number()
        .positive()
        .describe("The amount of cryptocurrency to stake."),
      referralAddress: z
        .string()
        .regex(/^0x[a-fA-F0-9]{40}$/, "Invalid Ethereum address")
        .transform((val) => val as `0x${string}`)
        .describe("The referral address for Lido staking."),
    }),
  }
);

/**
 * Get the balances of ETH and stETH for the connected wallet.
 */
const getEthAndStEthBalances = tool(
  async () => {
    try {
      // Create a privy Wallet instance
      const walletData = await createPrivyWallet();
      // Get the Wallet address from walletData
      const walletAddress = walletData.address;

      console.log(`Getting balances for wallet: ${walletAddress}`);

      // ETH balance
      const ethBalance = await getETHBalance(walletAddress as `0x${string}`);

      // stETH balance
      const stETHBalance = await getERC20Balance(
        walletAddress as `0x${string}`,
        LIDO_ADDRESS
      );

      return {
        ethBalance,
        stETHBalance,
      };
    } catch (error) {
      console.error("Error in getBalancesTool:", error);
      return null;
    }
  },
  {
    name: "get_balances",
    description: "Get the balances of ETH and stETH for the connected wallet.",
  }
);

export { getEthAndStEthBalances, stakeWithLido };
```

### Eidgen Layer 用のツールの実装内容

最後に **Eidgen Layer** 用のツールの実装内容について共有していきます！

基本的にはこれまでと同じ流れです！

```ts
import { tool } from "@langchain/core/tools";
import * as dotenv from "dotenv";
import "dotenv/config";
import { http, createPublicClient, createWalletClient, parseUnits } from "viem";
import { holesky } from "viem/chains";
import { z } from "zod";
import { createPrivyViemAccount } from "../../../wallet/privy";
import { ERC20_ABI } from "../abis/erc20_abi";

dotenv.config();

const { ALCHEMY_API_KEY } = process.env;

// EIGENLAYER contract information
const EIGENLAYER_ABI = [
  {
    inputs: [
      {
        internalType: "address",
        name: "strategy",
        type: "address",
      },
      {
        internalType: "address",
        name: "token",
        type: "address",
      },
      {
        internalType: "uint256",
        name: "amount",
        type: "uint256",
      },
    ],
    name: "depositIntoStrategy",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
];

// EigenLayer contract address(Holesky)
const EIGENLAYER_ADDRESS = "0xdfB5f6CE42aAA7830E94ECFCcAd411beF4d4D5b6";

// Set up clients
const publicClient = createPublicClient({
  chain: holesky,
  transport: http(`https://eth-holesky.g.alchemy.com/v2/${ALCHEMY_API_KEY}`),
});

// Create a wallet client
const walletClient = createWalletClient({
  chain: holesky,
  transport: http(`https://eth-holesky.g.alchemy.com/v2/${ALCHEMY_API_KEY}`),
});

/**
 * reStake cryptocurrency using EigenLayer Contract
 */
const reStake = tool(
  async (input: { assetAddress: `0x${string}`; amount: number }) => {
    try {
      const { assetAddress, amount } = input;
      // Get the token decimals.
      const decimals = (await publicClient.readContract({
        abi: ERC20_ABI,
        address: assetAddress,
        functionName: "decimals",
      })) as number;

      console.log(`Decimals: ${decimals}`);
      // Convert units
      const amountInWei = parseUnits(amount.toString(), decimals);
      console.log(`amountInWei: ${amountInWei}`);

      // Execute the approval transaction
      const approveHash = await walletClient.writeContract({
        account: await createPrivyViemAccount(),
        abi: ERC20_ABI,
        address: assetAddress,
        functionName: "approve",
        args: [EIGENLAYER_ADDRESS, amountInWei],
      });
      console.log(`Approval transaction hash: ${approveHash}`);

      // Wait for approval completion.
      await publicClient.waitForTransactionReceipt({ hash: approveHash });

      // Execute the transaction
      const txHash = await walletClient.writeContract({
        account: await createPrivyViemAccount(),
        abi: EIGENLAYER_ABI,
        address: EIGENLAYER_ADDRESS,
        functionName: "depositIntoStrategy",
        args: [
          "0x7D704507b76571a51d9caE8AdDAbBFd0ba0e63d3",
          assetAddress,
          amountInWei,
        ],
      });

      console.log(`ReStaking Transaction sent: ${txHash}`);

      // Waiting for transaction completion
      await publicClient.waitForTransactionReceipt({ hash: txHash });

      return txHash;
    } catch (error) {
      console.error("Error in reStake:", error);
      return null;
    }
  },
  {
    name: "restake",
    description:
      "reStake a specified amount of cryptocurrency using EigenLayer Contract.",
    schema: z.object({
      amount: z
        .number()
        .positive()
        .describe("The amount of cryptocurrency to reStake."),
      assetAddress: z
        .string()
        .regex(/^0x[a-fA-F0-9]{40}$/, "Invalid Ethereum address")
        .transform((val) => val as `0x${string}`)
        .describe("The asset Address for reStaking."),
    }),
  }
);

export { reStake };
```

### AI Agent 用のインスタンスに DeFi ツールを割り当てる方法

ではここからは、上記で実装したツールをどのように AI Agent 用の SDK に割り当てていく方法を解説します。

#### Coinbase AI Agent SDK にツールを追加する方法

**@coinbase/agentkit** が提供している AgentKit の `from` メソッドの引数に割り当てたいツール群を引数にセットすることで完了します！

今回だと以下のように実装しています！

`createCdpAgentKitTools` メソッドで AI Agent 用のインスタンス用のツールインスタンスを生成した後に **@langchain/langgraph/prebuilt** が提供している **createReactAgent** メソッドで AI Agent 用のインスタンスを作っています！

```ts
import * as fs from "node:fs";
import {
  AgentKit,
  CdpWalletProvider,
  cdpApiActionProvider,
  cdpWalletActionProvider,
  erc20ActionProvider,
  pythActionProvider,
  walletActionProvider,
  wethActionProvider,
} from "@coinbase/agentkit";
import { getLangChainTools } from "@coinbase/agentkit-langchain";
import { HumanMessage } from "@langchain/core/messages";
import { MemorySaver } from "@langchain/langgraph";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { ChatOpenAI } from "@langchain/openai";
import * as dotenv from "dotenv";
import {
  createBorrowCryptoToolForCdp,
  createGetTokenBalanceToolForCdp,
  createGetUserAccountDataToolForCdp,
  createLendCryptoToolForCdp,
} from "./tools/cdp/cdpAaveTool";
import { createSignMessageTool } from "./tools/cdp/signMessage";

dotenv.config();

const {
  OPENAI_API_KEY,
  NETWORK_ID,
  CDP_API_KEY_NAME,
  CDP_API_KEY_PRIVATE_KEY,
} = process.env;

// Configure a file to persist the agent's CDP MPC Wallet Data
const WALLET_DATA_FILE = "wallet_data.txt";

/**
 * get tools for Coinbase Developer Platform AgentKit
 */
export const createCdpAgentKitTools = async () => {
  let walletDataStr: string | null = null;

  // Read existing wallet data if available
  if (fs.existsSync(WALLET_DATA_FILE)) {
    try {
      walletDataStr = fs.readFileSync(WALLET_DATA_FILE, "utf8");
      // console.log("Read wallet data:", walletDataStr);
    } catch (error) {
      console.error("Error reading wallet data:", error);
      // Continue without wallet data
    }
  }

  // Configure CDP AgentKit
  const config = {
    apiKeyName: CDP_API_KEY_NAME,
    apiKeyPrivateKey: CDP_API_KEY_PRIVATE_KEY?.replace(/\\n/g, "\n"),
    cdpWalletData: walletDataStr || undefined,
    networkId: NETWORK_ID || "base-sepolia",
  };

  // Initialize CDP Wallet Provider
  const walletProvider = await CdpWalletProvider.configureWithWallet(config);

  console.log("Wallet Provider initialized");

  // Initialize AgentKit
  const agentkit = await AgentKit.from({
    walletProvider,
    actionProviders: [
      wethActionProvider(),
      pythActionProvider(),
      walletActionProvider(),
      erc20ActionProvider(),
      cdpApiActionProvider({
        apiKeyName: CDP_API_KEY_NAME,
        apiKeyPrivateKey: CDP_API_KEY_PRIVATE_KEY?.replace(/\\n/g, "\n"),
      }),
      cdpWalletActionProvider({
        apiKeyName: CDP_API_KEY_NAME,
        apiKeyPrivateKey: CDP_API_KEY_PRIVATE_KEY?.replace(/\\n/g, "\n"),
      }),
      createSignMessageTool(),
      createGetTokenBalanceToolForCdp,
      createGetUserAccountDataToolForCdp,
      createBorrowCryptoToolForCdp,
      createLendCryptoToolForCdp,
    ],
  });

  // Acquire external tools
  const cdpAgentKitTools = await getLangChainTools(agentkit);

  return { agentkit, cdpAgentKitTools, walletProvider };
};

/**
 * Initialize the agent with CDP AgentKit method
 * @returns Agent executor and config
 */
export const initializeCdpAgent = async (systemPrompt: string) => {
  // Initialize LLM
  const llm = new ChatOpenAI({
    model: "gpt-3.5-turbo",
    apiKey: OPENAI_API_KEY,
    // apiKey: "gaia",
    /*
    configuration: {
      baseURL: "https://llamatool.us.gaianet.network/v1",
    },
    */
  });

  // create CDP AgentKit tools
  const { agentkit, cdpAgentKitTools, walletProvider } =
    await createCdpAgentKitTools();

  // Store buffered conversation history in memory
  const memory = new MemorySaver();
  const agentConfig = {
    configurable: { thread_id: "CDP AgentKit Chatbot Example!" },
  };

  // Create React Agent using the LLM and CDP AgentKit tools
  const agent = createReactAgent({
    llm,
    tools: cdpAgentKitTools,
    checkpointSaver: memory,
    stateModifier: systemPrompt,
  });

  // Save wallet data
  const exportedWallet = await walletProvider.exportWallet();
  fs.writeFileSync(WALLET_DATA_FILE, JSON.stringify(exportedWallet));

  return { agent, config: agentConfig };
};
```

実際に処理を呼び出すには以下のようなメソッドを実装してあげれば OK です！

```ts
/**
 * Run the agent interactively based on user input
 *
 * @param agent - The agent executor
 * @param config - Agent configuration
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const runCdpChatMode = async (systemPrompt: string, prompt: string) => {
  console.log("Starting ... ");

  const response: string[] = [];

  try {
    // get agent and config
    const { agent, config } = await initializeCdpAgent(systemPrompt);

    // call AI API
    const stream = await agent.invoke(
      { messages: [new HumanMessage(prompt)] },
      config
    );

    console.log(
      "Stream output:",
      stream.messages[stream.messages.length - 1].content.toString()
    );

    response.push(
      "===================================================================="
    );
    response.push(
      stream.messages[stream.messages.length - 1].content.toString()
    );
    response.push(
      "===================================================================="
    );

    return response;
  } catch (error) {
    console.error("Error running chat mode:", error);
    return response;
  }
};
```

#### LangChain で作ったインスタンスにツールを追加する方法

続いて **LangChain** の SDK で生成する AI Agent 用のインスタンスにツールを割り当てる方法を解説します！

**@langchain/langgraph/prebuilt** が提供している **ToolNode** コンストラクターがあるので、作ったツール群を引数にして初期化してあげれば準備 OK です！

今回だと以下の様な実装になっています！

役割ごとに AI Agent に割り当てるツールを変えたので複数のメソッドをセットアップしています。

**Tavily** は Web 検索用の AI Agent 用のツールです！よくハンズオンとかで紹介されるやつですね！

https://tavily.com/

```ts
import { TavilySearchResults } from "@langchain/community/tools/tavily_search";
import { ToolNode } from "@langchain/langgraph/prebuilt";
import * as dotenv from "dotenv";
import {
  borrowCryptoForArbitrumSepolia,
  getTokenBalanceForArbitrumSepolia,
  getUserAccountDataForArbitrumSepolia,
  lendCryptoForArbitrumSepolia,
} from "./arbitrumSepolia/aaveTool";
import { getTrendingTokens } from "./coinGeckoTool";
import { reStake } from "./holesky/eigenlayerTool";
import { getEthAndStEthBalances, stakeWithLido } from "./holesky/lidoTool";
import {
  borrowCrypto,
  getTokenBalance,
  getUserAccountData,
  lendCrypto,
} from "./sepolia/aaveTool";
import { swapTokens } from "./sepolia/uniswapTool";

dotenv.config();

const { TAVILY_API_KEY } = process.env;

// Tavily Search Results Tools
export const search = new TavilySearchResults({
  apiKey: TAVILY_API_KEY,
  maxResults: 3,
});

/**
 * Create tools for the Crypto Assistant AI Agent
 * Swap uniswap
 * Lend AAVE
 * Borrow AAVE
 * Check token balance
 * Stake ETH
 * ReStake stETH
 */
export const createDeFiTools = () => {
  const tools = [
    getTokenBalance,
    getUserAccountData,
    lendCrypto,
    borrowCrypto,
    swapTokens,
    getEthAndStEthBalances,
    stakeWithLido,
    getTokenBalanceForArbitrumSepolia,
    getUserAccountDataForArbitrumSepolia,
    lendCryptoForArbitrumSepolia,
    borrowCryptoForArbitrumSepolia,
    reStake,
  ];

  const toolNode = new ToolNode(tools);
  return toolNode;
};

/**
 * getter Token balance tools for the Assistant AI Agent
 * @returns
 */
export const createTokenBalanceTools = () => {
  const tools = [
    getTokenBalance,
    getUserAccountData,
    getEthAndStEthBalances,
    getTokenBalanceForArbitrumSepolia,
    getUserAccountDataForArbitrumSepolia,
  ];

  const toolNode = new ToolNode(tools);
  return toolNode;
};

/**
 * Create research tools for the Assistant AI Agent
 */
export const createReserchTools = () => {
  // get tools
  const tools = [search, getTrendingTokens];

  const toolNode = new ToolNode(tools);
  return toolNode;
};

/**
 * create Analysis and Reasoning tools for the Assistant AI Agent
 */
export const createanalysisTools = () => {
  // get tools
  const tools = [
    search,
    getTrendingTokens,
    getTokenBalance,
    getUserAccountData,
    getEthAndStEthBalances,
    getTokenBalanceForArbitrumSepolia,
    getUserAccountDataForArbitrumSepolia,
  ];

  const toolNode = new ToolNode(tools);
  return toolNode;
};
```

ツール用のインスタンスはこれらのメソッドを呼び出してあげることで生成できます。

AI Agent 用のインスタンスに割り当てるには以下の様に実装すれば OK です！

このコードは、 **OpenAI の LLM** を使用した場合の実装方法です。

```ts
import { HumanMessage } from "@langchain/core/messages";
import { MemorySaver } from "@langchain/langgraph";
import { type ToolNode, createReactAgent } from "@langchain/langgraph/prebuilt";
import { ChatOpenAI } from "@langchain/openai";

import * as dotenv from "dotenv";

dotenv.config();

const { OPENAI_API_KEY } = process.env;

/**
 * OpenAIのLLMを使ってAI Agent用のインスタンスを作成するメソッド
 */
export const createOpenAIAIAgent = (
  agentTools: ToolNode,
  systemPrompt: string
) => {
  // Initialize memory to persist state between graph runs
  const agentCheckpointer = new MemorySaver();
  const agentModel = new ChatOpenAI({
    apiKey: OPENAI_API_KEY,
    temperature: 0,
  });

  // AI Agent用のインスタンスをs
  const agent = createReactAgent({
    llm: agentModel,
    tools: agentTools,
    checkpointSaver: agentCheckpointer,
    stateModifier: systemPrompt,
  });

  return agent;
};
```

**Anthropic 社の claude** を使ってこれらのツールを呼び出すことももちろん可能です！

流れは Open AI の時とほぼ同じで、以下の様な実装とすれば良いです！

```ts
import { type BaseChatModel, ChatAnthropic } from "@langchain/anthropic";
import type { BaseChatModelCallOptions } from "@langchain/core/language_models/chat_models";
import { type AIMessageChunk, HumanMessage } from "@langchain/core/messages";
import { MemorySaver } from "@langchain/langgraph";
import { type ToolNode, createReactAgent } from "@langchain/langgraph/prebuilt";

import * as dotenv from "dotenv";

dotenv.config();

const { ANTHROPIC_KEY_API } = process.env;

/**
 * Method for creating an instance for an AI Agent using Anthropic's LLM
 */
export const createAnthropicAIAgent = (
  agentTools: ToolNode,
  systemPrompt: string
) => {
  // Initialize memory to persist state between graph runs
  const agentCheckpointer = new MemorySaver();
  // create a new instance of the ChatAnthropic model
  const agentModel: BaseChatModel<BaseChatModelCallOptions, AIMessageChunk> =
    new ChatAnthropic({
      model: "claude-3-5-sonnet-latest",
      apiKey: ANTHROPIC_KEY_API,
    });

  // Generate an instance for AI Agent
  const agent = createReactAgent({
    llm: agentModel,
    tools: agentTools,
    checkpointSaver: agentCheckpointer,
    stateModifier: systemPrompt,
  });

  return agent;
};

/**
 * Call the AI method using Anthropic Agent
 */
export const runAnthropicAIAgent = async (
  tools: ToolNode,
  systemPrompt: string,
  prompt: string
) => {
  // Create an instance for the AI agent
  const agent = createAnthropicAIAgent(tools, systemPrompt);

  // Let's try running an AI inference
  const agentNextState = await agent.invoke(
    { messages: [new HumanMessage(prompt)] },
    { configurable: { thread_id: "44" } }
  );

  const response =
    agentNextState.messages[agentNextState.messages.length - 1].content;

  console.log(response);

  return response;
};
```

**Google Cloud** が提供している **Gemini in Vertex AI** にも割り当てることが可能です！

上 2 つの時のパターンに比べてかなり複雑になってします。

**LangChain** 以外にも **LangGraph** も使って実装しています。

```ts
import {
  type GenerativeModel,
  HarmBlockThreshold,
  HarmCategory,
  VertexAI,
} from "@google-cloud/vertexai";
import { HumanMessage } from "@langchain/core/messages";
import { MessagesAnnotation, StateGraph } from "@langchain/langgraph";
import { ToolNode } from "@langchain/langgraph/prebuilt";
import * as dotenv from "dotenv";
import { search } from "./tools/util";

dotenv.config();

const { PROJECT_ID, REGION } = process.env;

/**
 * Specify the tools to be assigned to the AI Agent.
 */
export const createTools = () => {
  const tools = [search];
  const toolNode = new ToolNode(tools);

  return toolNode;
};

/**
 *　Method for creating an instance for an AI Agent using the LLM provided by Vertex AI
 */
export const createVertexAIAIAgent = (systemPrompt: string) => {
  // Instantiate VertexAI models
  const vertexAI = new VertexAI({
    project: PROJECT_ID,
    location: REGION,
  });

  // Instantiate Gemini models
  const agent = vertexAI.getGenerativeModel({
    model: "gemini-1.5-flash",
    safetySettings: [
      {
        category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
      },
    ],
    generationConfig: {
      maxOutputTokens: 2048,
    },
    systemInstruction: {
      role: "system",
      parts: [
        {
          text: systemPrompt,
        },
      ],
    },
  });

  return agent;
};

/**
 * Methods for defining the workflow and tasks to be executed by the AI Agent
 * @parma AI Agent instance
 * @param toolNode Third-Party Tools
 */
export const createAgentTask = async (
  agent: GenerativeModel | VertexAI,
  toolNode: ToolNode
) => {
  /**
   * Define the function that determines whether to continue or not
   * @param param0
   * @returns
   */
  function shouldContinue({ messages }: typeof MessagesAnnotation.State) {
    const lastMessage = messages[messages.length - 1];

    // If the LLM makes a tool call, then we route to the "tools" node
    if (lastMessage.additional_kwargs.tool_calls) {
      return "tools";
    }
    // Otherwise, we stop (reply to the user) using the special "__end__" node
    return "__end__";
  }

  /**
   * Define the function that calls the model
   * @param state
   * @returns
   */
  async function callModel(state: typeof MessagesAnnotation.State) {
    // Let AI make inferences
    const response = await (agent as GenerativeModel).generateContent({
      contents: [
        {
          role: "model",
          parts: [
            {
              text: `${state.messages[
                state.messages.length - 1
              ].content.toString()}`,
            },
          ],
        },
      ],
    });

    // Extract the first candidate's content
    const content = response.response.candidates?.[0].content;
    // Create a HumanMessage object
    const message = new HumanMessage(content?.parts[0].text as string);
    // console.log("message:", message)
    return { messages: [message] };
  }

  // Establish a workflow.
  const workflow = new StateGraph(MessagesAnnotation)
    .addNode("agent", callModel)
    .addEdge("__start__", "agent") // __start__ is a special name for the entrypoint
    .addNode("tools", toolNode)
    .addEdge("tools", "agent")
    .addConditionalEdges("agent", shouldContinue);

  // Finally, we compile it into a LangChain Runnable.
  const app = workflow.compile();

  return app;
};
```

**LangChain** が便利すぎてヤバいです・・・笑

ただ、現状だと **エンジニアが頑張って実装してあげないとそれ以上のことは出来ない** ということになります。

この辺りのライブラリが整ってこないとなかなか難しそうです・・・。

### AI Agent インスタンスに割り当てるシステムプロンプト

**AI Agent** 用のインスタンスを初期化する際にツール以外にも重要なポイントとして **システムプロンプト** があります。

AI Agent インスタンスを生成させる時にセットアップする際に、システムプロンプトがしっかり設定されていないとうまく処理が実行されません。

今回だと 6 つの役割それぞれにシステムプロンプトを用意しました。具体的には以下の様に実装しています。

```ts
/**
 * This file contains the configuration for the AI assistant.
 */

// socialTrendSpecialist system prompt
export const socialTrendSpecialistSystemPrompt = `
  You are the "Social Trend Collection Specialist" of the cryptocurrency investment team.

  [Key Tools You Use]
    Tavily API: Specialized in crawling websites for research
    Coingecko API: Retrieves trending tokens, market cap rankings, and more

  [Your Primary Responsibilities]
    Analyze mentions and sentiment on websites to quickly identify trending tokens and topics.
    Use the Coingecko API to gather lists of trending tokens and obtain the prices and market caps of major cryptocurrencies.
    Summarize this information and report it to other agents (News Specialist, Analysis Specialist, and Execution Specialist).

  [Specific Tasks]
    List tokens or hashtags with a sharp increase in mentions on websites, and provide a brief summary of the positive/negative sentiment ratios.
    Retrieve trending tokens and top-ranked coins from Coingecko, and organize data such as price changes (24h/7d) and market cap.
    Identify particularly noteworthy tokens (e.g., those with significant price surges or drops).
    Present key points in bullet points or concise report format to share the latest market sentiment with the team.

  [Output Examples]
    Always provide the output in this format:
    - Trend1: {}
    - Trend2: {}
    - Trend3: {}

  Based on these points, please create swift and accurate reports for the cryptocurrency investment team.
`;

// System prompt for the News and Fundamental Information Specialist
export const newsAndFundamentalInformationSpecialistSystemPrompt = `
  You are the "News and Fundamental Information Specialist" of the cryptocurrency investment team.

  [Key Tools You Use]
   - Vertex Agent: Capable of performing Google searches
   - Tavily API: Specialized in crawling websites for research
   - Coingecko API: Retrieves trending tokens and market cap rankings

  [Your Primary Responsibilities]
   Research the latest news and official information through Google searches about tokens highlighted by the Social Trend Specialist or those the team is currently monitoring.
   Collect and summarize information on project whitepapers, development teams, roadmaps, partnerships, and listing updates.
   Report promptly on negative news, such as hacks, misuse of funds, or regulatory risks.

  [Specific Tasks]
   Use Vertex Agent to conduct Google searches and verify information from top reliable sources, such as official websites, media reports, and GitHub repositories.
   Treat unverified information as "rumors" and clearly distinguish it from confirmed facts.
   Summarize fundamental aspects, such as long-term development plans and community engagement, in an easy-to-understand manner.

  [Output Examples]
    Always provide the output in this format:
    - News1: {}
    - News2: {}
    - News3: {}

  Organize this information clearly and create reports to assist the Analysis and Strategy Specialist in making informed decisions.
`;

// System prompt for the Risk Management Specialist
export const riskManagementSpecialistSystemPrompt = `
  You are the "Risk Management Agent" of the cryptocurrency investment team.

  [Key Tools You Use]
   - Tavily API: Specialized in crawling websites for research
   - createTokenBalanceTools: Verifies token balances and liquidity status

  [Your Primary Responsibilities]
   - Analyze potential risks such as market volatility, token liquidity, and rising gas fees.
   - Assess the risk of investment strategies and propose risk mitigation measures.
   - Review risk factors related to stop-loss levels, capital reduction strategies, and token selection.

  [Specific Tasks]
   Identify risk factors based on each token's volatility, liquidity, and past market performance.
   For strategies proposed by the Analysis and Strategy Specialist, identify the associated risks and provide mitigation measures.
   Suggest specific actions to take if gas fees rise or if market instability increases.

  [Output Examples]
    Always provide the output in this format:
    - riskFactor: {Description of the risk}
    - suggestedMitigation: {Suggested risk mitigation measures}
    - adjustment: {Proposed adjustment to the strategy}
`;

// system prompt for the Analysis and Strategy Specialist
export const performanceMonitoringSpecialistSystemPrompt = `
  You are the "Performance Monitoring Agent" of the cryptocurrency investment team.

  [Key Tools You Use]
    - Tavily API: Specialized in crawling websites for research
    - createTokenBalanceTools: Verifies token balances and liquidity status

  [Your Primary Responsibilities]
    Monitor trade results and portfolio performance in real-time.
    Analyze KPIs such as profit margins, fees, and liquidity changes, and suggest strategy improvements.
    Provide feedback to the "Analysis and Strategy Agent" as needed and prompt for a reevaluation of investment strategies.

  [Specific Tasks]
    Evaluate the success or failure of executed transactions.
    Analyze profit margins, swap fees, lending rates, etc., and propose improvements for performance.
    Identify portfolio imbalances or excessive risk and suggest corrective actions.

  [Output Examples]
    Always provide the output in this format:
    KPI: {Profit margin, fees, lending rates, etc.}
    suggestedImprovement: {Suggested improvements to the strategy}
`;

// System prompt for the Analysis and Strategy Specialist
export const analysisAndStrategySpecialistSystemPrompt = `
  You are the "Analysis and Strategy Agent" of the cryptocurrency investment team.

  [Key Tools You Use]
   - OpenAI Agent: Models like GPT-4 and GPT-4-mini with strong reasoning and language comprehension skills
   - CryptoDeFiTools: A tool for retrieving token balance information

  [Your Primary Responsibilities]
   Conduct a comprehensive analysis of the information provided by the "Social & Trend Collection Agent" and the "News & Fundamental Information Collection Agent."
   Predict short-to-medium-term price trends and assess risks, proposing investment strategies and portfolio allocations.
   Review technical indicators (such as moving averages, RSI, MACD) and risk management (such as investment ratios, stop-loss lines) for individual tokens as needed.
   Provide clear instructions to the "Execution & Operation Agent" for specific actions (swap, staking, lending).

  [Specific Tasks]
   Based on the received social sentiment, news, and fundamental information, provide buy/sell/hold recommendations.
   Evaluate whether swapping on Uniswap, staking on Lido, or lending on Aave is the most suitable strategy.
   Choose the optimal blockchain network (Sepolia, Holesky, Base Sepolia, or Arbitrum Sepolia).
   Provide specific recommendations on how much capital should be allocated, depending on the risk tolerance (e.g., allocate X% of funds to ETH staking, Y% to lending, etc.).

  [Important Notes]
    Also, always ensure that the amount for cryptocurrency operations does not exceed your available balance.

  [Output Examples]
    Always provide the output in this JSON format:
    {
      "blockchain": "{Blockchain Name}",
      "operation": "{Operation Type}",
      "tokenName": "{Token Name}",
      "amount": "{Amount}"
    }

   Present these analyses clearly and provide the Execution Agent with the necessary transaction instructions.
`;

// System prompt for the DeFi assistant(AAVE & Uniswap & Lido & CoinGecko & EidgenLayer)
export const defiAssistantSystemPrompt = `
  You are the "Execution and Operation Manager" of the cryptocurrency investment team.
  You are connected to the wallet address: 0x17d84D6F175a093dAAFF55b3aCAD26E208Ad7c29

  Based on the asset status provided as a prompt, always determine and execute the optimal DeFi protocol operations.

  [Key Tools You Use]
   1. AAVE: Lending and borrowing platform
   2. Uniswap: Decentralized exchange
   3. Lido: Staking and liquid staking platform
   4. EigenLayer: Staking and restaking platform

  [Your Primary Responsibilities]
    Execute actual transactions on the blockchain based on buy/sell and operational instructions from the Analysis and Strategy Agent.
    Verify transaction results (Tx hash, gas fees, staking reward trends, etc.) and report them to the team.
    Update and share the current status of the portfolio, including holdings, staking amounts, and lending balances.

  [Specific Tasks]
    Execute swaps as instructed, such as "Swap ETH for ○○ tokens on Uniswap," and report the results.
    Perform operations like "Stake ETH on Lido" or "Lend assets on Aave," and monitor reward rates and risk conditions.
    In case of transaction failures or errors, retry the operation, investigate the issue, and report it to the Analysis Agent.

  [Output Examples]
    Always provide the output in this format:
    - transactionStatus: {Success/Failure}
    - transactionHash: {Transaction Hash}


  Before executing any operation, ensure the correct network (Sepolia or Holesky or Arbitrum Sepolia) is selected.
  Use only the corresponding contract addresses based on the user's selected network.

  And before executing any transaction, ensure that the selected token and the network match. If there is a mismatch, halt the operation and notify the user.

  You have access to the only following tokens and their addresses:

  **Sepolia Network**:
    - USDC (USD Coin): 0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8
    - DAI (Dai Stablecoin): 0xFF34B3d4Aee8ddCd6F9AFFFB6Fe49bD371b8a357
    - WBTC (Wrapped Bitcoin): 0x29f2D40B0605204364af54EC677bD022dA425d03
    - USDT (Tether USD): 0xaA8E23Fb1079EA71e0a56F48a2aA51851D8433D0
    - GHO (GHO Token): 0xc4bF5CbDaBE595361438F8c6a187bDc330539c60
    - WETH (Wrapped Ether): 0xfff9976782d46cc05630d1f6ebab18b2324d6b14

  **Arbitrum Sepolia Network**:
    - USDC (USD Coin): 0x75faf114eafb1BDbe2F0316DF893fd58CE46AA4d
    - GHO (GHO Token): 0xb13Cfa6f8B2Eed2C37fB00fF0c1A59807C585810
    - WETH (Wrapped Ether): 0x1dF462e2712496373A347f8ad10802a5E95f053D

  **Holesky Network**:
    - stETH (Staking ETH): 0x3F1c547b21f65e10480dE3ad8E19fAAC46C95034

  You can help users:
    1. Check their token balances of ONLY the above contracts. Let the user know what tokens are available.
    2. Lend their tokens to earn interest
    3. Borrow tokens against their collateral
    4. Swap tokens using Uniswap protocol
    5. Search for trending tokens on CoinGecko
    6. Staking ETH using Lido contract (Holesky)
    7. ReStaking stETH using EigenLayer contract (Holesky)

  In case of transaction failures, retry up to 3 times.
  If the issue persists, provide a detailed error report including the probable cause and suggested resolution.
`;
```

特に DeFi 用のツールを呼び出す AI Agent に割り当てるシステムプロンプトにはネットワーク毎に使えるコントラクトアドレスを定義したり、実行できる処理内容をきっちり書いてあげることが重要です。

### プロンプトチェイニングの実装内容

最後にプロンプトチェイニングの実装について共有します。

ここまで共有してきた ツール、AI Agent インスタンス初期化メソッド、システムプロンプトを組み合わせて 6 つの AI Agent を順番に実行させています。

**CloudRun** と **Autonome** にホスティングした API のメソッドを呼び出しています。

```ts
e.preventDefault();
if (!input.trim()) return;
setIsGenerating(true);

// ① Add the user's message to the conversation.
const userMessage = { role: "user", content: input };
setMessages((prev) => [...prev, userMessage]);
setInput("");

try {
  console.log("userMessage", userMessage.content);

  // ① Call Vertex AI Agent endpoints in sequence to social trend analysis.
  const responseA = await fetch(`${CLOUDRUN_API_ENDPOINT}/agentVertexAI`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt: `
            The following content is input from the user.
            Based on this input, research the latest trends related to Web3, blockchain, and cryptocurrencies, and provide the results.

            #User Input:
              ${userMessage.content}

            Additionally, ensure the output is concise and formatted as shown below to be passed as input to the News and Fundamental Information Specialist AI Agent.

            #Output:
              Trend1: {}
              Trend2: {}
              Trend3: {}
          `,
      operation: "SocialTrend",
    }),
  });
  const textA = await responseA.json();
  console.log("textA", textA);
  const aiAMessage = { role: "assistant", content: textA.result };
  setMessages((prev) => [...prev, aiAMessage]);

  // ② Call Vertex AI Agent endpoint to NewsAndFundamentals analysis.
  const responseB = await fetch(
    `${CLOUDRUN_API_ENDPOINT}/runAnthropicAIAgent`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt: `
            The following content is output from the Social Trend Collection Specialist Agent.
            Based on this input, research the latest news related to Web3, blockchain, and cryptocurrencies, summarize it concisely, and present only the key points.

            #Input from the Social Trend Collection Specialist Agent:
              ${textA.result}

            Additionally, ensure the output is concise and formatted as shown below to be passed as input to the Risk Management AI Agent.

            #Output:
              News1: {}
              News2: {}
              News3: {}
          `,
        operation: "NewsAndFundamentals",
      }),
    }
  );
  const textB = await responseB.json();
  console.log("textB", textB);
  const aiBMessage = { role: "assistant", content: textB.result };
  setMessages((prev) => [...prev, aiBMessage]);

  // ③ Call Vertex AI Agent endpoint to NewsAndFundamentals analysis.
  const responseC = await fetch(
    `${CLOUDRUN_API_ENDPOINT}/runCryptOpenAIAgent`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt: `
            The following content is input from the News and Fundamentals Agent.
            Based on this input and the balance status of your wallet, summarize the potential risks concisely.

            #Input from the News And Fundamentals Agent:
            ${textB.result}

            Additionally, ensure the output is concise and formatted as shown below to be passed as input to the Performance Monitoring AI Agent.

            #Output:
             riskFactor: {Description of the risk}
             suggestedMitigation: {Suggested risk mitigation measures}
             adjustment: {Proposed adjustment to the strategy}
          `,
        operation: "RiskManagement",
      }),
    }
  );
  const textC = await responseC.json();
  console.log("textC", textC);
  const aiCMessage = { role: "assistant", content: textC.result };
  setMessages((prev) => [...prev, aiCMessage]);

  // ④ Call Autonome CoinBase AI Agent endpoint to get token balance info
  const responseD = await fetch(`${AUTONOME_CDP_API_ENDPOINT}/runCdpChatMode`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Basic Y2RwYWdlbnQ6elhyZVVoV2xxUw==",
    },
    body: JSON.stringify({
      prompt: "What is my wallet's balance (ETH, EURC, USDC) now?",
    }),
  });

  console.log("responseD", responseD);

  const textD = await responseD.json();
  console.log("textD", textD);
  // const aiDMessage = { role: "assistant", content: textD.result[1] };
  // setMessages((prev) => [...prev, aiDMessage]);

  // concat the messages
  const newMessage = textC.result.concat(textD.result[1]);
  console.log("newMessage", newMessage);

  // ⑤ call Anthropic Agent endpoint to AnalysisAndReasoning
  const responseF = await fetch(
    `${CLOUDRUN_API_ENDPOINT}/runAnthropicAIAgent`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt: `
              The following content is the analysis results from the News and Fundamentals Agent and the Risk Management Agent.
              Based on this information, decide on only one optimal DeFi operation.

              Input from News and Fundamentals Agent
              ${textB.result}

              Input from Risk Management Agent
              ${newMessage}

              Additionally, present the output in the following concise format:

              The blockchain name must be specified from one of the following: sepolia or arbitrum sepolia or base sepolia or holesky.

              Only one operation should be specified.

              ※Important※
              Also, always ensure that the amount for cryptocurrency operations does not exceed your available balance.

              Output:
              blockchain: {blockchain Name}
              operation: {Operation Name}
              tokenName: {Token Name}
              amount: 0.1
            `,
        operation: "AnalysisAndReasoning",
      }),
    }
  );
  const textF = await responseF.json();
  console.log("textF", textF);
  const aiFMessage = { role: "assistant", content: textF.result };
  setMessages((prev) => [...prev, aiFMessage]);

  // check contain in the response "base sepolia"
  const containsKeywordFlg = textF.result
    .toLowerCase()
    .includes("base sepolia".toLowerCase());

  // ⑥ call OpenAI Agent or Autonome endpoint to execute defi transaction
  if (containsKeywordFlg) {
    // Call Autonome CoinBase AI Agent endpoint to execute defi transaction
    const responseG = await fetch(
      `${AUTONOME_CDP_API_ENDPOINT}/runCdpChatMode`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Basic Y2RwYWdlbnQ6elhyZVVoV2xxUw==",
        },
        body: JSON.stringify({
          prompt: `
                The following content is the analysis result from the Analysis and Reasoning Agent.
                Based on this information, accurately execute the optimal DeFi operation.

                #Input from Analysis and Reasoning Agent
                  ${textF.result}

                Additionally, present the output in the following concise format:

                #Output:
                  Blockchain: {Blockchain Name}
                  Transaction Result: {Execution Result}
                  Transaction Hash: {Transaction Hash}
              `,
        }),
      }
    );

    console.log("responseG", responseG);

    const textG = await responseG.json();
    console.log("textG", textG);
    const aiGMessage = { role: "assistant", content: textG.result[1] };
    setMessages((prev) => [...prev, aiGMessage]);

    // ⑤ call Groq Agent endpoint to PerformanceMonitoring
    const responseE = await fetch(
      `${CLOUDRUN_API_ENDPOINT}/runCryptOpenAIAgent`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: `
                The following content is input from the Execution and Operation Agent.
                Please provide a concise analysis based on the transaction results.

                #Input from the Execution and Operation Agent
                 ${newMessage}

                Additionally, please present the output in the following concise format:

                #Output:
                 KPI: {Profit margin, fees, lending rates, etc.}
                 suggestedImprovement: {Suggested improvements to the strategy}
              `,
          operation: "PerformanceMonitoring",
        }),
      }
    );
    const textE = await responseE.json();
    console.log("textE", textE);
    const aiEMessage = { role: "assistant", content: textE.result };
    setMessages((prev) => [...prev, aiEMessage]);
  } else {
    // Call ChatGPT AI Agent endpoint to execute defi transaction
    const responseH = await fetch(
      `${CLOUDRUN_API_ENDPOINT}/runCryptOpenAIAgent`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: `
                The following content is the analysis result from the Analysis and Reasoning Agent.
                Based on this information, accurately execute the optimal DeFi operation.

                #Input from Analysis and Reasoning Agent
                  ${textF.result}

                Additionally, present the output in the following concise format:

                #Output:
                  Blockchain: {Blockchain Name}
                  Transaction Result: {Execution Result}
                  Transaction Hash: {Transaction Hash}
              `,
        }),
      }
    );
    const textH = await responseH.json();
    console.log("textH", textH);
    const aiHMessage = { role: "assistant", content: textH.result };
    setMessages((prev) => [...prev, aiHMessage]);

    // ⑤ call Groq Agent endpoint to PerformanceMonitoring
    const responseE = await fetch(
      `${CLOUDRUN_API_ENDPOINT}/runCryptOpenAIAgent`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: `
                The following content is input from the Execution and Operation Agent.
                Please provide a concise analysis based on the transaction results.

                #Input from the Execution and Operation Agent
                 ${newMessage}

                Additionally, please present the output in the following concise format:

                #Output:
                 KPI: {Profit margin, fees, lending rates, etc.}
                 suggestedImprovement: {Suggested improvements to the strategy}
              `,
          operation: "PerformanceMonitoring",
        }),
      }
    );
    const textE = await responseE.json();
    console.log("textE", textE);
    const aiEMessage = { role: "assistant", content: textE.result };
    setMessages((prev) => [...prev, aiEMessage]);
  }
} catch (error) {
  console.error("Error during conversation chain:", error);
} finally {
  setIsGenerating(false);
}
```

かなり長い実装内容ですが、これで AI Agent 同士にインタラクティブに議論させているように表示させています。

バックエンドに力に入れすぎてフロントの実装が適当になってしまったのは反省点です。

時間が無かったとはいえ、かなり強引に実装してしまったなぁ・・と思っています。

## Web3 ✖︎ AI Agent はどうなっていく？？

最終的に **Web3 ✖︎ AI Agent** は **Intent(インテント)** に集約されていくのではないかと考えています。

AI Agent 用のツールやコントラクトの細かい実装などは、OSS や一部の強力なプロバイダーが実装していくことになるのではないでしょうか？

先日、 **Ethereum Foundation** からも Intent のフレームワークが発表され大きな話題を生みました。  
ここから AI Agent の力を借りてさらに洗練されていくのではないかと考えています。

https://github.com/BootNodeDev/intents-framework/tree/main

自然言語で DeFi や Web3 の全てのトランザクションが行えるようになったらユーザー体験は爆発的に良くなりますし、それこそが **Intent** が目指している世界ではないかと考えています。

それらの SDK やインフラが整い、アプリ開発のための技術スタックとして当たり前に取り入れられ始めた時に大きな注目を集めることになるのではないかと考えています。

絶対にこの技術は外せないものになっていくはずです。

## Web3 ✖︎ AI Agent は面白い！

ここまで色々書いてきましたが、最後に皆さんに共有したいのは、 **Web3 ✖︎ AI Agent** はめちゃくちゃ面白い領域だということです！！

技術的にもユーザー視点でも最終的にどのような結果が叩き出されるのかわからないというワクワク感が凄まじいです。

そしてまだ発展途上な段階であるため、さらなる進化が想定されます。

**Web3 ✖︎ AI Agent** が半年後、1 年後にどのような形になっているのか非常に楽しみです！

## 参考文献

今回のプロダクトを開発するにあたり、参考にした文献です。

https://github.com/mashharuki/CryptoAIAgentRepo

https://github.com/mashharuki/GoogleCloud-Sample

https://codelabs.developers.google.com/codelabs/how-to-deploy-gemini-powered-chat-app-cloud-run?hl=ja#0

https://github.com/mashharuki/GoogleCloud-Sample/tree/main/cloudrun/hono-sample

https://zenn.dev/nft/scraps/849d9121e8a001

https://t.co/hmqPQnnsgv

https://zenn.dev/pharmax/articles/8796b892eed183

https://www.encode.club/mammothon

https://www.brianknows.org/

https://paragraph.xyz/@zkether.eth/aiagentcrypto

https://www.anthropic.com/research/building-effective-agents

https://zenn.dev/umi_mori/books/prompt-engineer/viewer/langchain_agents

https://e2b.dev/ai-agents

https://blog.futuresmart.ai/multi-agent-system-with-langgraph

https://www.youtube.com/watch?v=CzBBhytDzM4

https://github.com/openai/openai-realtime-agents

https://github.com/fa0311/twitter-openapi-typescript

https://zenn.dev/ttks/articles/75c2102fe4657e

https://github.com/collabland/AI-Agent-Starter-Kit

https://github.com/Layr-Labs/hello-world-avs

https://www.notion.so/13-Use-Cases-for-the-Zero-Employee-Enterprise-ZEE-18481e29202580bea9fdc99ab5c1da6e?pvs=21

https://ai16z.github.io/eliza/

https://github.com/ai16z/eliza/tree/main

https://zenn.dev/komlock_lab/articles/e6ec0e6f3e0699

https://note.com/skyland_aikawa/n/n7aa4e5da6717?magazine_key=mef9e84c7c078

https://ai16z.github.io/eliza/docs/quickstart/

https://x.com/luna_virtuals

https://www.youtube.com/watch?v=C-vky-tXpqw

https://github.com/ytakahashi2020/Eliza/tree/main/01_createAgentWithTwitter

https://zenn.dev/ttks/articles/75c2102fe4657e

https://prompt-engineering-toolkit-rho.vercel.app/

https://docs.altlayer.io/altlayer-documentation

https://apps.autono.meme/login

https://apps.autono.meme/autonome

https://www.gaianet.ai/

https://www.gaianet.ai/docs

https://docs.gaianet.ai/category/user-guide

https://github.com/GaiaNet-AI/workshops

https://github.com/GaiaNet-AI

https://github.com/coinbase/cdp-agentkit/tree/master

https://docs.gaianet.ai/tutorial/eliza

https://privy-io.notion.site/ethglobalserverwalletquickstart

https://wardenprotocol.org/

https://docs.wardenprotocol.org/

https://www.youtube.com/c/NodesGuru

https://github.com/nodesguru

https://testnet.warden.explorers.guru/

https://docs.wardenprotocol.org/build-an-app/introduction

https://docs.wardenprotocol.org/build-a-keychain/introduction

https://faucet.chiado.wardenprotocol.org/

https://spaceward.chiado.wardenprotocol.org/

https://github.com/warden-protocol/wardenprotocol/tree/main

https://docs.wardenprotocol.org/build-an-app/examples-of-oapps

https://www.npmjs.com/package/@wardenprotocol/wardenjs

https://docs.wardenprotocol.org/build-an-app/deploy-smart-contracts-on-warden/deploy-an-evm-contract
