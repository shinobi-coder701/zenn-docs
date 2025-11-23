---
title: "【実践編】Midnight徹底解説：Compactでスマートコントラクト開発はじめ方！"
emoji: "🔐"
type: "tech" 
topics: ["blockchain", "cardano", "typescript", "privacy", "zkp"]
published: false
---

![](/images/cardano_midnight_1/0.png)

## はじめに：ブロックチェーンの「透明すぎる」問題

Bitcoinのホワイトペーパーが登場して以来、ブロックチェーン技術は「トラストレス」と「透明性」そして「対改ざん性」を強みとして、金融からサプライチェーンまで様々な分野に革命をもたらしてきました。

https://bitcoin.org/bitcoin.pdf

誰もが分散した同じ内容の台帳を検証できることで、中央集権的な管理者を必要としないトラスト（信頼）のネットワークを築き上げる現実的な方法を打ち出したことはまさに革命的でした。

しかし、その「完全な透明性」は時として大きな弱点となります。

- **企業の機密情報**が競合他社に漏洩してしまったら？
- **個人の金融取引履歴**が世界中に公開されてしまったら？
- **プライベートな医療情報や投票履歴**が誰でも閲覧可能だったら？

考えただけでも恐ろしいですよね。

この「透明すぎる」問題こそが、パブリックブロックチェーン技術がエンタープライズ領域や個人の日常に広く浸透するのを阻む、大きな壁の一つとなっていました。

このジレンマを解決するため、**Cardano**エコシステムから画期的なプロジェクトが登場しました。

それが**Midnight**です。

https://www.midnight.network/

:::message
Midnightはデータ保護とプライバシーに特化したCardanoのサイドチェーンです。
:::

ゼロ知識証明（ZKP）[^1]という最先端の暗号技術を活用し、 **「証明したい事実だけを、それ以外の情報を一切明かさずに証明する」** ことを可能にします。

:::message
ゼロ知識証明はプライバシー保護の観点でよく言及される技術ですが、用途次第では計算コストの圧縮にも活用できます！

代表的な活用事例は EVM系のL2チェーン実現のアプローチとして存在する**ZkEVM**や**INTMAX**があります。

https://intmax.io/
:::

先日ロンドンにて開催された**Midnight Hackathon**参加のためにCompactのことを調べたので、この記事ではその学びをシェアするため環境構築からコントラクトの実装、テスト、デプロイまで、ハンズオン形式で徹底的に解説しています！

https://midnightsummit.io/

Midnightの概要から知りたいという方は以下の記事を参照ください！

https://zenn.dev/mashharuki/articles/midnight_zkp-1

> [^1]: ゼロ知識証明（Zero-Knowledge Proof）とは、ある命題が真であることを、それ以外の情報（なぜ真であるかなど）を一切伝えることなく証明できる暗号学的な手法です。

## Compact言語：TypeScriptで書けるプライベートスマートコントラクト

Midnightの革新性を支えるもう一つの柱が、スマートコントラクト言語「**Compact**」です。

:::message
「ゼロ知識証明なんて、一部の暗号学者にしか扱えないのでは？」
:::

Compactは、そのハードルを劇的に下げるために設計されています。

### TypeScriptベースの構文

Compactの最大の特徴は、**TypeScriptをベースにしたドメイン固有言語（DSL）** である点です。

これにより世界中の膨大な数のWeb開発者が新たな言語をゼロから学ぶことなく、慣れ親しんだ構文でプライバシー保護アプリケーションを開発できるされています(実際には色々調べることになりましたが笑)。

Compactコンパイラが、開発者が書いたロジックを自動的にゼロ知識証明の生成に必要な暗号コンポーネントに変換してくれるため、開発者はZKPの複雑な数学を意識する必要がありません。

### データの3つの状態：Public, Private, Witness

Compactにおけるデータ管理の核心は、データのプライバシーレベルを明確に区別することにあります。

データは主に3つの状態で扱われます。

```mermaid
graph TD
    subgraph "ユーザーのオフチェーン環境"
        A[🔏 private: プライベート状態<br>（例: 個人のCounter値）] --> B;
    end
    subgraph "トランザクション入力"
        B[🤝 witness: 証明<br>（例: 「私の前の値は5でした」）] --> C{回路の実行};
    end
    subgraph "Midnightブロックチェーン（オンチェーン）"
         D[📢 public: 公開状態<br>（例: 全体の更新回数）] --> C;
    end
    C --> E[新しいPublic State];
    C --> F[新しいPrivate State];
    E --> D;
    F --> A;
```

1.  **`public` (公開状態)**
    - ブロックチェーン上に公開され、誰でも閲覧可能なデータです。
    - 従来のスマートコントラクトの状態変数に似ています。
    - `ledger` キーワードを使って定義されます。

2.  **`private` (プライベート状態)**
    - ユーザーのローカル環境（オフチェーン）でのみ管理される、秘匿されたデータです。
    - このデータそのものがブロックチェーンに記録されることはありません。
    - `private` キーワードで定義されます。

3.  **`witness` (証明)**
    - トランザクション実行時に、ユーザーが「私はこのデータを知っている」と証明するために提供する入力値です。
    - `private` な状態を更新する際の根拠として使われます。
    - `witness` キーワードで定義されます。

### 基本的な文法とCounterスマートコントラクトの例

これらの概念を、簡単なCounterスマートコントラクトの例で見ていきましょう。

このコントラクトはただ数字を加算していくだけという非常にシンプルなコードとなっており、公式のチュートリアルでも紹介されています。


このコントラクトには、

- 公開台帳に保存されるステート変数
- 上記ステート変数を加算するメソッド

が含まれます。

```typescript:counter.compact
pragma language_version >= 0.16 && <= 0.25;
import CompactStandardLibrary;

// public state (公開台帳に保存される状態)
export ledger round: Counter;

// transition function changing public state (公開状態を変更する関数)
export circuit increment(): [] {
    round.increment(1);
}
```

- **`ledger`**:  
  ブロックチェーン上で公開されるステート変数です。
- **`circuit`**:   
  トランザクションによって呼び出される関数（ステート遷移関数）です。  
  この中で状態の検証と更新が行われます。

<br/>

このように、Compactを使えばTypeScriptライクな構文で、データのプライバシーを細かく制御しつつその正当性を証明するロジックを直感的に記述できます！

## ハンズオン：Midnight開発環境を構築しよう

理論を学んだところで、いよいよ実践です。

ここからは、`counter.compact` を実際に動かすための開発環境を構築していきます。

:::message
この記事を執筆している2025年11月時点ではフロントエンドのとの接続はまだ不安定なようです。

よってこのハンズオンではスマートコントラクトのデプロイとデプロイ後のコントラクトをCLIで操作することをGoalとします。
:::

開発に必要なコンポーネントは以下の通りです。

1.  **Compact CLI**:   
  スマートコントラクトをコンパイルし、テストするためのコマンドラインツール。
2.  **Lace Midnight Preview Wallet**:   
  Midnight Testnetと対話するためのブラウザ拡張ウォレット。
3.  **Testnet Faucet**:   
  テスト用のトークンを入手するためのサービス。
4.  **ZK Proof Server**:   
  ローカルでゼロ知識証明を生成・検証するためのサーバー。
5.  **サンプルリポジトリ**:   
  この記事で利用するコード一式。

### Step 1: Compact CLI のインストール

まず、Compact言語のコンパイラである`compact` CLIをインストールします。

以下のコマンドをターミナルで実行してください。

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/midnightntwrk/compact/releases/latest/download/compact-installer.sh | sh
```

次に、特定のバージョン（この記事では`0.25.0`）を使用するように設定します。

```bash
compact update 0.25.0
```

インストールが成功したか、バージョンを確認してみましょう。

```bash
compact --version
# compact 0.2.0 or similar
compact compile --version
# 0.25.0
```

`compact compile --version` が `0.25.0` と表示されればOKです。

### Step 2: Lace Wallet の準備とTestnetトークンの入手

次に、Midnight Testnetに接続するためのウォレットを準備し、テストに必要なトークンを受け取ります。

1.  **Lace Walletのインストール**:  
    Chromeウェブストアから「[Lace Midnight Preview](https://chromewebstore.google.com/detail/lace-midnight-preview/hgeekaiplokcnmakghbdfbgnlfheichg)」をブラウザに追加します。
2.  **ウォレットの作成**:  
    画面の指示に従い、新しいウォレットを作成します。リカバリーフレーズは必ず安全な場所に保管してください。
3.  **アドレスのコピー**:  
    ウォレットのメイン画面で「Receive」ボタンを押し、自分のウォレットアドレスをコピーします。
4.  **Faucetでトークンを入手**:  
    [Midnight Testnet Faucet](https://midnight.network/test-faucet)にアクセスします。コピーしたアドレスを貼り付け、「Request funds」をクリックします。しばらくすると、テスト用の`tDUST`トークンがウォレットに届きます。

### Step 3: ZK Proof Server の起動

スマートコントラクトのプライベートな部分（証明の生成など）は、ローカルで実行される`Proof Server`と通信して処理されます。

このサーバーをMidnight公式が発表しているDockerコンテナイメージを使って起動します。

:::message
このステップにはDocker Destopがインストールされている必要があります。
:::

以下のコマンドを実行して、Proof Serverを起動してください。

```bash
docker run -p 6300:6300 midnightnetwork/proof-server -- 'midnight-proof-server --network testnet'
```

ターミナルにログが流れ始めれば成功です。  
このターミナルは起動したままにしておいてください。

念の為以下のコマンドでも稼働確認が可能です！

```bash
curl -X GET "http://localhost:6300"
```

以下のように表示されればOKです！

```bash
We're alive 🎉!
```

### Step 4: サンプルリポジトリの準備

最後に、この記事で解説するコードが含まれたリポジトリを準備します。

今回は以下のリポジトリを使用します。

https://github.com/mashharuki/midnight-sample

必要に応じてリポジトリを自分のアカウントにクローンしてきてください。

```bash
# リポジトリをクローン(事前に自分のアカウントにフォークしておくこと！)
git clone https://github.com/<user-name>/midnight-sample.git
cd midnight-sample

# 依存関係をインストール
yarn
```

:::message 
`git clone`のURLは、実際のサンプルリポジトリのURLに置き換えてください。
:::

以上で開発環境の準備は完了です！

次のセクションでは、いよいよスマートコントラクトの実装とテストを行っていきます。

## Counterコントラクトの実装とテスト

環境が整ったので、いよいよスマートコントラクトを実装し、テストしていきましょう。

### コードの解説

`pkgs/contract/src/counter.compact` に、先ほど解説したCounterスマートコントラクトを記述します。


```typescript:pkgs/contract/src/counter.compact
pragma language_version >= 0.16 && <= 0.25;
import CompactStandardLibrary;

// public state (公開台帳に保存される状態)
export ledger round: Counter;

// transition function changing public state (公開状態を変更する関数)
export circuit increment(): [] {
    round.increment(1);
}
```

コードを記述したら、`compact` CLIを使ってコンパイルします。

これにより、ゼロ知識証明の生成に必要な暗号マテリアル（proving key, verification keyなど）が生成されます。

```bash
yarn contract compact
```

実際には以下のようなコマンドを実行しています。

```bash
compact compile ./src/counter.compact ./src/managed/counter
```

成功すると、以下のようなログが表示されます。

```bash
Fetching public parameters for k=10 [====================] 192.38 KiB / 192.38 KiB
  circuit "increment" (k=10, rows=29)  
Overall progress [====================] 1/1   
```

### ユニットテストの実装

Compactでは、コントラクトのロジックをオフチェーンでシミュレートしてテストすることができます。

`pkgs/contract/src/test/counter.test.ts` で、そのテストコードを見てみましょう。

テストには `CounterSimulator` というヘルパークラス（内部でCompactのテスト用ライブラリを使用）を利用します。

```typescript:pkgs/contract/src/test/counter.test.ts
import { CounterSimulator } from "./counter-simulator.js";
import {
  NetworkId,
  setNetworkId
} from "@midnight-ntwrk/midnight-js-network-id";
import { describe, it, expect } from "vitest";

setNetworkId(NetworkId.Undeployed);

/**
 * Counterコントラクト用のユニットテストコード
 */
describe("Counter smart contract", () => {
  it("generates initial ledger state deterministically", () => {
    // シミュレーター型インスタンスを生成
    const simulator0 = new CounterSimulator();
    const simulator1 = new CounterSimulator();
    expect(simulator0.getLedger()).toEqual(simulator1.getLedger());
  });

  it("properly initializes ledger state and private state", () => {
    const simulator = new CounterSimulator();
    // 初期状態の台帳のステートを取得
    const initialLedgerState = simulator.getLedger();
    // 0になるはず
    expect(initialLedgerState.round).toEqual(0n);
    // プライベートのステートも0になるはず
    const initialPrivateState = simulator.getPrivateState();
    expect(initialPrivateState).toEqual({ privateCounter: 0 });
  });

  it("increments the counter correctly", () => {
    const simulator = new CounterSimulator();
    // incrementメソッドを呼び出す
    const nextLedgerState = simulator.increment();
    // 1加算されているはず
    expect(nextLedgerState.round).toEqual(1n);
    // プライベートステートの値は変わっていないはず
    const nextPrivateState = simulator.getPrivateState();
    expect(nextPrivateState).toEqual({ privateCounter: 0 });
  });
});
```

このテストコードは、以下の3つのシナリオを検証しています。

1. コントラクトが正しく初期化されること
2. ledgerの初期値が0であること
3. incrementメソッドが正しく呼び出されること

### テストの実行

それでは、実際にテストを実行してみましょう。以下のコマンドを実行します。

```bash
yarn contract test
```

すべてのテストが成功すれば、以下のような出力が表示されます。

```bash
RUN  v4.0.8 /workspaces/midnight-sample/my-mn-app/pkgs/contract

 ✓ test/counter.test.ts (3 tests) 44ms
   ✓ Counter smart contract (3)
     ✓ generates initial ledger state deterministically 36ms
     ✓ properly initializes ledger state and private state 3ms
     ✓ increments the counter correctly 4ms

 Test Files  1 passed (1)
      Tests  3 passed (3)
   Start at  08:27:47
   Duration  421ms (transform 95ms, setup 0ms, collect 233ms, tests 44ms, environment 0ms, prepare 13ms)

JUNIT report written to /workspaces/midnight-sample/my-mn-app/pkgs/contract/reports/report.xml
Done in 1.34s.
```

これで、コントラクトのロジックが意図通りに動作することが確認できました。

次は、このコントラクトをTestnetにデプロイするためのCLIツールを作成していきます。

## CLIからTestnetにデプロイ＆実行

ローカルでのテストが完了したら、いよいよコントラクトをTestnetにデプロイします。

`pkgs/cli` パッケージには、デプロイやコントラクトとの対話を行うためのスクリプトが含まれています。

### TypeScript APIの生成

まず、`contract`パッケージのビルドを行います。

これにより、コンパイルされたコントラクトの情報に基づいて、CLIから利用するためのTypeScriptの型定義やAPIが自動生成されます。

```bash
yarn contract build
```

実際には以下のようなコマンドが実行されます。

```bash
rm -rf dist && tsc --project tsconfig.build.json && cp -Rf ./src/managed ./dist/managed && cp ./src/counter.compact ./dist
```

このステップにより、`cli`パッケージから`contract`パッケージの回路（`increment`など）を型安全に呼び出すことができるようになります！

### 環境変数の設定

Testnetへのデプロイには、トランザクションに署名するためのウォレットの秘密鍵が必要です。

`pkgs/cli` ディレクトリにある `.env.example` ファイルをコピーして `.env` ファイルを作成し、Lace Walletのシードを設定します。

```bash
cp pkgs/cli/.env.example pkgs/cli/.env
```

そして、作成した `pkgs/cli/.env` ファイルを編集します。

```:pkgs/cli/.env
# testnetをしている
NETWORK_ENV_VAR=testnet
# ここにLaceWalletからエクスポートしたシードを貼り付ける
SEED_ENV_VAR=
INITIAL_COUNTER_ENV_VAR=
CACHE_FILE_ENV_VAR=
# コントラクトデプロイ後に設定
CONTRACT_ADDRESS=
```

:::message
**シードの取り扱いには最大限の注意を払ってください。** 

このファイルがGitHubなどに公開されないように`.gitignore`に含まれていることを必ず確認してください。
:::

### CLI用ユニットテストコードの解説

CLI用にもユニットテストコードを用意しています。

```ts
// This file is part of midnightntwrk/example-counter.
// Copyright (C) 2025 Midnight Foundation
// SPDX-License-Identifier: Apache-2.0
// Licensed under the Apache License, Version 2.0 (the "License");
// You may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { type Resource } from '@midnight-ntwrk/wallet';
import { type Wallet } from '@midnight-ntwrk/wallet-api';
import path from 'path';
import * as api from '../api';
import { type CounterProviders } from '../utils/common-types';
import { currentDir } from '../config';
import { createLogger } from '../utils/logger-utils';
import { TestEnvironment } from './commons';
import { describe, it, expect, beforeAll, afterAll } from 'vitest';

const logDir = path.resolve(currentDir, '..', 'logs', 'tests', `${new Date().toISOString()}.log`);
const logger = await createLogger(logDir);

describe('API', () => {
  let testEnvironment: TestEnvironment;
  let wallet: Wallet & Resource;
  let providers: CounterProviders;

  /**
   * 全ユニットテストコード実行前に行う共通処理
   * ウォレットやプロバイダー、環境変数の設定、ロギングの設定を行う
   */
  beforeAll(
    async () => {
      api.setLogger(logger);
      testEnvironment = new TestEnvironment(logger);
      const testConfiguration = await testEnvironment.start();
      wallet = await testEnvironment.getWallet();
      providers = await api.configureProviders(wallet, testConfiguration.dappConfig);
    },
    1000 * 60 * 45,
  );

  afterAll(async () => {
    await testEnvironment.saveWalletCache();
    await testEnvironment.shutdown();
  });

  it('should deploy the contract and increment the counter [@slow]', async () => {
    // Counterコントラクトをデプロイする
    const counterContract = await api.deploy(providers, { privateCounter: 0 });
    expect(counterContract).not.toBeNull();
    // デプロイ後のCounterコントラクトの値を確認する
    const counter = await api.displayCounterValue(providers, counterContract);
    expect(counter.counterValue).toEqual(BigInt(0));

    await new Promise((resolve) => setTimeout(resolve, 2000));
    // incrementメソッドを呼び出す
    const response = await api.increment(counterContract);
    expect(response.txHash).toMatch(/[0-9a-f]{64}/);
    expect(response.blockHeight).toBeGreaterThan(BigInt(0));
    // 実行後に1加算されていれば正常！
    const counterAfter = await api.displayCounterValue(providers, counterContract);
    expect(counterAfter.counterValue).toEqual(BigInt(1));
    expect(counterAfter.contractAddress).toEqual(counter.contractAddress);
  });
});
```

このユニットテストコードをローカルブロックチェーンとテストネットブロックチェーン上それぞれで実行してみます！

以下のコマンドを実行してみてください！

#### ローカルでのユニットテストコード実施

```bash
yarn cli test-api
```

以下のようになればOK!

```bash
Test Files  1 passed (1)
      Tests  1 passed (1)
   Start at  08:41:12
   Duration  200.97s (transform 180ms, setup 72ms, collect 1.11s, tests 199.62s, environment 0ms, prepare 10ms)
```

#### テストネットでのユニットテストコード実施

```bash
yarn cli test-against-testnet
```

以下のようになればOK!

```bash
✓ src/test/counter.api.test.ts (1 test) 151857ms
  ✓ API (1)
    ✓ should deploy the contract and increment the counter [@slow]  125059ms

Test Files  1 passed (1)
    Tests  1 passed (1)
  Start at  08:47:54
  Duration  153.65s (transform 205ms, setup 93ms, collect 1.56s, tests 151.86s, environment 0ms, prepare 8ms)
```

### デプロイスクリプトの解説

`pkgs/cli/scripts/deploy.ts` は、コントラクトをTestnetにデプロイするためのスクリプトです。

```ts
import type { Logger } from 'pino';
import { createLogger } from '../src/utils/logger-utils.js';
import {
	StandaloneConfig,
	TestnetLocalConfig,
	TestnetRemoteConfig,
	type Config,
} from '../src/config.js';
import * as api from '../src/api.js';
import * as dotenv from 'dotenv';

dotenv.config();

const {
    NETWORK_ENV_VAR,
    SEED_ENV_VAR,
    INITIAL_COUNTER_ENV_VAR,
    CACHE_FILE_ENV_VAR,
} = process.env;

/**
 * CIやスクリプト実行向けの非対話的なデプロイヘルパー。
 * 対象ネットワークと再利用するウォレットシードを環境変数で指定し、手動入力なしに安全に再デプロイできる。
 */

type SupportedNetwork = 'standalone' | 'testnet-local' | 'testnet' | 'testnet-remote';

const resolveNetwork = (value: string | undefined): SupportedNetwork => {
	const normalized = (value ?? 'testnet').toLowerCase();
	if (normalized === 'testnet') {
		return 'testnet';
	}
	switch (normalized) {
		case 'testnet-remote':
		case 'standalone':
		case 'testnet-local':
			return normalized;
		default:
			throw new Error(`Unsupported network '${value}'.`);
	}
};

const buildConfig = (network: SupportedNetwork): Config => {
	switch (network) {
		case 'standalone':
			return new StandaloneConfig();
		case 'testnet-local':
			return new TestnetLocalConfig();
		case 'testnet':
		case 'testnet-remote':
		default:
			return new TestnetRemoteConfig();
	}
};

const ensureSeed = (seed: string | undefined): string => {
	if (seed === undefined || seed.trim() === '') {
		throw new Error(`Wallet seed is required. Set ${SEED_ENV_VAR}.`);
	}
	return seed.trim();
};

const parseInitialCounter = (value: string | undefined): number => {
	if (value === undefined || value.trim() === '') {
		return 0;
	}
	const parsed = Number(value);
	if (!Number.isSafeInteger(parsed) || parsed < 0) {
		throw new Error(`Initial counter must be a non-negative safe integer. Received '${value}'.`);
	}
	return parsed;
};

const defaultCacheName = (seed: string, network: SupportedNetwork): string => {
	const prefix = seed.substring(0, 8);
	return `${prefix}-${network}.state`;
};

// Midnight系リソースはbest-effortなcloseメソッドを持つことが多いため、失敗は握り潰して再実行可能性を保つ。
const closeIfPossible = async (resource: unknown, label: string): Promise<void> => {
	if (resource !== null && typeof resource === 'object') {
		const maybeClosable = resource as { close?: () => unknown };
		if (typeof maybeClosable.close === 'function') {
			try {
				await Promise.resolve(maybeClosable.close());
			} catch (error) {
				if (logger !== undefined) {
					if (error instanceof Error) {
						logger.warn(`Failed to close ${label}: ${error.message}`);
						logger.debug(error.stack ?? '');
					} else {
						logger.warn(`Failed to close ${label}: ${String(error)}`);
					}
				}
			}
		}
	}
};

let logger: Logger | undefined;

/**
 * コントラクトデプロイ用のスクリプト
 */
const main = async () => {
    // ネットワーク情報を取得する
	const network = resolveNetwork(NETWORK_ENV_VAR);
	const seed = ensureSeed(SEED_ENV_VAR);
	const initialCounter = parseInitialCounter(INITIAL_COUNTER_ENV_VAR);
	const cacheFileName = CACHE_FILE_ENV_VAR ?? defaultCacheName(seed, network);
    // 設定ファイルの読み込み
	const config = buildConfig(network);
    // ロガーの設定
	logger = await createLogger(config.logDir);
	api.setLogger(logger);

	logger.info(`Deploying counter contract to '${network}' network.`);
	logger.info(`Using cache file '${cacheFileName}'.`);
    
	let wallet: Awaited<ReturnType<typeof api.buildWalletAndWaitForFunds>> | undefined;
	
    try {
        // シードからウォレットを作成
		wallet = await api.buildWalletAndWaitForFunds(config, seed, cacheFileName);
        // プロバイダーインスタンスを生成
		const providers = await api.configureProviders(wallet, config);
        // Counterコントラクトをデプロイする
		const counterContract = await api.deploy(providers, { privateCounter: initialCounter });
        // デプロイしたトランザクション情報を出力する
		const deployTx = counterContract.deployTxData.public;
		logger.info(`Deployment transaction: ${deployTx.txId}`);
		logger.info(`Contract address: ${deployTx.contractAddress}`);
		console.log(`Counter contract deployed at: ${deployTx.contractAddress}`);
		await api.saveState(wallet, cacheFileName);
		await closeIfPossible(providers.privateStateProvider, 'private state provider');
	} finally {
		if (wallet !== undefined) {
			await closeIfPossible(wallet, 'wallet');
		}
	}
};

/**
 * メインメソッド
 */
await main().catch((error) => {
	if (logger !== undefined) {
		if (error instanceof Error) {
			logger.error(`Deployment failed: ${error.message}`);
			logger.debug(error.stack ?? '');
		} else {
			logger.error(`Deployment failed: ${String(error)}`);
		}
	} else {
		console.error(error);
	}
	process.exitCode = 1;
});
```

`@midnight-ntwrk/midnight-sdk` などのライブラリを使い、以下のような処理を行っています。

- `.env` ファイルから秘密鍵を読み込む。
- 秘密鍵を使ってウォレットオブジェクトを構築する。
- Testnetへの接続設定（Provider）を行う。
- `api.deploy` を呼び出し、コントラクトのデプロイを実行する。

### デプロイの実行

準備が整ったら、以下のコマンドでデプロイを実行します。

```bash
yarn cli deploy
```

成功すると、デプロイされたコントラクトのアドレスがターミナルに出力されます。

```bash
[12:16:24.603] INFO (39506): Deploying counter contract...
[12:17:27.488] INFO (39506): Deployed contract at address: 020050e6bdae4c9e65023a252a6aba74323c1d9c1ba6e520f00e84a5fc1c75b100f3
[12:17:27.488] INFO (39506): Deployment transaction: 00000000c408a293e4e287285649623774b2be950bf0d385a20117ce79a99eb7315aa547
[12:17:27.489] INFO (39506): Contract address: 020050e6bdae4c9e65023a252a6aba74323c1d9c1ba6e520f00e84a5fc1c75b100f3
Counter contract deployed at: 020050e6bdae4c9e65023a252a6aba74323c1d9c1ba6e520f00e84a5fc1c75b100f3
[12:17:27.489] INFO (39506): Not saving cache as sync cache was not defined
Done in 90.16s.
```

このコントラクトアドレスを、先ほど作成した `.env` ファイルの `CONTRACT_ADDRESS` に設定しておきましょう。

### `increment`の実行

最後に、デプロイしたコントラクトの `increment` 回路を呼び出してみましょう。

`pkgs/cli/scripts/increment.ts` がそのためのスクリプトです。

```ts
import type { Logger } from 'pino';
import { createLogger } from '../src/utils/logger-utils.js';
import {
	StandaloneConfig,
	TestnetLocalConfig,
	TestnetRemoteConfig,
	type Config,
} from '../src/config.js';
import * as api from '../src/api.js';
import { assertIsContractAddress } from '@midnight-ntwrk/midnight-js-utils';
import * as dotenv from 'dotenv';

dotenv.config();

/**
 * 既存のカウンターコントラクトに対し、非対話的に increment を実行するヘルパー。
 * ネットワークやウォレットシード、コントラクトアドレスは環境変数で受け取り、CI 等でもそのまま利用できる。
 */

type SupportedNetwork = 'standalone' | 'testnet-local' | 'testnet' | 'testnet-remote';

const { NETWORK_ENV_VAR, SEED_ENV_VAR, CONTRACT_ADDRESS, CACHE_FILE_ENV_VAR } = process.env;

const resolveNetwork = (value: string | undefined): SupportedNetwork => {
	const normalized = (value ?? 'testnet').toLowerCase();
	if (normalized === 'testnet') {
		return 'testnet';
	}
	switch (normalized) {
		case 'testnet-remote':
		case 'standalone':
		case 'testnet-local':
			return normalized;
		default:
			throw new Error(`Unsupported network '${value}'.`);
	}
};

const buildConfig = (network: SupportedNetwork): Config => {
	switch (network) {
		case 'standalone':
			return new StandaloneConfig();
		case 'testnet-local':
			return new TestnetLocalConfig();
		case 'testnet':
		case 'testnet-remote':
		default:
			return new TestnetRemoteConfig();
	}
};

const ensureSeed = (seed: string | undefined): string => {
	if (seed === undefined || seed.trim() === '') {
		throw new Error('Wallet seed is required. Set SEED_ENV_VAR.');
	}
	return seed.trim();
};

const ensureContractAddress = (address: string | undefined): string => {
	if (address === undefined || address.trim() === '') {
		throw new Error('Contract address is required. Set CONTRACT_ADDRESS.');
	}
	const trimmed = address.trim();
	assertIsContractAddress(trimmed);
	return trimmed;
};

const defaultCacheName = (seed: string, network: SupportedNetwork): string => {
	const prefix = seed.substring(0, 8);
	return `${prefix}-${network}.state`;
};

// Midnight系リソースはbest-effortなcloseメソッドを持つことが多いため、失敗は握り潰して再実行可能性を保つ。
const closeIfPossible = async (resource: unknown, label: string): Promise<void> => {
	if (resource !== null && typeof resource === 'object') {
		const maybeClosable = resource as { close?: () => unknown };
		if (typeof maybeClosable.close === 'function') {
			try {
				await Promise.resolve(maybeClosable.close());
			} catch (error) {
				if (logger !== undefined) {
					if (error instanceof Error) {
						logger.warn(`Failed to close ${label}: ${error.message}`);
						logger.debug(error.stack ?? '');
					} else {
						logger.warn(`Failed to close ${label}: ${String(error)}`);
					}
				}
			}
		}
	}
};

let logger: Logger | undefined;

const main = async () => {
	const network = resolveNetwork(NETWORK_ENV_VAR);
	const seed = ensureSeed(SEED_ENV_VAR);
	const contractAddress = ensureContractAddress(CONTRACT_ADDRESS);
	const cacheFileName = CACHE_FILE_ENV_VAR ?? defaultCacheName(seed, network);

	const config = buildConfig(network);
	logger = await createLogger(config.logDir);
	api.setLogger(logger);

	logger.info(`Incrementing counter contract on '${network}' network.`);
	logger.info(`Target contract address: ${contractAddress}`);
	logger.info(`Using cache file '${cacheFileName}'.`);

	let wallet: Awaited<ReturnType<typeof api.buildWalletAndWaitForFunds>> | undefined;
	let providers: Awaited<ReturnType<typeof api.configureProviders>> | undefined;
	try {
		wallet = await api.buildWalletAndWaitForFunds(config, seed, cacheFileName);
		providers = await api.configureProviders(wallet, config);
        // デプロイ済みのコントラクトインスタンスを生成
		const counterContract = await api.joinContract(providers, contractAddress);
        // Counterコントラクトの increment メソッドを呼び出す
		const txInfo = await api.increment(counterContract);
		logger.info(`Increment transaction: ${txInfo.txId} (block ${txInfo.blockHeight})`);
		console.log(`Counter incremented. txId=${txInfo.txId} block=${txInfo.blockHeight}`);
		const { counterValue } = await api.displayCounterValue(providers, counterContract);
		if (counterValue !== null) {
			logger.info(`Current counter value: ${counterValue.toString()}`);
			console.log(`Current counter value: ${counterValue.toString()}`);
		}
		await api.saveState(wallet, cacheFileName);
	} finally {
		if (providers !== undefined) {
			await closeIfPossible(providers.privateStateProvider, 'private state provider');
		}
		if (wallet !== undefined) {
			await closeIfPossible(wallet, 'wallet');
		}
	}
};

await main().catch((error) => {
	if (logger !== undefined) {
		if (error instanceof Error) {
			logger.error(`Increment failed: ${error.message}`);
			logger.debug(error.stack ?? '');
		} else {
			logger.error(`Increment failed: ${String(error)}`);
		}
	} else {
		console.error(error);
	}
	process.exitCode = 1;
});
```

以下のコマンドを実行します。

```bash
yarn cli increment
```

このスクリプトは、`.env` ファイルからコントラクトアドレスを読み込み、`api.joinContract` で既存のコントラクトに接続し、`api.increment` を呼び出します。

成功すると、トランザクションIDや現在のCounterの値が出力されます。

```bash
[12:33:37.176] INFO (47085): Incrementing...
[12:34:34.270] INFO (47085): Transaction 000000000202acbcd05e9f19e5144acc5f97953255840b8b932fc71b84520e715b7ca900 added in block 2485067
[12:34:34.271] INFO (47085): Increment transaction: 000000000202acbcd05e9f19e5144acc5f97953255840b8b932fc71b84520e715b7ca900 (block 2485067)
Counter incremented. txId=000000000202acbcd05e9f19e5144acc5f97953255840b8b932fc71b84520e715b7ca900 block=2485067
[12:34:34.271] INFO (47085): Checking contract ledger state...
[12:34:34.462] INFO (47085): Ledger state: 1
[12:34:34.463] INFO (47085): Current counter value: 1
[12:34:34.463] INFO (47085): Current counter value: 1
Current counter value: 1
[12:34:34.463] INFO (47085): Not saving cache as sync cache was not defined
Done in 128.20s.
```

`Current counter value: 1` と表示され、パブリックなCounterが1つ加算されたことが確認できましたね！

ハンズオンは以上となります。

## 現状の制約と今後について

Midnightはこの記事を執筆している2025年11月現在、まだ**開発者向けTestnet**の段階にあり、Mainnetはローンチされていません。

そのため、いくつかの制約や注意点があります。

- **パフォーマンス**:   
  Testnet上でのトランザクションのファイナリティには時間がかかる場合があります。
- **APIの変更**:   
  開発段階にあるため、SDKやCLIの仕様が変更される可能性があります。公式ドキュメントを定期的に確認することをお勧めします。
- **機能の制限**:   
  利用できる機能やツールはまだ限定的ですが、コミュニティからのフィードバックを元に、急速に開発が進んでいます。
- **フロントエンドとの接続**:
  ハッカソン参加にあたり一番調査に時間を使ったのがこの部分でした。現地でMidnightチームにも確認しましたが、現状では安定してフロントエンドとコントラクトを接続させるライブラリ等はないとのことでした(今はCLIで呼び出すしかない)。

<br/>

Midnightは、プライバシーというWeb3の重要課題に取り組む、非常に野心的なプロジェクトです。

Cardanoの強力なコミュニティとセキュリティ基盤を背景に、今後の発展から目が離せません！

フロントエンドとの接続等課題もありますが、今後アップデート予定とのことなので続報を待ちたいと思います！

## おわりに

この記事では、Cardanoのプライバシー保護サイドチェーン**Midnight**と、そのスマートコントラクト用プログラミング言語**Compact**について、ハンズオン形式で解説しました。

- ブロックチェーンの「透明すぎる」問題を解決するMidnightのアーキテクチャ。
- TypeScriptライクな構文で直感的にプライベートDAppsを開発できるCompact言語。
- `public`, `private`, `witness` を使い分けたデータ管理。
- 開発環境の構築から、コントラクトの実装、テスト、Testnetへのデプロイまでの一連の流れ。

今後の発展が非常に楽しみですね！  

招待していただいたHackathonも本当に楽しかったので引き続きウォッチしようと思います！

ここまで読んでいただきありがとうございました！

## 参考文献
- [Midnight公式サイト](https://www.midnight.network/)
- [Midnightドキュメント](https://docs.midnight.network/)
- [Compact GitHubリポジトリ](https://github.com/midnightntwrk/compact)
- [Midnight Awesome DApps](https://github.com/midnightntwrk/midnight-awesome-dapps)
- [Lace Midnight Preview Wallet](https://chromewebstore.google.com/detail/lace-midnight-preview/hgeekaiplokcnmakghbdfbgnlfheichg)
- [Midnight Testnet Faucet](https://midnight.network/test-faucet)
- [Midnight Hackathon (Devpost)](https://midnight-hackathon.devpost.com/)
