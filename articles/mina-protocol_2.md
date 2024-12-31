---
title: "o1jsを使って署名・検証が試せるZKアプリを動かしてみた！"
emoji: "🛠"
type: "tech"
topics: ["Web3", "Blockchain", "ゼロ知識証明", "TypeScript", "zk"]
published: true
---

![](/images/mina-protocol_2/0.jpeg)

## はじめに

皆さん、こんにちは。

今回は、**MinaProtocol** というブロックチェーンをテーマにした記事を執筆していこうと思います！

現在ハッカソンプラットフォーム**Akindo**と**MinaProtocol**のチームがタッグ組んで WaveHack というプログラムを実施中です！

https://app.akindo.io/wave-hacks/ENw9p7R6nUz818lo1

**WaveHack** ってなんだという方は以下の記事をご参照ください！

ファウンダーである金城さんの想いがまとめられています！！！

https://note.com/shinkinjo/n/n313d1e931ebf

## Mina Protocol とは

Mina Protocol は O(1)Labs により 2017 年 6 月から開発されている L1 のスマートコントラクトプラットフォームです。

https://minaprotocol.com/

**o1js** というライブラリを使って **TypeScript** でスマートコントラクトを実装することができます！！

https://docs.minaprotocol.com/zkapps/o1js

また、ただのスマートコントラクトではなくゼロ知識証明をフル活用した **ZK App**を開発することができるプロトコルになっています！！

## 今回使うコード

今回使うコードは以下に格納されています。

https://github.com/mashharuki/mina-protocol-workshop-slides/tree/2024-devcon-main

Fork 元のコードは **Devcon** 期間中に開催されたワークショップのコードです！

https://lu.ma/ua6yov8a?tk=9QSuVq

コードの構造としては、フロントエンドとバックエンドが綺麗に分かれています。

```bash
.
├── LICENSE
├── README.md
├── ui
└── zk
```

バックエンドのロジック用ファイルを格納している `zk` フォルダの中身は以下の通りです。

この後のコードの解説では、 `ethSignatureProgram.ts`をメインに解説していきます！

```bash
.
├── babel.config.cjs
├── bun.lockb
├── config.json
├── package.json
├── src
│   ├── ethSignatureProgram.test.ts
│   └── ethSignatureProgram.ts
├── tsconfig.json
└── vitest.config.ts
```

フロントエンド用の `ui`フォルダの中身は以下の通りです！

**Next.js**を使って構築されています。

```bash
.
├── README.md
├── app
│   ├── components
│   ├── layout.tsx
│   ├── page.tsx
│   ├── zkWorker.ts
│   └── zkWorkerClient.ts
├── bun.lockb
├── global.d.ts
├── next.config.ts
├── package.json
├── postcss.config.mjs
├── public
│   └── assets
├── styles
│   ├── Home.module.css
│   └── globals.css
├── tailwind.config.ts
└── tsconfig.json
```

## コードの解説

ではコードの解説にうつります！

- **バックエンドの解説**

  ではまず署名データを検証する ZK サーキット用のファイルの解説を行います！

  :::message
  **ethSignatureProgram.ts** の中身です。
  :::

  普通の TypeScript のコードを書く感じで ZK サーキットを実装できる点が、 MinaProtocol の最大のポイントですね！

  ```ts
  import {
    Bool,
    Bytes,
    createEcdsa,
    createForeignCurve,
    Crypto,
    ZkProgram,
  } from "o1js";

  class Secp256k1 extends createForeignCurve(Crypto.CurveParams.Secp256k1) {}
  class ECDSA extends createEcdsa(Secp256k1) {}
  class Bytes32 extends Bytes(32) {}

  /**
   * 署名データを検証するためのZK回路
   */
  export const EthSignatureProgram = ZkProgram({
    name: "EthSignatureProgram",
    publicInput: Bytes32, // インプット
    publicOutput: Bool, // アウトプット
    methods: {
      // 検証用のメソッドを定義。使用するアルゴリズムなどを指定。
      // 今回は、verifySignatureというメソッドを定義している。
      verifySignature: {
        privateInputs: [ECDSA, Secp256k1],
        async method(message: Bytes32, signature: ECDSA, publicKey: Secp256k1) {
          return {
            // 戻り値して、検証結果のみを返す。
            publicOutput: signature.verifyEthers(message, publicKey),
          };
        },
      },
    },
  });
  ```

  今回はテストコードも用意されていました！

  ```ts
  import { Wallet } from "ethers";
  import { Bytes, createEcdsa, createForeignCurve, Crypto } from "o1js";
  import { beforeAll, describe, expect, it } from "vitest";
  import { EthSignatureProgram } from "./ethSignatureProgram.js";

  class Secp256k1 extends createForeignCurve(Crypto.CurveParams.Secp256k1) {}
  class ECDSA extends createEcdsa(Secp256k1) {}
  class Bytes32 extends Bytes(32) {}

  /**
   * ZK回路を使用して、署名データを検証するためのテスト
   */
  describe("EthSignatureProgram", () => {
    // Padding the messages to 32 bytes so that both signing libraries handle them the same
    const message = "Hello, world!".padEnd(32, "0");
    const spoofedMessage = "Goodbye, world!".padEnd(32, "0");

    // Convert ethereum public key to o1js Secp256k1 point
    const ethWallet = Wallet.createRandom();
    const compressedPublicKey = ethWallet.signingKey.compressedPublicKey;
    const publicKey = Secp256k1.fromEthers(compressedPublicKey);

    beforeAll(async () => {
      // ZKサーキットをコンパイル
      await EthSignatureProgram.compile();
    });

    it("should verify a valid signature", async () => {
      // 署名データを作成
      const ethSignature = await ethWallet.signMessage(message);
      // proofを作成(元のメッセージ、署名データ、公開鍵を使う。)
      const proof = (
        await EthSignatureProgram.verifySignature(
          Bytes32.fromString(message),
          ECDSA.fromHex(ethSignature),
          publicKey
        )
      ).proof;
      // 問題なく検証されたことを確認する。
      expect(proof.publicOutput.toBoolean()).toBe(true);
    });
    it("should not verify an invalid signature", async () => {
      const ethSignature = await ethWallet.signMessage(message);
      // 異なる署名データを与える。(元の署名データを変える。)
      const proof = (
        await EthSignatureProgram.verifySignature(
          Bytes32.fromString(spoofedMessage),
          ECDSA.fromHex(ethSignature),
          publicKey
        )
      ).proof;
      //署名データが異なるので検証が失敗することを確認する。
      expect(proof.publicOutput.toBoolean()).toBe(false);
    });
  });
  ```

  今回は非常にシンプルなロジックとなっています！

- **フロントエンドの解説**

  ではここからフロントエンドの解説にうつります！！

  :::message
  以下、3 つのファイルの中身を解説していきます！

  - **zkWorker.ts**
  - **zkWorkerClient.ts**
  - **page.tsx**
    :::

  - **zkWorker.ts** について

    zkWorker.ts には、ZK サーキットの機能を呼び出すロジックが実装されています！

    バックエンドのセクションで紹介した ZK サーキットのプログラムをロードしコンパイルする実装などがあります。

    そして今回のキモとなる 検証用のメソッドを呼び出す API も実装しています。

    ```ts
    import * as Comlink from "comlink";
    import { Bytes, Crypto, Mina, createEcdsa, createForeignCurve } from "o1js";
    import type { EthSignatureProgram } from "../../zk/build/src/ethSignatureProgram.js";

    const state = {
      zkProgram: null as null | typeof EthSignatureProgram,
    };

    class Secp256k1 extends createForeignCurve(Crypto.CurveParams.Secp256k1) {}
    class ECDSA extends createEcdsa(Secp256k1) {}
    class Bytes32 extends Bytes(32) {}

    /**
     * ZK回路操作関連のAPI
     */
    export const api = {
      /**
       * デフォルトのMinaインスタンスをDevnetに設定します。
       */
      async setActiveInstanceToDevnet() {
        const Network = Mina.Network(
          "https://api.minascan.io/node/devnet/v1/graphql"
        );
        console.log("Devnet network instance configured");
        Mina.setActiveInstance(Network);
      },
      /**
       * プログラムをロードします。
       */
      async loadProgram() {
        const { EthSignatureProgram } = await import(
          "../../zk/build/src/ethSignatureProgram.js"
        );
        state.zkProgram = EthSignatureProgram;
      },
      /**
       * プログラムをコンパイルします。
       */
      async compileProgram() {
        await state.zkProgram!.compile();
      },
      /**
       * 署名を検証するためのメソッド
       * @param message
       * @param ethSignature
       * @param ethPublicKey
       * @returns
       */
      async verifySignature(
        message: string,
        ethSignature: string,
        ethPublicKey: string
      ) {
        const messageBytes = Bytes32.fromString(message);
        const signature = ECDSA.fromHex(ethSignature);
        const publicKey = Secp256k1.fromEthers(ethPublicKey);
        // 検証
        const result = await state.zkProgram!.verifySignature(
          messageBytes,
          signature,
          publicKey
        );
        // 検証結果を取得
        const valid = result.proof.publicOutput.toBoolean();
        if (!valid) {
          console.error("Invalid signature");
          return {
            valid: false,
            proof: result.proof.toJSON(),
          };
        }

        return {
          valid: true,
          proof: result.proof.toJSON(),
        };
      },
    };

    // Expose the API to be used by the main thread
    Comlink.expose(api);
    ```

  - **zkWorkerClient.ts** について

    このファイルは、一つ前に紹介した ZK サーキット周りの機能を呼び出す API を扱うためのクラスを定義しているファイルです。

    ここで実装したクラスをインスタンス化して `page.tsx`で利用しています！

    ```ts
    import * as Comlink from "comlink";

    /**
     * ZkWorkerCllient Class
     */
    export default class ZkWorkerCllient {
      // ---------------------------------------------------------------------------------------
      worker: Worker;
      // Proxy to interact with the worker's methods as if they were local
      remoteApi: Comlink.Remote<typeof import("./zkWorker").api>;

      constructor() {
        // Initialize the worker from the zkappWorker module
        const worker = new Worker(new URL("./zkWorker.ts", import.meta.url), {
          type: "module",
        });
        this.worker = worker;
        // Wrap the worker with Comlink to enable direct method invocation
        this.remoteApi = Comlink.wrap(worker);
      }

      async loadProgram() {
        return this.remoteApi.loadProgram();
      }

      async compileProgram() {
        return this.remoteApi.compileProgram();
      }

      async verifySignature(
        message: string,
        ethSignature: string,
        ethPublicKey: string
      ) {
        console.log("Verifying signature...");
        console.log("Message: ", message);
        console.log("Signature: ", ethSignature);
        console.log("Public key: ", ethPublicKey);
        return this.remoteApi.verifySignature(
          message,
          ethSignature,
          ethPublicKey
        );
      }
    }
    ```

    ここで来たらいよいよフロントエンドから呼び出す準備が整いました！

  - **page.tsx** について

    一つ前に紹介した`ZkWorkerCllient`クラスをインスタンス化して検証できるようにしています！

    そして、レンダリング時に ZK サーキット用のプログラムをロード＆コンパイルして使えるようにしています！

    メッセージの署名は `ethers.js`で提供されているメソッドを利用します。

    ```ts
    "use client";
    import { ethers, SigningKey } from "ethers";
    import Head from "next/head";
    import Image from "next/image";
    import { JsonProof } from "o1js";
    import { useEffect, useState } from "react";
    import heroMinaLogo from "./../public/assets/hero-mina-logo.svg";
    import styles from "./../styles/Home.module.css";
    import GradientBG from "./components/GradientBG.js";
    import ZkWorkerClient from "./zkWorkerClient";

    /**
     * home component
     * @returns
     */
    export default function Home() {
      const [zkWorkerClient] = useState(new ZkWorkerClient());
      const [hasBeenCompiled, sethasBeenCompiled] = useState(false);
      const [isVerifying, setIsVerifying] = useState(false);
      const [isVerified, setIsVerified] = useState<boolean | null>(null);
      const [proof, setProof] = useState<JsonProof | null>(null);

      const [connected, setConnected] = useState(false);
      const [ethWalletAddress, setEthAddress] = useState("");
      const [ethSigner, setEthSigner] = useState<ethers.JsonRpcSigner | null>(
        null
      );

      const [message, setMessage] = useState("");
      const [ethSignature, setEthSignature] = useState("");

      function shortenString(str: string) {
        return `${str.slice(0, 20)}...${str.slice(-6)}`;
      }

      /**
       * Function to connect/disconnect the wallet
       */
      async function connectEthWallet() {
        if (!connected) {
          // Connect the wallet using ethers.js
          const provider = new ethers.BrowserProvider(window.ethereum);
          const signer = await provider.getSigner();
          const address = await signer.getAddress();

          setConnected(true);
          setEthAddress(address);
          setEthSigner(signer);
        } else {
          // Disconnect the wallet
          window.ethereum.selectedAddress = null;
          setConnected(false);
          setEthAddress("");
          setEthSigner(null);
        }
      }

      /**
       * 署名データから公開鍵を取得する。
       * @returns
       */
      async function getPublicKeyFromSignature() {
        const address = ethWalletAddress;
        console.log("Wallet Address:", address);

        // Hash the message (to match Ethereum's signing behavior)
        const paddedMessage = message.padEnd(32, "0");
        const messageHash = ethers.hashMessage(paddedMessage);
        // メッセージハッシュと署名データから公開鍵を復元する。
        const ethPublicKey = SigningKey.recoverPublicKey(
          messageHash,
          ethSignature
        );
        const compressedPublicKey = SigningKey.computePublicKey(
          ethPublicKey,
          true
        );

        // The public key is in uncompressed form (starts with "04" prefix)
        console.log("Recovered Public Key:", compressedPublicKey);
        return compressedPublicKey;
        // return ethWallet.signingKey.compressedPublicKey;
      }

      /**
       * メッセージから署名データを作成する。
       * @param message
       * @returns
       */
      async function signMessageEthers(message: string) {
        const paddedMessage = message.padEnd(32, "0");
        const provider = new ethers.BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();
        // 署名データを作成する。
        const ethSignature = await signer.signMessage(paddedMessage);
        console.log("signing message with ethers.js");
        console.log("message:", paddedMessage);
        setEthSignature(ethSignature);
        return ethSignature;
      }

      /**
       * メッセージを渡して検証する。
       * @param message
       * @returns
       */
      async function verifyMessageMina(message: string) {
        const paddedMessage = message.padEnd(32, "0");
        // 署名データから公開鍵を取得する。
        const ethPublicKey = await getPublicKeyFromSignature();
        // 検証する。
        const result = await zkWorkerClient.verifySignature(
          paddedMessage,
          ethSignature,
          ethPublicKey
        );
        return result;
      }

      useEffect(() => {
        (async () => {
          console.log("compiling...");
          // プログラムをロードしてコンパイルする
          await zkWorkerClient.loadProgram();
          await zkWorkerClient.compileProgram();
          console.log("compiled!");

          sethasBeenCompiled(true);
        })();
      }, [zkWorkerClient, sethasBeenCompiled]);

      return (
        <>
          <Head>
            <title>Eth to Mina Signature Verification Example</title>
            <meta name="description" content="built with o1js" />
            <link rel="icon" href="/assets/favicon.ico" />
          </Head>
          <GradientBG>
            <main className={styles.main}>
              <div className={styles.center}>
                <a
                  href="https://minaprotocol.com/"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Image
                    className={styles.logo}
                    src={heroMinaLogo}
                    alt="Mina Logo"
                    width="191"
                    height="174"
                    priority
                  />
                </a>
                <p className={styles.tagline}>
                  built with &nbsp;
                  <code className="font-weight-bold">o1js</code>
                </p>
                <div className="pt-10">
                  <p className="text-black text-shadow-white text-2xl">
                    Eth to Mina Signature Verification Example
                  </p>
                  <div>
                    <button
                      className="mt-4 mb-4 w-full text-lg text-white font-bold rounded-lg p-2 bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-700 hover:to-blue-900"
                      onClick={connectEthWallet}
                    >
                      {connected
                        ? "Disconnect Eth Wallet"
                        : "Connect Eth Wallet"}
                    </button>
                  </div>
                  {connected && (
                    <div className="p-4 bg-gray-100 rounded-lg shadow-md mb-10">
                      <p className="mb-4 text-lg font-semibold text-gray-700">
                        Connected eth wallet address: {ethWalletAddress}
                      </p>
                      <div className="flex flex-col space-y-4">
                        <input
                          id="message"
                          type="text"
                          placeholder="Message to sign"
                          value={message}
                          onChange={(e) => setMessage(e.target.value)}
                          className="p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <button
                          className="mt-4 mb-4 w-full text-lg text-white font-bold rounded-lg p-2 bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-700 hover:to-blue-900"
                          onClick={async () => {
                            const ethSignature = await signMessageEthers(
                              message
                            );
                            console.log(ethSignature);
                          }}
                        >
                          Sign Message Ethers
                        </button>
                      </div>
                    </div>
                  )}
                  {!!ethSignature && (
                    <div className="p-4 bg-gray-100 rounded-lg shadow-md">
                      {!hasBeenCompiled && (
                        <div>
                          <p className="mb-4 text-lg font-semibold text-gray-700">
                            Compiling zkProgram...
                          </p>
                        </div>
                      )}
                      {hasBeenCompiled && (
                        <div>
                          <p className="mb-4 text-lg font-semibold text-gray-700">
                            Signature: {shortenString(ethSignature)}
                          </p>
                          <p className="mb-4 text-lg font-semibold text-gray-700">
                            Public Key: {ethWalletAddress}
                          </p>
                          <p className="mb-4 text-lg font-semibold text-gray-700">
                            Message: {message}
                          </p>
                          <button
                            className="mt-4 mb-4 w-full text-lg text-white font-bold rounded-lg p-2 bg-gradient-to-r from-purple-500 to-purple-700 hover:from-purple-700 hover:to-purple-900"
                            onClick={async () => {
                              if (hasBeenCompiled) {
                                setIsVerifying(true);
                                const result = await verifyMessageMina(message);
                                console.log(result);
                                setIsVerified(result.valid);
                                setProof(result.proof);
                                setIsVerifying(false);
                              } else {
                                console.log("zkProgram not compiled yet");
                              }
                            }}
                          >
                            Verify Signature o1js
                          </button>
                          {isVerifying && (
                            <div>
                              <p className="mb-4 text-lg font-semibold text-gray-700">
                                Verifying signature...
                              </p>
                            </div>
                          )}
                          {!isVerifying && isVerified !== null && (
                            <div className="overflow-scroll max-w-xl">
                              <p className="mb-4 text-lg font-semibold text-gray-700">
                                Verification:{" "}
                                {isVerified ? "Success" : "Failed"}
                              </p>
                              <p className="mb-4 text-lg font-semibold text-gray-700">
                                Public Output:
                              </p>
                              <pre className="bg-gray-200 p-4 rounded-lg max-w-3/4 mx-auto whitespace-pre-wrap break-words">
                                {proof?.publicOutput || ""}
                              </pre>
                              <p className="mb-4 text-lg font-semibold text-gray-700">
                                Public Input:
                              </p>
                              <pre className="bg-gray-200 p-4 rounded-lg max-w-3/4 mx-auto whitespace-pre-wrap break-words">
                                {proof?.publicInput || ""}
                              </pre>
                              <p className="mb-4 text-lg font-semibold text-gray-700">
                                Proof:
                              </p>
                              <pre className="bg-gray-200 p-4 rounded-lg max-w-3/4 mx-auto whitespace-pre-wrap break-words">
                                {proof?.proof || ""}
                              </pre>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </main>
          </GradientBG>
        </>
      );
    }
    ```

    長かったですが、フロントエンドの実装は以上になります！

## 動かし方

ここからは紹介したコードを動かす具体的な方法を解説していきたいと思います！！

- **動かし方(ZK サーキット側)**

  - 依存関係のインストール

    ```bash
    cd zk && bun install
    ```

  - ZK サーキットのテスト

    ```bash
    bun run test
    ```

  - ZK サーキットのビルド

    ```bash
    bun run build
    ```

- **動かし方(フロントエンド)**

  - 依存関係のインストール

    ```bash
    cd ui && bun install
    ```

  - ローカルでの起動方法

    ```bash
    bun run dev
    ```

    問題なければ、 localhost:3000 でアプリにアクセスできます！！

    ![](/images/mina-protocol_2/0_2.jpg)

    ウォレットを接続すると以下のような画面に切り替わります！

    ![](/images/mina-protocol_2/1.png)

    適当に署名用のメッセージを記入して署名してしまいましょう！

    ![](/images/mina-protocol_2/2.png)

    署名にはしばらく時間がかかります！

    ![](/images/mina-protocol_2/3.png)

    署名が問題なく終われば以下のような表示に切り替わります！

    ![](/images/mina-protocol_2/4.jpg)

    **Verify Signature O1js** ボタンを押して検証してみましょう！！

    検証にも時間がかかりますが、問題なければ以下のように **Success** と表示されるはずです！！！

    ![](/images/mina-protocol_2/5.png)

長かったですが、動かし方についての解説はここまでになります！

## もっと MinaProtocol を学びたい人は・・・

この記事を読んでもっと MinaProtocol を勉強したいと思った人は以下の Youtube が参考になります！

https://www.youtube.com/watch?v=LLule5GUkkg&t=4116s

https://www.youtube.com/watch?v=hEHxBJNWkJo

https://www.youtube.com/live/_sklhKIPobM

## 参考文献

今回のコードを実装する上で参考になった文献のリンクを共有します！

1. [writing-a-zkapp](https://docs.minaprotocol.com/zkapps/writing-a-zkapp)
2. [zkapp-development-frameworks](https://docs.minaprotocol.com/zkapps/zkapp-development-frameworks)
3. [GitHub - mina-fungible-token](https://github.com/MinaFoundation/mina-fungible-token)
4. [Mina Fungible Token Documentation](https://minafoundation.github.io/mina-fungible-token/deploy.html)
5. [examples/zkapps/](https://github.com/o1-labs/docs2/tree/main/examples/zkapps/)
6. [Mina Foundation Online Workshop for Building ZKApps with o1js](https://www.youtube.com/watch?v=LLule5GUkkg&t=4116s)
7. [作成した開発用ウォレット](https://minascan.io/devnet/tx/5JuPC4hhNb83ufKmuRtj97jSSbdDURLTwTb6vmJL6k3Bv7Zi6uA7)
8. [ファウセット用リンク](https://faucet.minaprotocol.com/?address=B62qoFHxcia11kauLdy6f9B8yfB9QUkMRDTJhrXoKEgkuDzDSGU9MgU&explorer=minascan)
9. [mina-fungible-token Docs](https://minafoundation.github.io/mina-fungible-token/)
10. [interacting-with-zkapps-server-side](https://docs.minaprotocol.com/zkapps/tutorials/interacting-with-zkapps-server-side)
11. [Tutorial 4: Build a zkApp UI in the Browser with React](https://docs.minaprotocol.com/zkapps/tutorials/zkapp-ui-with-react)
12. [GitHub - o1-labs-XT/workshop-slides](https://github.com/o1-labs-XT/workshop-slides/tree/main)
