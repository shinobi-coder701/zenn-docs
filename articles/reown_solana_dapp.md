---
title: "Reownを使ってWeb3アプリを作ってみた！"
emoji: "🤖"
type: "tech"
topics: ["Solana", "Web3", "TypeScript", "ブロックチェーン", "生成AI"]
published: false
---

![](/images/reown_solana_dapp/title.png)

## 🚀 はじめに

**Breakout** という Solana ハッカソンで、Reown の SDK を使って Web3 アプリを開発してみました！

https://www.colosseum.org/breakout

**「Solana とどうつなぐの？」** **「コントラクト機能をどう呼び出すの？」** といった疑問を、実際のコード付きで徹底解説します。

初心者から中級者まで使えるノウハウ満載、最速で動くデモもご用意しましたので、ぜひ最後までご覧ください！

## 💡 Reown SDK とは？

**Reown** は **WalletConnect** をリブランディングしたものです。

https://reown.com/

**Reown SDK** は、

- Solana や EVM 系などマルチチェーンに対応したウォレット機能を提供している SDK です
- **Anchor** や **viem** などの SDK と組みわせてコントラクトの呼び出し＆書き込み処理が可能です！
- TypeScript/JavaScript 対応

など Web3 アプリ開発に必要な機能をワンパッケージで提供してくれるウォレット系のライブラリです。

デモサイトも公開されています！！

**EVM 系だけではなく Solana などスマートコントラクトの仮想マシンが異なる複数のブロックチェーンに対応している点が大きな特徴** です！

https://demo.reown.com/?config=eyJmZWF0dXJlcyI6eyJyZWNlaXZlIjp0cnVlLCJzZW5kIjp0cnVlLCJlbWFpbFNob3dXYWxsZXRzIjp0cnVlLCJjb25uZWN0b3JUeXBlT3JkZXIiOlsid2FsbGV0Q29ubmVjdCIsInJlY2VudCIsImluamVjdGVkIiwiZmVhdHVyZWQiLCJjdXN0b20iLCJleHRlcm5hbCIsInJlY29tbWVuZGVkIl0sImFuYWx5dGljcyI6dHJ1ZSwiYWxsV2FsbGV0cyI6dHJ1ZSwibGVnYWxDaGVja2JveCI6ZmFsc2UsInNtYXJ0U2Vzc2lvbnMiOmZhbHNlLCJjb2xsYXBzZVdhbGxldHMiOmZhbHNlLCJ3YWxsZXRGZWF0dXJlc09yZGVyIjpbIm9ucmFtcCIsInN3YXBzIiwicmVjZWl2ZSIsInNlbmQiXSwiY29ubmVjdE1ldGhvZHNPcmRlciI6WyJlbWFpbCIsInNvY2lhbCIsIndhbGxldCJdLCJwYXkiOmZhbHNlfSwidGhlbWVWYXJpYWJsZXMiOnt9LCJyZW1vdGVGZWF0dXJlcyI6eyJzd2FwcyI6WyIxaW5jaCJdLCJvbnJhbXAiOlsiY29pbmJhc2UiLCJtZWxkIl0sImVtYWlsIjp0cnVlLCJzb2NpYWxzIjpbImdvb2dsZSIsIngiLCJmYXJjYXN0ZXIiLCJkaXNjb3JkIiwiYXBwbGUiLCJnaXRodWIiLCJmYWNlYm9vayJdLCJhY3Rpdml0eSI6dHJ1ZSwicmVvd25CcmFuZGluZyI6dHJ1ZX19

## Reown SDK の導入方法

導入方法は以下の 3 ステップです！！！

### 1. API キーの発行

まずダッシュボードで API キーを発行する必要があります！！

https://cloud.reown.com

### 2. ライブラリのインストール

次に必要なライブラリを一式インストールします。

```bash
npm install @reown/appkit @coral-xyz/anchor @reown/appkit-adapter-solana @solana/wallet-adapter-react @solana/web3.js
```

### 3. appkit-button コンポーネントの埋め込み

ここまできたら必要な設定ファイルを用意して、 `<appkit-button>` を埋め込めば準備 OK です！

- 設定ファイル(config.ts)の実装

  環境変数の読み込みや対応するチェーンの種類などを定義します。

  今回はメインネット、テストネット、Dev ネットを指定しています。

  ```ts
  import { SolanaAdapter } from "@reown/appkit-adapter-solana/react";
  import type { AppKitNetwork } from "@reown/appkit/networks";

  // Get projectId from https://cloud.reown.com
  export const projectId =
    process.env.NEXT_PUBLIC_PROJECT_ID || "b56e18d47c72ab683b10814fe9495694";

  if (!projectId) {
    throw new Error("Project ID is not defined");
  }

  // solana mainnet, testnet, and devnet
  export const networks = [solana, solanaTestnet, solanaDevnet] as [
    AppKitNetwork,
    ...AppKitNetwork[]
  ];

  // Set up Solana Adapter
  export const solanaWeb3JsAdapter = new SolanaAdapter();
  ```

- `createAppKit` で AppKit インスタンスを生成

  上記設定ファイルを読み込んで **AppKit** を生成させます。

  下記は実装例です。

  ```ts
  "use client";

  import { networks, projectId, solanaWeb3JsAdapter } from "@/config";
  import { createAppKit } from "@reown/appkit";
  import { ConnectionProvider } from "@solana/wallet-adapter-react";
  import { clusterApiUrl } from "@solana/web3.js";
  import { createContext, useEffect, useState, type ReactNode } from "react";

  // Set up metadata
  const metadata = {
    name: "oto",
    description: "oto",
    url: "https://github.com/Heterod0x/oto", // origin must match your domain & subdomain
    icons: ["https://avatars.githubusercontent.com/u/179229932"],
  };

  const solanaEndpoint = clusterApiUrl("devnet");

  // Create the modal
  export const modal = createAppKit({
    adapters: [solanaWeb3JsAdapter], // ここでアダプターを指定
    projectId, // プロジェクトIdを指定
    networks, // 対応するブロックチェーンを指定
    metadata,
    themeMode: "light",
    features: {
      analytics: true, // Optional - defaults to your Cloud configuration
    },
    themeVariables: {
      "--w3m-accent": "#000000",
    },
  });

  // Create context
  export const WalletContext = createContext<WalletContextType>(defaultContext);

  // Provider component
  export function WalletProvider({ children }: { children: ReactNode }) {
    return (
      <ConnectionProvider endpoint={solanaEndpoint}>
        <WalletContext.Provider>{children}</WalletContext.Provider>
      </ConnectionProvider>
    );
  }
  ```

  そしたら任意のコンポーネントファイルに埋め込んであげるだけです！！

  <br/>

  `<appkit-button />` ですね！

  <br/>

  これを埋め込んであげるだけでウォレット接続やアドレスの QR コード、残高表示など最低限必要な機能が簡単に実装できてしまいます！！！

  ```ts
  "use client";

  import { useAppKitAccount } from "@reown/appkit/react";
  import { useRouter } from "next/navigation";
  import { useEffect } from "react";

  /**
   * Home Component
   */
  export default function Home() {
    const { address: walletAddress } = useAppKitAccount();
    const router = useRouter();

    useEffect(() => {
      if (walletAddress) {
        router.push("/record");
      }
    }, [walletAddress, router]);

    return (
      <div className="container flex flex-col items-center justify-center min-h-screen py-12 space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-2">Welcome to Oto</h1>
          <p className="text-xl text-muted-foreground">
            Connect your wallet to get started
          </p>
        </div>

        {walletAddress ? null : (
          <div className="flex flex-col items-center">
            {/* これが Reown SDKが提供しているコンポーネント */}
            <appkit-button />
          </div>
        )}
      </div>
    );
  }
  ```

## 🛠 コントラクトを呼び出す方法

今回は **Solana** 上にデプロイしたスマートコントラクトの機能を呼び出す方法を紹介します！

**reown** の特徴は **Solana** と **EVM** 系のブロックチェーン両方に対応している点です！

さすがにコントラクトを呼び出す部分だけは書き換える必要が出てきますが、大元のウォレットの SDK をいちいち変える必要がないところが良いですね。

hooks として実装しました。

書き込み系・読み込み系のメソッド両方とも実装しているので参考にしてください！

```typescript
"use client";

import { BN, Program } from "@coral-xyz/anchor";
import { useAppKitAccount, useAppKitProvider } from "@reown/appkit/react";
import {
  ASSOCIATED_TOKEN_PROGRAM_ID,
  TOKEN_PROGRAM_ID,
} from "@solana/spl-token";
import { PublicKey, SYSVAR_RENT_PUBKEY } from "@solana/web3.js";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useEffect, useMemo, useState } from "react";

import { Oto } from "@/contracts/oto";
import otoIdl from "@/contracts/oto.json";
import { useAnchorProvider } from "./useAnchorProvider";

// Constants
const OTO_SEED = "oto";
const USER_SEED = "user";
const MINT_SEED = "mint";

/**
 * Custom hook to communicate with the Oto contract
 * @returns Functions and data for contract operations
 */
export const useContract = () => {
  const [otoPDA, setOtoPDA] = useState<string | null>(null);
  const [userPDA, setUserPDA] = useState<string | null>(null);
  const [mintPDA, setMintPDA] = useState<string | null>(null);

  const { address } = useAppKitAccount();
  // Solanaの場合は "solana" を引数に指定する。
  // EVMの場合は、 "eip155"を引数に指定する
  const { walletProvider } = useAppKitProvider<any>("solana");
  // Anchor SDKの useAnchorProviderを使います。
  const { provider, cluster } = useAnchorProvider();

  // 今回使うコントラクトのプログラムID
  const programId = useMemo(() => {
    try {
      return new PublicKey(otoIdl.address);
    } catch (error) {
      console.error("Failed to create PublicKey:", error);
      return null;
    }
  }, []);

  // Otoコントラクトインスタンスの生成
  const program = useMemo(() => {
    try {
      if (!provider || !programId) return null;
      // Create Program class correctly
      return new Program<Oto>(otoIdl as any, provider);
    } catch (error) {
      console.error("Failed to create Program instance:", error);
      return null;
    }
  }, [provider, programId]);

  // Calculation of PDAs
  useEffect(() => {
    /**
     * calculatePDAs method
     * @returns
     */
    const calculatePDAs = async () => {
      if (!program || !programId) return;

      console.log("Program ID:", programId.toBase58());

      // Oto PDA - correct seeds based on IDL definition
      const [oto] = PublicKey.findProgramAddressSync(
        [Buffer.from(OTO_SEED)],
        programId
      );
      setOtoPDA(oto.toBase58());
      console.log("Oto PDA:", oto.toBase58());

      // Mint PDA - correct seeds based on IDL definition
      const [mint] = PublicKey.findProgramAddressSync(
        [Buffer.from(MINT_SEED)],
        programId
      );
      setMintPDA(mint.toBase58());
      console.log("Mint PDA:", mint.toBase58());
    };

    calculatePDAs();
  }, [program, programId]);

  const getUserId = (address: string) => {
    return address.substring(0, 8);
  };

  /**
   * Calculate PDA for a specific user
   * @param userId
   * @returns
   */
  const getUserPDA = async (userId: string) => {
    if (!programId) return null;
    console.log("Program ID:", programId.toBase58());
    console.log("User ID:", userId);

    // If user ID is too long, use only the first 8 characters
    // Or, if using the wallet address, limit to a certain length
    const shortenedUserId = getUserId(userId);
    console.log("Shortened User ID:", shortenedUserId);

    // PDA - generate correct PDA using USER_SEED and userId
    const [userPDA] = PublicKey.findProgramAddressSync(
      [Buffer.from(USER_SEED), Buffer.from(shortenedUserId)],
      programId
    );
    return userPDA.toBase58();
  };

  /**
   * get User Account PDA
   * @param userId
   * @returns
   */
  const getUserAccount = async (userId: string) => {
    if (!program || !programId) return null;

    try {
      // call getUserPDA to get correct user PDA
      const userAddress = await getUserPDA(userId);
      console.log("User Address:", userAddress);
      if (!userAddress) return null;

      const userPDA = new PublicKey(userAddress);
      console.log("userPDA", userPDA.toBase58());

      // call fetch method with the correct PDA
      return await program.account.user.fetch(userPDA);
    } catch (error: any) {
      // Identify cases where the account does not exist
      if (
        error.message?.includes("Account does not exist") ||
        error.message?.includes("account not found") ||
        error.message?.includes("Program failed to complete")
      ) {
        console.log("User account does not exist:", userId);

        if (!program || !address || !otoPDA || !mintPDA)
          throw new Error("Not initialized");
      }

      return null;
    }
  };

  /**
   * Mutation to initialize a user
   */
  const initializeUser = useMutation({
    mutationKey: ["oto", "initializeUser", { cluster }],
    mutationFn: async ({
      userId,
      owner,
    }: {
      userId: string;
      owner?: string;
    }) => {
      // 以後、実際の処理
      if (!program || !address || !otoPDA) throw new Error("Not initialized");

      const shortenedUserId = getUserId(userId);

      // Use the specified owner or the current connected address
      const ownerKey = owner ? new PublicKey(owner) : new PublicKey(address);

      // Calculate the user's PDA
      const calculatedUserPDA = await getUserPDA(userId);
      if (!calculatedUserPDA) throw new Error("Failed to calculate user PDA");

      console.log("User PDA to initialize:", calculatedUserPDA);
      console.log("Oto PDA:", otoPDA);
      console.log("Payer:", address);

      // Correctly specify the required accounts based on the IDL
      try {
        // Userの初期化
        const sig = await program.methods
          .initializeUser(shortenedUserId, ownerKey)
          .accounts({
            payer: new PublicKey(address),
          })
          .rpc();
        console.log(sig);
      } catch (error) {
        console.error("Failed to initialize user account:", error);
      }
    },
  });

  /**
   * Mutation to initialize the Oto program
   */
  const initializeOto = useMutation({
    mutationKey: ["oto", "initializeOto", { cluster }],
    mutationFn: async ({ nftCollection }: { nftCollection: PublicKey }) => {
      if (!program || !address || !programId)
        throw new Error("Not initialized");

      // Calculate PDAs
      const [otoPDA] = PublicKey.findProgramAddressSync(
        [Buffer.from(OTO_SEED)],
        programId
      );

      const [mintPDA] = PublicKey.findProgramAddressSync(
        [Buffer.from(MINT_SEED)],
        programId
      );

      console.log("Oto PDA:", otoPDA.toBase58());
      console.log("Mint PDA:", mintPDA.toBase58());

      // Calculate metadata address
      const TOKEN_METADATA_PROGRAM_ID = new PublicKey(
        "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
      );
      const metadataAddress = PublicKey.findProgramAddressSync(
        [
          Buffer.from("metadata"),
          TOKEN_METADATA_PROGRAM_ID.toBytes(),
          mintPDA.toBytes(),
        ],
        TOKEN_METADATA_PROGRAM_ID
      )[0];

      console.log("Oto PDA to initialize:", otoPDA.toBase58());
      console.log("Mint PDA:", mintPDA.toBase58());
      console.log("NFT Collection:", nftCollection.toBase58());
      console.log("Metadata Address:", metadataAddress.toBase58());

      // Otoを初期化
      return await program.methods
        .initializeOto()
        .accounts({
          payer: new PublicKey(address),
          nftCollection: nftCollection,
          tokenProgram: TOKEN_PROGRAM_ID,
          rent: SYSVAR_RENT_PUBKEY,
          tokenMetadataProgram: TOKEN_METADATA_PROGRAM_ID,
          metadata: metadataAddress,
        })
        .rpc();
    },
  });

  /**
   * Mutation to claim tokens
   */
  const claimTokens = useMutation({
    mutationKey: ["oto", "claim", { cluster }],
    mutationFn: async ({
      userId,
      claimAmount,
    }: {
      userId: string;
      claimAmount: number;
    }) => {
      if (!program || !address || !otoPDA || !mintPDA)
        throw new Error("Not initialized");

      // Calculate user PDA
      const shortenedUserId = getUserId(userId);
      const calculatedUserPDA = await getUserPDA(shortenedUserId);
      if (!calculatedUserPDA) throw new Error("Failed to calculate user PDA");

      // Calculate ATA
      const [userTokenAccount] = await PublicKey.findProgramAddressSync(
        [walletProvider.publicKey.toBytes()],
        ASSOCIATED_TOKEN_PROGRAM_ID
      );

      // Oto トークンをクレームする
      return program.methods
        .claim(shortenedUserId, new BN(claimAmount))
        .accounts({
          beneficiary: address,
          tokenProgram: TOKEN_PROGRAM_ID,
        })
        .rpc();
    },
  });

  /**
   * Mutation to update points (for admin)
   */
  const updatePoint = useMutation({
    mutationKey: ["oto", "updatePoint", { cluster }],
    mutationFn: async ({
      userId,
      delta,
    }: {
      userId: string;
      delta: number;
    }) => {
      if (!program || !address || !otoPDA) throw new Error("Not initialized");

      // Calculate user PDA
      const shortenedUserId = getUserId(userId);
      const calculatedUserPDA = await getUserPDA(shortenedUserId);
      if (!calculatedUserPDA) throw new Error("Failed to calculate user PDA");

      // ポイントを更新する
      return program.methods
        .updatePoint(shortenedUserId, new BN(delta))
        .accounts({
          oto: otoPDA,
          user: calculatedUserPDA,
          admin: address,
        })
        .rpc();
    },
  });

  /**
   * Query to get Oto account information
   */
  const getOtoAccount = useQuery({
    queryKey: ["oto", "otoAccount", { cluster }],
    queryFn: async () => {
      if (!program || !otoPDA) throw new Error("Not initialized");
      return program.account.oto.fetch(otoPDA);
    },
    enabled: !!program && !!otoPDA,
  });

  /**
   * Query to get the claimable amount for a user
   * Automatically initializes the user if they do not exist
   */
  const getClaimableAmount = useQuery({
    queryKey: ["oto", "claimableAmount", { userId: address, cluster }],
    queryFn: async () => {
      if (!address || !program) throw new Error("Not initialized");

      try {
        const userId = address; // Use the current address as the user ID
        console.log("User ID:", userId);

        // Get user account information
        let userAccount = await getUserAccount(userId);

        console.log("User account information:", userAccount);

        if (!userAccount) {
          console.log(
            "User account is not initialized. Returning claimable amount as 0"
          );
          return "0";
        }

        // Check if claimableAmount exists
        if (userAccount.claimableAmount) {
          console.log(
            "userAccount.claimableAmount:",
            userAccount.claimableAmount
          );
          const amount = userAccount.claimableAmount.toString();
          console.log(`Claimable amount for user ${userId}: ${amount}`);
          return amount;
        }

        return "0";
      } catch (error) {
        console.error("Error fetching claimable amount:", error);
        return "0"; // Return 0 in case of error (to avoid breaking the UI)
      }
    },
    enabled: !!program && !!address && !!walletProvider,
    staleTime: 60 * 1000, // Use cache for 1 minute
    refetchOnWindowFocus: true, // Refetch on window focus
    retry: 2, // Retry 2 times on error
  });

  return {
    program,
    programId,
    otoPDA,
    mintPDA,
    getUserPDA,
    getUserAccount,
    initializeUser,
    initializeOto,
    claimTokens,
    updatePoint,
    getOtoAccount,
    getClaimableAmount,
  };
};

export default useContract;
```

以上実装の解説になります！！

## 🔥 実際の挙動の様子

- ログイン前

  connect ボタンを押すとウォレットに接続できます！

  ![](/images/reown_solana_dapp/0.png)

- Wallet Connect

  ウォレットは **Phantom** や **Backpack** の他、メールアドレスや Gmail でも設定可能です！

  ![](/images/reown_solana_dapp/0.1.png)

- ログイン後

  ログイン後は、 `<appkit-button>` コンポーネントが多機能なウォレットボタンに様変わり！

  ![](/images/reown_solana_dapp/1.png)

  残高やアドレスを確認したり、接続するチェーンを切り替えたりすることができます！！

  ![](/images/reown_solana_dapp/4.png)

  ![](/images/reown_solana_dapp/2.png)

  署名処理が必要な場合には、このようなモーダルが立ち上がりユーザー Sign ボタンを押すだけで署名処理を行うことができます！！

  問題がなければそのままトランザクションがブロックチェーンに送られます！

  ![](/images/reown_solana_dapp/3.png)

## 📂 リポジトリ＆デモ

今回僕たちが作ったプロダクトのリポジトリやデモサイトのリンクを共有します！！

もし良かったら見てみてください！！

### プロダクトページ

今回、 **Oto** というプロダクトを開発しました！

AI の学習データ不足を解決するためのプロダクトです！！

https://arena.colosseum.org/projects/explore/oto

### ピッチスライド

まだ実物がありませんが、AI デバイスの構想もあります！

https://www.figma.com/slides/zENm8UTvypmVpUscp14Imc/oto---Pitch-Deck?node-id=5-45&t=3RG8vMWEwdsLl8zv-0

### GitHub リポジトリ

https://github.com/Heterod0x/oto

### デモサイト

https://oto-gules.vercel.app/

### GitBook

https://oto-dev.gitbook.io/oto

## まとめ

**Reown SDK** を使えば、Solana や EVM などマルチチェーンに対応した Web3 アプリ開発がグッとラクに！

ぜひ一度開発者ドキュメントを見たり、デモアプリを試したりしてみてください！！

今回はここまでになります！

読んでいただきありがとうございました！
