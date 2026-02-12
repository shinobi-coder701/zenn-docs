---
title: "CircleのSDKでステーブルコインを操作してみよう！"
emoji: "🟠"
type: "tech" 
topics: ["Web3","blockchain","SDK","ステーブルコイン","TypeScript"]
published: false
---

# Circleとは

Circleは、USDC・EURCなどのステーブルコインを発行し、ウォレット、クロスチェーン転送（CCTP）、スマートコントラクトプラットフォームなどの開発者向けインフラを提供する企業です。また、ArcというオープンなLayer-1ブロックチェーンも構築しています。

https://www.circle.com/

昨年金融庁から初めて承認を得て発行が開始されて日本円建てステーブルコインJPYCの株主でもあります。

https://prtimes.jp/main/html/rd/p/000000283.000054018.html

https://jpyc.co.jp/

# USDCとは

USDCは米ドルに連動した法定通貨担保型ステーブルコインです。Arcネットワークではネイティブガストークンとして使われ、取引手数料の支払いにも利用されます。価格が安定しているため、手数料が予測可能（約$0.01/トランザクション）になります。

# Arcとは

Arcは、Circleが構築したオープンなLayer-1ブロックチェーンです。

https://www.arc.network/blog/circle-launches-arc-public-testnet

レンディング、資本市場、FX、決済など、現実世界の経済活動をオンチェーンで実現するために設計されています。

Arcはパブリックネットワークなので誰でも自由に開発・取引が可能ですが、バリデータはセキュリティとコンプライアンスのために許可制（Proof-of-Authority）となっています。

## Arcの主な特徴

- **EVM互換**:   
  Solidity・Foundry・Hardhatなど、Ethereumと同じツールがそのまま使えます
- **USDCがネイティブガストークン**:   
  ETHではなくUSDCで手数料を支払うため、コストが安定（約$0.01/tx）
- **サブ秒の確定的ファイナリティ**:   
  Malachite（Tendermint BFT）ベースのコンセンサスにより、1秒未満でトランザクションが確定・不可逆
- **高スループット**:   
  バリデータ20台で3,000+ TPS、4台で10,000+ TPS
- **オプトインプライバシー**:     
  暗号化された金額での送金やView Keyによる選択的開示（ロードマップ上）
- **クロスチェーン対応**:   
  CCTPやGatewayで他チェーンとのUSDCブリッジが可能

## アーキテクチャ

| レイヤー | 技術 | 役割 |
|---------|------|------|
| コンセンサス層 | Malachite (Tendermint BFT) | トランザクションの順序決定とブロック確定 |
| 実行層 | Reth (Rust製Ethereum実行クライアント) | 台帳管理、EVM実行、Fee Manager・Privacy Module等の拡張 |
実行層|	Reth (Rust製Ethereum実行クライアント)	|台帳管理、EVM実行、Fee Manager・Privacy Module等の拡張

## Arc上で実現できるもの

- オンチェーン信用・レンディング
- 資本市場の決済・トークン化担保
- ステーブルコインFX
- AIエージェントによる自律的商取引
- クロスボーダー決済・送金

# Circle SDKでできること

CircleからはUSDCの利便性を高めるために便利なSDKが出ています！

裏側ではCCTPなどのクロスチェーン技術が使用されています。

- ウォレットの作成・管理（Dev-Controlled Wallets SDK）
USDC/EURCの送金
- クロスチェーンでのUSDCブリッジ（Bridge Kit + CCTP）
- スマートコントラクトのデプロイ・操作・イベント監視（Smart Contract Platform SDK）

# サンプルコードを試してみよう！

ではここからは早速サンプルコードを試していきましょう！

## GitHubリポジトリ

https://github.com/mashharuki/Arc-Sample/tree/main/sdk-sample

## セットアップ

まずは依存関係をインストールします

```bash
bun install
```

次に環境変数用のファイルを作成します。

```bash
cp .env.example .env
```

まず最初にCircleの開発者コンソールにログインしてAPIキーを発行する必要があります。

```bash
API_KEY=
CIRCLE_ENTITY_SECRET=
```

その次に`EntitySecret`をセットする必要があります。

まず以下のスクリプトを実行して`EntitySecret`を生成させます。

```bash
bun run generate
```

うまくいけば以下のようになります！

```bash
================================================================
!!!! ENTITY SECRET: <ここに出力される> !!!!
================================================================
```

ちなみにスクリプトの中身は以下のようになっています！

```ts
import { generateEntitySecret } from "@circle-fin/developer-controlled-wallets";

/**
 * メイン関数
 */
const main = async () => { 
  // エンティティシークレットの生成
  generateEntitySecret();
};

main();
```

この値を環境変数として設定するほか、Circle 開発者コンソールの方にも設定する必要があるので以下のスクリプトを実行します。

```bash
bun run register 
```

これで準備OKです！

スクリプトの中身は以下のようになっています！

```ts
import { registerEntitySecretCiphertext } from "@circle-fin/developer-controlled-wallets";

const { API_KEY, CIRCLE_ENTITY_SECRET } = process.env;

if (!API_KEY || !CIRCLE_ENTITY_SECRET) {
  throw new Error("API_KEYまたはCIRCLE_ENTITY_SECRETが設定されていません。");
}

/**
 * メイン関数
 */
const main = async () => { 
  // エンティティシークレットを登録するメソッド
  const response = await registerEntitySecretCiphertext({
    apiKey: API_KEY,
    entitySecret: CIRCLE_ENTITY_SECRET,
    recoveryFileDownloadPath: "",
  });
  console.log(response.data?.recoveryFile);
};

main();
```

## ウォレット作成

いよいよCircleSDKを使ってウォレットを作っていきます！

```bash
bun run createWallet
```

そうすると以下のようにウォレットが作成されます！

```json
{
  walletData: [
    {
      id: "30cb80df-7b3d-5e4a-86c8-36bb11b77cc9",
      state: "LIVE",
      walletSetId: "e8e41a4b-fd7f-5f15-9293-3806f2fbb189",
      custodyType: "DEVELOPER",
      address: "0x22e24e551daa46183e5b41db72a54922f816c449",
      blockchain: "ARC-TESTNET",
      accountType: "EOA",
      updateDate: "2026-01-31T13:50:55Z",
      createDate: "2026-01-31T13:50:55Z",
    }, {
      id: "5a6fc874-3233-5fbd-bb92-7f7417b604c6",
      state: "LIVE",
      walletSetId: "e8e41a4b-fd7f-5f15-9293-3806f2fbb189",
      custodyType: "DEVELOPER",
      address: "0x7b6314ea59b46e4db01d882964c5ded58477f3ad",
      blockchain: "ARC-TESTNET",
      accountType: "EOA",
      updateDate: "2026-01-31T13:50:55Z",
      createDate: "2026-01-31T13:50:55Z",
    }
  ],
}
```

スクリプトの中身は以下のような感じです！

```ts
import { client } from "./sdk-config";

/**
 * メイン関数
 */
const main = async () => {
  // Create a wallet set
  const walletSetResponse = await client.createWalletSet({
    name: "Wallet Set 1",
  });

  // Create a wallet on Arc Testnet
  // blockchainsの部分で作成対象のブロックチェーンを選べる！
  const walletsResponse = await client.createWallets({
    blockchains: ["ARC-TESTNET", "ARB-SEPOLIA"],
    count: 2,
    walletSetId: walletSetResponse.data?.walletSet?.id ?? "",
  });

  const walletData = await walletsResponse.data?.wallets

  console.log({walletData});
}

main();
```

作成したウォレットの残高を確認するためにはSDKで提供されている`getWalletTokenBalance`メソッドを利用します！

```bash
bun run getBalance
```

以下のようになればOK!

```bash
=== WALLET_ID1の残高 ===
{
  "tokenBalances": []
}
=== WALLET_ID2の残高 ===
{
  "tokenBalances": []
}
```

スクリプトは以下のような感じです！

```ts
import { client } from "./sdk-config";

const {
  WALLET_ID1,
  WALLET_ID2,
} = process.env;

/**
 * メイン関数
 */
const main = async () => {
  // 残高を取得する
  const response = await client.getWalletTokenBalance({
    id: WALLET_ID1!,
  });

  const response2 = await client.getWalletTokenBalance({
    id: WALLET_ID2!,
  });

  console.log("=== WALLET_ID1の残高 ===");
  console.log(JSON.stringify(response.data, null, 2));

  console.log("=== WALLET_ID2の残高 ===");
  console.log(JSON.stringify(response2.data, null, 2));
};

main();
```

## USDCの送金

次にUSDCの送金を試してみようと思います。

試す前に各ウォレットにネイティブトークンとUSDCを入金しておく必要があります！

以下のスクリプトで実行できます。

```bash
bun run transfer
```

以下のようになればOKです！

```bash
{
  id: "65aa2774-df57-5d8a-a1d0-bc1eaeccaa2f",
  state: "INITIATED",
}
{
  transaction: {
    id: "65aa2774-df57-5d8a-a1d0-bc1eaeccaa2f",
    blockchain: "ARC-TESTNET",
    tokenId: "15dc2b5d-0994-58b0-bf8c-3a0501148ee8",
    walletId: "30cb80df-7b3d-5e4a-86c8-36bb11b77cc9",
    sourceAddress: "0x22e24e551daa46183e5b41db72a54922f816c449",
    destinationAddress: "0x7b6314ea59b46e4db01d882964c5ded58477f3ad",
    transactionType: "OUTBOUND",
    custodyType: "DEVELOPER",
    state: "INITIATED",
    transactionScreeningEvaluation: {
      screeningDate: "2026-01-31T14:15:00Z",
    },
    amounts: [ "0.1" ],
    nfts: null,
    networkFee: "",
    operation: "TRANSFER",
    feeLevel: "MEDIUM",
    refId: "",
    abiParameters: null,
    createDate: "2026-01-31T14:14:59Z",
    updateDate: "2026-01-31T14:15:00Z",
  },
}
```

スクリプトの中身は以下です。

SDKの`createTransaction`メソッドを使います。

```ts
import { client } from "./sdk-config";

const {
  WALLET_ID1,
  WALLET_ID2
} = process.env;

/**
 * メイン関数
 */
const main = async () => {
  // senderとreceiverのウォレット情報を取得する
  const senderWallet = await client.getWallet({
    id: WALLET_ID1!,
  });

  const receiverWallet = await client.getWallet({
    id: WALLET_ID2!,
  });

  // USDCを送金する
  const transferResponse = await client.createTransaction({
    amount: ["0.1"], // Transfer 0.1 USDC
    destinationAddress: receiverWallet!.data!.wallet.address!,
    tokenAddress: "0x3600000000000000000000000000000000000000", // USDC contract address on Arc Testnet
    blockchain: "ARC-TESTNET",
    walletAddress: senderWallet!.data!.wallet.address!,
    fee: {
      type: "level",
      config: {
        feeLevel: "MEDIUM",
      },
    },
  });

  console.log(transferResponse.data);

  const response = await client.getTransaction({
    id: transferResponse!.data!.id!,
  });
  console.log(response.data);

};

main();
```

## Bridgeを試す

では次にBridgeを試していこうと思います！

以下のコマンドで試せます。

```bash
bun run bridge
```

以下のようになればOKです！

```json
{
  state: 'success',
  amount: '0.1',
  token: 'USDC',
  source: {
    address: '0xadb0d5482f87fa230eb9bc9fe68c82cff90c28cd',
    chain: {
      type: 'evm',
      chain: 'Arc_Testnet',
      name: 'Arc Testnet',
      title: 'ArcTestnet',
      nativeCurrency: { name: 'USDC', symbol: 'USDC', decimals: 18 },
      chainId: 5042002,
      isTestnet: true,
      explorerUrl: 'https://testnet.arcscan.app/tx/{hash}',
      rpcEndpoints: [ 'https://rpc.testnet.arc.network/' ],
      eurcAddress: '0x89B50855Aa3bE2F677cD6303Cec089B5F319D72a',
      usdcAddress: '0x3600000000000000000000000000000000000000',
      cctp: {
        domain: 26,
        contracts: {
          v2: {
            type: 'split',
            tokenMessenger: '0x8FE6B999Dc680CcFDD5Bf7EB0974218be2542DAA',
            messageTransmitter: '0xE737e5cEBEEBa77EFE34D4aa090756590b1CE275',
            confirmations: 1,
            fastConfirmations: 1
          }
        }
      },
      kitContracts: { bridge: '0xC5567a5E3370d4DBfB0540025078e283e36A363d' }
    }
  },
  destination: {
    address: '0xadb0d5482f87fa230eb9bc9fe68c82cff90c28cd',
    chain: {
      type: 'evm',
      chain: 'Arbitrum_Sepolia',
      name: 'Arbitrum Sepolia',
      title: 'Arbitrum Sepolia Testnet',
      nativeCurrency: { name: 'Sepolia Ether', symbol: 'ETH', decimals: 18 },
      chainId: 421614,
      isTestnet: true,
      explorerUrl: 'https://sepolia.arbiscan.io/tx/{hash}',
      rpcEndpoints: [ 'https://sepolia-rollup.arbitrum.io/rpc' ],
      eurcAddress: null,
      usdcAddress: '0x75faf114eafb1BDbe2F0316DF893fd58CE46AA4d',
      cctp: {
        domain: 3,
        contracts: {
          v1: {
            type: 'split',
            tokenMessenger: '0x9f3B8679c73C2Fef8b59B4f3444d4e156fb70AA5',
            messageTransmitter: '0xaCF1ceeF35caAc005e15888dDb8A3515C41B4872',
            confirmations: 65
          },
          v2: {
            type: 'split',
            tokenMessenger: '0x8FE6B999Dc680CcFDD5Bf7EB0974218be2542DAA',
            messageTransmitter: '0xE737e5cEBEEBa77EFE34D4aa090756590b1CE275',
            confirmations: 65,
            fastConfirmations: 1
          }
        }
      },
      kitContracts: { bridge: '0xC5567a5E3370d4DBfB0540025078e283e36A363d' }
    }
  },
  steps: [
    {
      name: 'approve',
      state: 'success',
      txHash: '0x5f13bec0bbec421ad60c2390099bf47db6def6c19359af82657073297614dc00',
      data: {
        txHash: '0x5f13bec0bbec421ad60c2390099bf47db6def6c19359af82657073297614dc00',
        status: 'success',
        cumulativeGasUsed: 55696n,
        gasUsed: 55696n,
        blockNumber: 24592829n,
        blockHash: '0x0d01027da2ddfc33a989576bfe7e9474d02a98a0a9381c9cbed29b2dca8250ab',
        transactionIndex: 0,
        effectiveGasPrice: 90106009568n
      },
      explorerUrl: 'https://testnet.arcscan.app/tx/0x5f13bec0bbec421ad60c2390099bf47db6def6c19359af82657073297614dc00'
    },
    {
      name: 'burn',
      state: 'success',
      txHash: '0xe4c49619fd71494e073b62f493aa5aeb8b47309633c647d7350d36ba49c64df6',
      data: {
        txHash: '0xe4c49619fd71494e073b62f493aa5aeb8b47309633c647d7350d36ba49c64df6',
        status: 'success',
        cumulativeGasUsed: 742925n,
        gasUsed: 184683n,
        blockNumber: 24592838n,
        blockHash: '0xfd05d589dedc933f4db138c369d26545525b32f68543a2446b19ffeff35f3a37',
        transactionIndex: 7,
        effectiveGasPrice: 22000000000n
      },
      explorerUrl: 'https://testnet.arcscan.app/tx/0xe4c49619fd71494e073b62f493aa5aeb8b47309633c647d7350d36ba49c64df6'
    },
    {
      name: 'fetchAttestation',
      state: 'success',
      data: {
        attestation: '0x9454e141ed3e68bcb4a1109d8c19fc639f88fed4900de920777d871a01cef887683f126944eafd83a21278bc6df128b97093e77fdaa0adda875ca5139c0dcb731b4cd67b03aeae4920fec04e2b6b711fe83329f36341e5111e23ad321bcbc2114734462c4ba627ed1175a31bc3c3e756dcac816a6596ae0b74710fc0aad3de20ee1c',
        message: '0x000000010000001a00000003b8ced7e31f0b174b46f5623cff15fe16c41d8e0d6bdf0beed136c9fcb5315cdc0000000000000000000000008fe6b999dc680ccfdd5bf7eb0974218be2542daa0000000000000000000000008fe6b999dc680ccfdd5bf7eb0974218be2542daa0000000000000000000000000000000000000000000000000000000000000000000003e8000007d0000000010000000000000000000000003600000000000000000000000000000000000000000000000000000000000000adb0d5482f87fa230eb9bc9fe68c82cff90c28cd00000000000000000000000000000000000000000000000000000000000186a0000000000000000000000000c5567a5e3370d4dbfb0540025078e283e36a363d000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        eventNonce: '0xb8ced7e31f0b174b46f5623cff15fe16c41d8e0d6bdf0beed136c9fcb5315cdc',
        cctpVersion: 2,
        status: 'complete',
        decodedMessage: {
          sourceDomain: '26',
          destinationDomain: '3',
          nonce: '0xb8ced7e31f0b174b46f5623cff15fe16c41d8e0d6bdf0beed136c9fcb5315cdc',
          sender: '0x8fe6b999dc680ccfdd5bf7eb0974218be2542daa',
          recipient: '0x8fe6b999dc680ccfdd5bf7eb0974218be2542daa',
          destinationCaller: '0x0000000000000000000000000000000000000000000000000000000000000000',
          minFinalityThreshold: '1000',
          finalityThresholdExecuted: '2000',
          messageBody: '0x000000010000000000000000000000003600000000000000000000000000000000000000000000000000000000000000adb0d5482f87fa230eb9bc9fe68c82cff90c28cd00000000000000000000000000000000000000000000000000000000000186a0000000000000000000000000c5567a5e3370d4dbfb0540025078e283e36a363d000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
          decodedMessageBody: {
            burnToken: '0x3600000000000000000000000000000000000000',
            mintRecipient: '0xadb0d5482f87fa230eb9bc9fe68c82cff90c28cd',
            amount: '100000',
            messageSender: '0xc5567a5e3370d4dbfb0540025078e283e36a363d',
            maxFee: '0',
            feeExecuted: '0',
            expirationBlock: '0',
            hookData: null
          }
        },
        delayReason: null
      }
    },
    {
      name: 'mint',
      state: 'success',
      txHash: '0x58b1b9fd990b05734b99b96162b53a836f6122b61c2758d4306e7ebc271e480f',
      data: {
        txHash: '0x58b1b9fd990b05734b99b96162b53a836f6122b61c2758d4306e7ebc271e480f',
        status: 'success',
        cumulativeGasUsed: 192267n,
        gasUsed: 192267n,
        blockNumber: 238542600n,
        blockHash: '0xc2a611db6408d9e336e05c0a255e69138899a903bc7e7403f2c7424a19d6642c',
        transactionIndex: 1,
        effectiveGasPrice: 20054000n
      },
      explorerUrl: 'https://sepolia.arbiscan.io/tx/0x58b1b9fd990b05734b99b96162b53a836f6122b61c2758d4306e7ebc271e480f'
    }
  ],
  config: { transferSpeed: 'FAST' },
  provider: 'CCTPV2BridgingProvider'
}
```

ブロックエクスプローラー上でも結果が確認できます！

[Arbitrum Sepoliaのトランザクション - 0xadb0d5482f87fa230eb9bc9fe68c82cff90c28cd](https://sepolia.arbiscan.io/address/0xadb0d5482f87fa230eb9bc9fe68c82cff90c28cd)

スクリプトは以下の通りです。

SDKの`bridge`メソッドを実装

```ts
import { BridgeKit } from "@circle-fin/bridge-kit";
import { inspect } from "util";
import { adapter, client } from "./sdk-config";

const {
  WALLET_ID1,
} = process.env;

// Initialize the SDK
const kit = new BridgeKit();

/**
 * メイン関数
 */
const main = async () => {
  console.log("---------------Starting Bridging---------------");

  // senderとreceiverのウォレット情報を取得する
  const wallet = await client.getWallet({
    id: WALLET_ID1!,
  });

  try {
    // ArcからArbitrumへのブリッジを実行する
    const result = await kit.bridge({
      from: {
        adapter,
        chain: "Arc_Testnet",
        address: wallet.data!.wallet.address, // EVM address (developer-controlled)
      },
      to: {
        adapter,
        chain: "Arbitrum_Sepolia",
        address: wallet.data!.wallet.address, // EVM address (developer-controlled)
      },
      amount: "0.1",
    });

    console.log("RESULT", inspect(result, false, null, true));
    } catch (err) {
    console.log("ERROR", inspect(err, false, null, true));
  }
};

main();
```

## Crosschain送金

最後にクロスチェーン送金を試そうと思います！！

送金といっても実態は送信元のチェーンで`burn`しその分を送信先チェーンで`mint`しているということになっています。

ではまずウォレット作成から！

```bash
bun run crosschain:createWallet
```

以下のようになればOKです!

今回は一気に4種類のブロックチェーン上にウォレットを作成します。

```json
{
  walletData: [
    {
      id: "db398d05-9ec3-585c-adb2-2ac3fe12cf16",
      state: "LIVE",
      walletSetId: "d17f6615-3306-547e-a5ff-23255bf3d275",
      custodyType: "DEVELOPER",
      refId: "source-depositor",
      name: "",
      address: "0x3f7cb60bc138cf13c3aae1bef4d1f429ec42fd70",
      blockchain: "ARC-TESTNET",
      accountType: "EOA",
      updateDate: "2026-02-02T00:31:54Z",
      createDate: "2026-02-02T00:31:54Z",
    }, {
      id: "feeb44c5-7b35-5755-b7cc-4b7b53864d6c",
      state: "LIVE",
      walletSetId: "d17f6615-3306-547e-a5ff-23255bf3d275",
      custodyType: "DEVELOPER",
      refId: "source-depositor",
      name: "",
      address: "0x3f7cb60bc138cf13c3aae1bef4d1f429ec42fd70",
      blockchain: "AVAX-FUJI",
      accountType: "EOA",
      updateDate: "2026-02-02T00:31:54Z",
      createDate: "2026-02-02T00:31:54Z",
    }, {
      id: "c14f3aa0-3982-5880-8439-9a36b6b3c121",
      state: "LIVE",
      walletSetId: "d17f6615-3306-547e-a5ff-23255bf3d275",
      custodyType: "DEVELOPER",
      refId: "source-depositor",
      name: "",
      address: "0x3f7cb60bc138cf13c3aae1bef4d1f429ec42fd70",
      blockchain: "BASE-SEPOLIA",
      accountType: "EOA",
      updateDate: "2026-02-02T00:31:54Z",
      createDate: "2026-02-02T00:31:54Z",
    }, {
      id: "922fcab9-e60d-5f01-9165-67b19b2d5f6a",
      state: "LIVE",
      walletSetId: "d17f6615-3306-547e-a5ff-23255bf3d275",
      custodyType: "DEVELOPER",
      refId: "source-depositor",
      name: "",
      address: "0x3f7cb60bc138cf13c3aae1bef4d1f429ec42fd70",
      blockchain: "ETH-SEPOLIA",
      accountType: "EOA",
      updateDate: "2026-02-02T00:31:54Z",
      createDate: "2026-02-02T00:31:54Z",
    }
  ],
}
```

生成された4つのウォレットIDは環境変数に登録する

```bash
CROSSCHAIN_WALLET_ID1=
CROSSCHAIN_WALLET_ID2=
CROSSCHAIN_WALLET_ID3=
CROSSCHAIN_WALLET_ID4=
```

生成後にウォレットアドレスに対して`ネイティブトークン`と`USDC`をそれぞれ送金する必要があるので注意です！

残高取得は以下のコマンドを実行すればOKです！

```bash
bun run crosschain:getBalance
```

以下のようになればOKです！

```bash
=== CROSSCHAIN_WALLET_ID1の残高 ===
{
  "tokenBalances": []
}
=== CROSSCHAIN_WALLET_ID2の残高 ===
{
  "tokenBalances": []
}
=== CROSSCHAIN_WALLET_ID3の残高 ===
{
  "tokenBalances": []
}
=== CROSSCHAIN_WALLET_ID4の残高 ===
{
  "tokenBalances": []
}
```

次にクロスチェーン転送するためにGatewayコントラクトにUSDCをdepositします。

```bash
bun run crosschain:deposit -- base avalanche
# 他のチェーンの場合は以下
bun run crosschain:deposit -- arc ethereum
bun run crosschain:deposit -- arc op unichain
```

以下のようになればOKです!

```bash
--- Arc Testnet ---
Approving 2 USDC for spender 0x0077777d7EBA4688BDeF3E311b846F25870A19B9
Waiting for USDC approve (txId=6324ffaf-4872-5cfa-b3f7-ce2c39c7dbea)
..
USDC approve final state: COMPLETE
Depositing 2 USDC to Gateway Wallet
Waiting for Gateway deposit (txId=272af8ca-252e-585c-8fc4-8c0470cdd247)
..
Gateway deposit final state: COMPLETE

--- Ethereum Sepolia ---
Approving 2 USDC for spender 0x0077777d7EBA4688BDeF3E311b846F25870A19B9
Waiting for USDC approve (txId=21aefe3c-8dd0-598f-9d8c-d238dd706073)
......
USDC approve final state: CONFIRMED
Depositing 2 USDC to Gateway Wallet
Waiting for Gateway deposit (txId=c2694599-26dc-527e-91a3-9e724a32ae4a)
...........
Gateway deposit final state: CONFIRMED
Transaction complete. Once finality is reached, Gateway credits your unified USDC balance.
```

実施後にGatewayコントラクトの残高を確認すると増えているはずです！

```bash
bun run crosschain:getGatewayBalance
```

以下のようになっているはず

```bash
Depositor address: 0x3f7cb60bc138cf13c3aae1bef4d1f429ec42fd70
  - Ethereum Sepolia: 2.000000 USDC
  - Avalanche Fuji: 2.000000 USDC
  - Base Sepolia: 2.000000 USDC
  - Arc Testnet: 2.000000 USDC
Unified USDC available: 8.000000 USDC
```

最後にクロスチェーン転送を試してみます！

Ethereum Sepolia、 Avalanche Fuji、 Arc TestnetからBase Sepoliaに1USDCを転送するには以下ようにスクリプトを実行します！

```bash
# 一気に複数チェーンやる場合
bun run crosschain:transfer -- arc op unichain
```

すると以下のようにログが出力されるはずです！！

```bash
Mint tx submitted: 4eea00c4-ef54-5aa3-a19b-4160f0534f09
Waiting for USDC mint (txId=4eea00c4-ef54-5aa3-a19b-4160f0534f09)
......
USDC mint final state: CONFIRMED
Minted 0.1 USDC
```

# まとめ

今回は以上となります。

USDCを皮切りにクロスチェーンブリッジ・送金のためのAPI、SDKを提供してからのArcの公開という流れは素晴らしいですね。

ステーブルコイン熱が世界で高まる中、ステーブルコインをネイティブトークンにしたブロックチェーンの需要が確実に高まってくるはずですし、他のブロックチェーンエコシステムから孤立しないようにしっかりとインフラ基盤を固めてからブロックチェーンを出したCircle社の戦略は非常に参考になると思いました。

今後は多くのプロダクトでCircleのSDKの採用事例が増えていくものと思われます。

最後まで読んでいただきありがとうございました！

# 参考文献
- [Circle公式サイト](https://www.circle.com/)
- [チュートリアル](https://docs.arc.network/arc/tutorials/bridge-usdc-to-arc)