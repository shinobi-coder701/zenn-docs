---
title: "圧倒的な高速取引を実現するYellowProtocolについて調べてみた！"
emoji: "🌻"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["Web3","Ethereum","Typescript","ERC","blockchain"]
published: true
---


# はじめに

先日 **ETH Global**が主催する**HackMoney2026**に参加する機会があり**Yellow Protocol**というステートチャネルプロトコルについて調べる機会があったので学びをシェアするための記事を書きました！

https://ethglobal.com/events/hackmoney2026

ぜひ最後まで読んでいってください！

# Yellow Protcolとは

Yellow Network（イエローネットワーク）が開発・推進する「Yellow Protocol（イエロープロトコル）」は分散型金融（DeFi）の流動性を統一し、異なるブロックチェーン間での高速な取引と清算（クリアリング）を可能にする、Layer-3の分散型決済ネットワークです。 

https://www.yellow.org/

## 主な特徴・仕組み

- **Layer-3ピアツーピア・メッシュネットワーク**:   
  ブロックチェーン上の通信を高速化するため、既存のブロックチェーン（Layer-1/2）の上に構築された第3層ネットワーク。
- **ステートチャンネル技術**:   
  ビットコインのLightning Networkに触発された技術を採用し、ブロックチェーン外（オフチェーン）で高速に取引を行い、最終的な結果のみをオンチェーンに記録することで、高いスケーラビリティを実現。
- **分散型清算システム（ClearSync）**:   
  取引所やブローカー間で発生する流動性問題を解決し、取引の相手方リスクを軽減する、スマートコントラクトを活用した清算メカニズム。
- **非保管型（ノングストディアル）**:   
  取引所がユーザーの資金を保有せず、セキュリティの確保されたマルチシグ・スマートコントラクト上で資産が管理される。

## 目的とメリット

- 流動性の断片化の解決:   
  複数のブロックチェーンや取引所に分散している流動性を集約し、共通の流動性プールを作成する。
- 超高速・低コスト取引:   
  中央集権型取引所（CEX）のようなスピードと、分散型取引所（DEX）のセキュリティを両立させる。
- インターオペラビリティ（相互運用性）:   
  Ethereum、Polygon、Lineaなど、異なるネットワーク間でのシームレスな取引を可能にする。 

## $YELLOWトークン

ネットワーク内で使用されるネイティブトークン（$YELLOW）は、以下の用途で利用されます。

- 取引および清算手数料の支払い
- ブローカーの証拠金（ステートチャンネル開設のため）
- ネットワークへの参加（ノード運営など） 

# ERC7824とは

https://github.com/erc7824

https://ethereum-magicians.org/t/erc-7824-state-channels-framework/22566

ERC7824はYellow Protocolの心臓部である **「Nitrolite（ニトロライト）」プロトコルを定義する標準規格** です。

ブロックチェーンの拡張性（スケーラビリティ）問題を解決するための **「ステートチャネル・フレームワーク」** として設計されています。  

この規格により、以下のことが実現されます。

- **即時確定（ファイナリティ）**:   
  取引がブロックチェーンの承認を待たずに、当事者間ですぐに完了します。
- **ガス代の大幅な削減**:   
  ほとんどのやり取りをオフチェーン（チェーンの外）で行い、チェーン上には最小限の記録しか残さないため、手数料が非常に安く済みます。
- **高いセキュリティ**:    
  オンチェーンのスマートコントラクトによって安全性が担保されており、何か問題が起きてもブロックチェーン上の証拠を使って資産を取り戻す仕組みが備わっています。
- **互換性**:   
  Ethereumだけでなく、PolygonやBNB ChainなどのあらゆるEVM互換チェーンで動作するように設計されています。

# Yellow Protocolでできること

Yellow Protocolを利用することで、ユーザーや開発者は以下のようなメリットを享受できます。

- **超高速なクロスチェーン取引**:   
  資産をブリッジする手間やリスクなく、ビットコインやイーサリアムなど異なるチェーンの資産を、まるで一つの取引所にいるかのような感覚で瞬時に取引できます。
- **安全な資産管理（ノンカストディアル）**:   
  取引所に資産を預けっぱなしにする必要がなく、自分のウォレットや安全なスマートコントラクトで資産を管理したまま取引が可能です。
- **$YELLOWトークンの活用**:   
  ネットワーク内での取引手数料の支払いや、ブローカーがネットワークに参加するための担保として利用されます。
- **次世代アプリの開発**:   
  開発者はERC7824（Nitrolite SDK）を利用して、高速な決済システム、ゲーム、金融アプリケーションなどを簡単に構築できます。
- **流動性の共有**:   
  小規模な取引所（ブローカー）でも、Yellow Networkに接続することで、世界中の他のブローカーが持つ大きな流動性にアクセスできるようになります。

# サンプルコードを試してみよう！

## サンプルコード

https://github.com/mashharuki/yellow-sample

## 動かし方

まず以下のコマンドでテストネット用のytest.usdトークンのfaucetを取得します。

```bash
curl -XPOST https://clearnet-sandbox.yellow.com/faucet/requestTokens \
  -H "Content-Type: application/json" \
  -d '{"userAddress":"<自分のアドレス>"}'
```

以下のようになればOKです！

```json
{"success":true,"message":"Tokens sent successfully","txId":"14765","amount":"10000000","asset":"ytest.usd","destination":"0x51908F598A5e0d8F1A3bAbFa6DF76F9704daD072"}
```

今回はリポジトリの中にある`sdk-tutorials`フォルダ配下にあるプログラムが対象となります。

このプログラムでは2つのウォレットを使って共通のステートチャネルを作成し、状態更新(送金しあって残高情報を更新する)が試せます！

環境変数として以下の値を設定します。

```bash
CHAIN_ID=11155111
PRIVATE_KEY=
PRIVATE_KEY2=
```

セットアップとしてYellow Networkと接続するためのクライアントインスタンス等を準備する必要があります。

```ts
import { ContractAddresses } from "@erc7824/nitrolite";
import { config } from "dotenv";
import {
  createPublicClient,
  createWalletClient,
  http,
  type Address,
} from "viem";
import {
  generatePrivateKey,
  PrivateKeyAccount,
  privateKeyToAccount,
} from "viem/accounts";
import { base, sepolia } from "viem/chains";

config();

const { PRIVATE_KEY, PRIVATE_KEY2 } = process.env;

export interface SessionKey {
  privateKey: `0x${string}`;
  address: Address;
}

// Node RPC URL(検証ではこちらのサンドボックス用URLを使います)
export const YELLOW_RPC_URL = "wss://clearnet-sandbox.yellow.com/ws";

// Connect to Sandbox Node
export const ws = new WebSocket(YELLOW_RPC_URL);

/**
 * 一時的なセッションキーを生成するメソッド
 * @returns
 */
export const generateSessionKey = (): SessionKey => {
  const privateKey = generatePrivateKey();
  const account = privateKeyToAccount(privateKey);
  return { privateKey, address: account.address };
};

/**
 * チェーン後に応じたコントラクトアドレスを取得します。
 * @param chainId
 * @returns
 */
export function getContractAddresses(chainId: number): ContractAddresses {
  if (chainId === base.id) {
    return {
      custody: "0x490fb189DdE3a01B00be9BA5F41e3447FbC838b6",
      adjudicator: "0x7de4A0736Cf5740fD3Ca2F2e9cc85c9AC223eF0C",
    };
  }
  if (chainId === sepolia.id) {
    // Sepolia
    return {
      custody: "0x019B65A265EB3363822f2752141b3dF16131b262",
      adjudicator: "0x7c7ccbc98469190849BCC6c926307794fDfB11F2",
    };
  }

  throw new Error(`Unsupported chain ID: ${chainId}`);
}

/**
 * チェーンに応じたトークンアセットを取得します。
 */
export function getAssetByChain(chainId: number) {
  if (chainId === base.id) {
    return {
      token: "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
      decimals: 6,
      asset: "usdc",
    };
  }
  if (chainId === sepolia.id) {
    return {
      token: "0xDB9F293e3898c9E5536A3be1b0C56c89d2b32DEb",
      decimals: 6,
      asset: "ytest.usd",
    };
  }
  throw new Error(`Unsupported chain ID: ${chainId}`);
}

export const AUTH_SCOPE = "test.app";
export const APP_NAME = "Test app";
export const SESSION_DURATION = 3600; // 1 hour

// Verify environment variables
const privateKey = PRIVATE_KEY!;
const privateKey2 = PRIVATE_KEY2!;
if (!privateKey || !privateKey2) {
  throw new Error("PRIVATE_KEY not set in .env");
}

// Create account from private key
export const account = privateKeyToAccount(privateKey as `0x${string}`);
console.log("✓ Wallet loaded:", account.address);

export const account2 = privateKeyToAccount(privateKey2 as `0x${string}`);
console.log("✓ Wallet2 loaded:", account2.address);

/**
 * チェーンの種類に応じたパブリッククライアントとウォレットクライアントを作成します。
 */
export const getClientsByChain = (
  chainId: number,
  account: PrivateKeyAccount,
) => {
  let chain;
  if (chainId === base.id) {
    chain = base;
  } else if (chainId === sepolia.id) {
    chain = sepolia;
  }

  const publicClient = createPublicClient({
    chain,
    transport: http(),
  });

  const walletClient = createWalletClient({
    account: account,
    chain,
    transport: http(),
  });
  return { publicClient, walletClient };
};
```

これで準備OKです！

Yellow Networkと接続するとWebSocket通信を行うことになります。

例えば以下のような実装になります。

```ts
import {
  createAuthRequestMessage,
  createAuthVerifyMessage,
  createECDSAMessageSigner,
  createEIP712AuthMessageSigner,
  RPCMethod,
  type RPCResponse,
} from "@erc7824/nitrolite";
import {
  account,
  APP_NAME,
  AUTH_SCOPE,
  generateSessionKey,
  getClientsByChain,
  SESSION_DURATION,
} from "./lib/utils";

import { config } from "dotenv";
import { Client } from "yellow-ts";

const { CHAIN_ID } = process.env;

/**
 * メインスクリプト
 */
export async function main() {
  config();

  const sessionKey = generateSessionKey();

  // Think of this like a temporary stamp that proves we're allowed to make requests
  const sessionSigner = createECDSAMessageSigner(sessionKey.privateKey);

  const yellow = new Client();
  // Yellow NetworkとWebSocketで接続
  await yellow.connect();

  console.log(`Yellow connected`);

  console.log(`Session signer`, sessionSigner);

  const sessionExpireTimestamp = String(
    Math.floor(Date.now() / 1000) + SESSION_DURATION,
  );

  // Create authentication message with session configuration
  const authMessage = await createAuthRequestMessage({
    address: account.address,
    session_key: sessionKey.address, // Using account address as session key
    app_name: APP_NAME,
    allowances: [], // Define RPC allowances as needed
    expire: sessionExpireTimestamp, // 24 hours from now
    scope: AUTH_SCOPE, // Chain scope
    application: account.address, // Application contract address
  });
  console.log(`Auth message created`, authMessage);

  await yellow.sendMessage(authMessage);

  // チェーンIDに応じたクライアントを取得
  const { walletClient, publicClient } = getClientsByChain(
    Number(CHAIN_ID),
    account,
  );

  yellow.listen(async (message: RPCResponse) => {
    switch (message.method) {
      // 認証チャレンジのメッセージを受け取ったら認証を行う。
      case RPCMethod.AuthChallenge:
        console.log(`Auth Challenge`, message);

        const authParams = {
          scope: AUTH_SCOPE,
          application: walletClient.account?.address as `0x${string}`,
          participant: sessionKey.address as `0x${string}`,
          expire: sessionExpireTimestamp, // 24 hours from now
          allowances: [],
          session_key: sessionKey.address,
          expires_at: BigInt(sessionExpireTimestamp),
        };

        const eip712Signer = createEIP712AuthMessageSigner(
          walletClient,
          authParams,
          { name: APP_NAME },
        );

        const authVerifyMessage = await createAuthVerifyMessage(
          eip712Signer,
          message,
        );
        // 認証チャレンジ用のメッセージを送る
        await yellow.sendMessage(authVerifyMessage);
        break;

      case RPCMethod.Assets:
        const assets = message.params.assets;
        console.log(`Assets`, assets);
        break;

      case RPCMethod.Error:
        const error = message.params.error;
        console.log(`Error`, error);
        break;

      case RPCMethod.AuthVerify:
        console.log(`Auth verify`, message.params);
        break;

      case RPCMethod.ChannelsUpdate:
        console.log(`Channels`, message.params);
        break;

      case RPCMethod.BalanceUpdate:
        console.log(`Balances`, message.params);
        break;
    }
  });

  const blockNumber = await publicClient.getBlockNumber();
  console.log(`Current block number: ${blockNumber}`);
}

if (require.main === module) {
  main().catch(console.error);
}
```

では次に複数ウォレットがやりとりするマルチパーティ用のステートレスチャネルを作成するサンプルコードの解説です。

このスクリプトは、Nitroliteステートチャネルを使用してマルチパーティ（複数参加者）アプリケーションセッションを作成および管理する方法を実演します。アプリセッションにより、複数の参加者が共有されたオフチェーンコンテキスト内で、暗号的に保護された状態更新を行いながら対話することができます。

:::message

**このコードで学べること**

* 1. マルチパーティ認証のセットアップ (2つのウォレット)
* 2. 複数の参加者を持つアプリケーションの定義
* 3. 初期割り当てを伴うアプリセッションの作成
* 4. セッション状態の更新 (参加者間の価値の移動)
* 5. 複数署名によるセッションの終了
:::

:::message
**フローの概要**

* 1. Yellowネットワークに接続
* 2. 両方の参加者のウォレットを認証
* 3. アプリ構成を定義 (参加者、重み付け、定足数)
* 4. 初期残高割り当てでセッションを作成
* 5. 状態更新を送信 (オフチェーンでの状態変更を実演)
* 6. 複数署名を用いてセッションを終了
:::

そのコードの内容が以下です！

```ts
import {
  createAppSessionMessage,
  createCloseAppSessionMessage,
  createECDSAMessageSigner,
  createSubmitAppStateMessage,
  RPCAppDefinition,
  RPCAppSessionAllocation,
  RPCData,
  RPCMethod,
  RPCProtocolVersion,
  RPCResponse,
} from "@erc7824/nitrolite";
import { config } from "dotenv";
import { WalletClient } from "viem";
import { Client } from "yellow-ts";
import { authenticateWallet } from "../../lib/auth";
import {
  account,
  account2,
  APP_NAME,
  getClientsByChain,
  YELLOW_RPC_URL,
} from "../../lib/utils";

config();

const { CHAIN_ID } = process.env;

/**
 * メインスクリプト
 */
export async function main() {
  // ============================================================================
  // STEP 1: Yellowネットワークに接続
  // ============================================================================
  // YellowクリアネットエンドポイントへのWebSocket接続を確立します
  const yellow = new Client({
    url: YELLOW_RPC_URL,
  });

  await yellow.connect();
  console.log("🔌 Connected to Yellow clearnet");

  // ============================================================================
  // STEP 2: 両方の参加者のウォレットをセットアップ
  // ============================================================================
  // シードフレーズから両方の参加者用のウォレットクライアントを作成します
  // 実際のアプリケーションでは、各参加者がそれぞれのウォレットを管理します

  const { walletClient } = getClientsByChain(Number(CHAIN_ID), account);
  const { walletClient: wallet2Client } = getClientsByChain(
    Number(CHAIN_ID),
    account2,
  );

  // ============================================================================
  // STEP 3: 両方の参加者を認証
  // ============================================================================
  // 各参加者は、メッセージ署名用のセッションキーを作成するために認証を行う必要があります
  // これにより、メインウォレットで毎回署名することなく、RPCメッセージに署名できるようになります
  const sessionKey = await authenticateWallet(
    yellow,
    walletClient as WalletClient,
  );
  const messageSigner = createECDSAMessageSigner(sessionKey.privateKey);

  const sessionKey2 = await authenticateWallet(yellow, wallet2Client);
  const messageSigner2 = createECDSAMessageSigner(sessionKey2.privateKey);

  // アプリ定義で使用するために、参加者のアドレスを抽出します
  const userAddress = walletClient.account?.address as `0x${string}`;
  const partnerAddress = wallet2Client.account?.address as `0x${string}`;

  // ============================================================================
  // STEP 4: アプリケーション構成の定義
  // ============================================================================
  // アプリ定義では以下を指定します:
  // - participants: 参加者アドレスの配列
  // - weights: 各参加者の投票の重み (ここでは50/50)
  // - quorum: 決定に必要な割合/定足数 (100 = 全員一致)
  // - challenge: チャレンジ期間の秒数 (0 = チャレンジ期間なし)
  // - nonce: このアプリインスタンスの一意な識別子
  const appDefinition: RPCAppDefinition = {
    protocol: RPCProtocolVersion.NitroRPC_0_4,
    participants: [userAddress, partnerAddress],
    weights: [50, 50], // 均等な投票権
    quorum: 100, // 全員一致の合意が必要
    challenge: 0, // チャレンジ期間なし
    nonce: Date.now(), // 一意のセッション識別子
    application: APP_NAME,
  };

  // ============================================================================
  // STEP 5: 初期割り当ての設定
  // ============================================================================
  // 各参加者がどの資産をどれだけ持って開始するかを定義します
  // この例では: userAddress が 0.01 USDC、partnerAddress が 0 を持ちます
  // base と sepoliaで許容されているアセットの種類が異なります。
  let allocations: RPCAppSessionAllocation[] = [];

  if (CHAIN_ID === "8453") {
    allocations = [
      { participant: userAddress, asset: "usdc", amount: "0.00" },
      { participant: partnerAddress, asset: "usdc", amount: "0.01" },
    ] as RPCAppSessionAllocation[];
  } else if (CHAIN_ID === "11155111") {
    allocations = [
      { participant: userAddress, asset: "ytest.usd", amount: "0.00" },
      { participant: partnerAddress, asset: "ytest.usd", amount: "0.01" },
    ] as RPCAppSessionAllocation[];
  }

  // ============================================================================
  // STEP 6: アプリセッションの作成と送信
  // ============================================================================
  // 最初の参加者によって署名されたセッションメッセージを作成します
  const sessionMessage = await createAppSessionMessage(messageSigner, {
    definition: appDefinition,
    allocations,
  });

  // 2つ目の参加者の署名を追加
  const sessionMessageJson = JSON.parse(sessionMessage);
  const signedSessionMessageSignature2 = await messageSigner2(
    sessionMessageJson.req as RPCData,
  );
  sessionMessageJson.sig.push(signedSessionMessageSignature2);

  console.log(
    "📝 Session message created with both signatures:",
    sessionMessageJson,
  );

  // セッションレスポンスを待つためのPromise
  const sessionResponsePromise = new Promise<any>((resolve, reject) => {
    const timeout = setTimeout(() => {
      reject(new Error("Session creation timeout"));
    }, 30000); // 30秒のタイムアウト

    const listener = async (message: RPCResponse) => {
      console.log("📨 Received message:", message); // すべてのメッセージをログ出力

      if (
        message.method === "create_app_session" &&
        message.params.appSessionId
      ) {
        clearTimeout(timeout);
        resolve(message);
      } else if (message.method === RPCMethod.Error) {
        clearTimeout(timeout);
        reject(new Error(`Session creation failed: ${message.params.error}`));
      }
    };

    yellow.listen(listener);
  });

  // セッション作成リクエストをYellowに送信します
  await yellow.sendMessage(JSON.stringify(sessionMessageJson));
  console.log("✅ Session message sent");

  const sessionResponse = await sessionResponsePromise;
  console.log("🆔 Session response:", sessionResponse);

  // ============================================================================
  // STEP 7: セッション状態の更新 (アプリセッション内での送金)
  // ============================================================================
  // アプリセッション内での状態変化を表す新しい割り当てを作成します
  // ここでは、userからpartnerへ 0.01 ytest.usd 全額を送金しています
  // これはオンチェーン取引を介さずに、オフチェーンでの状態更新（送金）を実演しています
  // 注意: これはsubmitAppStateMessageを使ったアプリセッション内の送金です

  // base と sepoliaで許容されているアセットの種類が異なります。
  let finalAllocations: RPCAppSessionAllocation[] = [];

  if (CHAIN_ID === "8453") {
    finalAllocations = [
      { participant: userAddress, asset: "usdc", amount: "0.00" },
      { participant: partnerAddress, asset: "usdc", amount: "0.01" },
    ] as RPCAppSessionAllocation[];
  } else if (CHAIN_ID === "11155111") {
    finalAllocations = [
      { participant: userAddress, asset: "ytest.usd", amount: "0.00" },
      { participant: partnerAddress, asset: "ytest.usd", amount: "0.01" },
    ] as RPCAppSessionAllocation[];
  }

  console.log(
    "🔄 Updating session state with new allocations:",
    finalAllocations,
  );

  // 更新された状態をYellowに送信します
  const submitAppStateMessage = await createSubmitAppStateMessage(
    messageSigner,
    {
      app_session_id: sessionResponse.params.appSessionId,
      allocations: finalAllocations,
    },
  );

  const submitAppStateMessageJson = JSON.parse(submitAppStateMessage);
  console.log("📊 Submit app state message:", submitAppStateMessageJson);

  // ============================================================================
  // STEP 8: 複数署名によるセッションの終了
  // ============================================================================
  // 終了セッションメッセージを作成します (最初の参加者が署名)
  const closeSessionMessage = await createCloseAppSessionMessage(
    messageSigner,
    {
      app_session_id: sessionResponse.params.appSessionId,
      allocations: finalAllocations,
    },
  );

  // 追加の署名を加えるためにメッセージをパースします
  const closeSessionMessageJson = JSON.parse(closeSessionMessage);

  // ============================================================================
  // STEP 9: 2人目の参加者の署名を収集
  // ============================================================================
  // マルチパーティセッションでは、全参加者が終了メッセージに署名する必要があります
  // ここでは、2人目の参加者のセッションキーで署名を行っています
  const signedCloseSessionMessageSignature2 = await messageSigner2(
    closeSessionMessageJson.req as RPCData,
  );

  console.log(
    "✍️  Wallet 2 signed close session message:",
    signedCloseSessionMessageSignature2,
  );

  // メッセージに2つ目の署名を追加します
  // 定足数 (quorum) が100%であるため、両方の署名が必要です
  closeSessionMessageJson.sig.push(signedCloseSessionMessageSignature2);

  console.log(
    "📤 Close session message (with all signatures):",
    closeSessionMessage,
  );

  // ============================================================================
  // STEP 10: 終了リクエストの送信
  // ============================================================================
  // セッションを確定させるため、全ての署名が揃った終了メッセージを送信します
  const closeSessionResponse = await yellow.sendMessage(
    JSON.stringify(closeSessionMessageJson),
  );
  console.log("✅ Close session message sent");

  console.log("🎉 Close session response:", closeSessionResponse);

  // サーバーからの追加メッセージをリッスンします
  yellow.listen(async (message: RPCResponse) => {
    console.log("📨 Received message:", message);
  });
}

main().catch((error) => {
  console.error("❌ Error:", error.message || error);
  process.exitCode = 1;
});

```

# まとめ

以上、 **Yellow Protocol**についての技術ブログでした！

Ethereumエコシステムでもステートレスチャネルの高速取引を実現させている点は非常に画期的ですし、EVM互換性があるので多くのブロックチェーンにも対応できる点は強みだと思いました！

まだ基本的な使い方しかできていませんが、マスターしたら応用が効きそうなので引き続きウォッチしようと思います。

ここまで読んでいただきありがとうございました。

# 参考文献

- [Yellow Protocol Docs](https://docs.yellow.org)
- [ERC7824 Specification](https://eips.ethereum.org/EIPS/eip-7824)
- [Quickstart](https://docs.yellow.org/docs/build/quick-start/)
- [Yellow SDK Tutorial](https://github.com/stevenzeiler/yellow-sdk-tutorials/tree/main)
- [GitHub SDKリポジトリ](https://github.com/erc7824/nitrolite)
- [ETH Global Yellow Protocol](https://ethglobal.com/events/prague/prizes/yellow)
- [Yellow SDK](https://github.com/stevenzeiler/yellow-sdk-tutorials/tree/main)