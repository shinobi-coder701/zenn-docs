---
title: "Hardhatを使ってAlephZero(EVM Layer)にスマートコントラクトをデプロイする"
emoji: "🛠"
type: "tech"
topics: ["Web3","Blockchain","ゼロ知識証明","EVM","Solidity"]
published: false
---

![](/images/aleph_zero_2/0.jpeg)

## はじめに

皆さん、こんにちは！

今回も Aleph Zeroについても技術ブログ記事になります！！

前回の記事で Aleph Zeroの概要については紹介しました。

今回は実際にスマートコントラクトをデプロイしてみたいと思います！！

## AlephZero(EVM Layer) にスマコンをデプロイしてみよう！

今回使うソースコードは以下のリポジトリに格納されています！！

https://github.com/mashharuki/AlephZero-Sample/tree/main

基本はHardhatのテンプレートプロジェクトをそのまま流用しています！

スマートコントラクトはテンプレのものをそのまま流用しているので解説は割愛させていただきます。

### 設定ファイルを確認しよう！

ではまず、設定ファイルである`hardhat.config.ts`を確認していきたいと思います。

```ts
import type { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox-viem";
import fs from "fs";
import path from "path";
import * as dotenv from "dotenv";

dotenv.config();

const { PRIVATE_KEY} = process.env;

// タスクファイルを読み込むための設定
const SKIP_LOAD = process.env.SKIP_LOAD === "true";
if (!SKIP_LOAD) {
	const taskPaths = ["", "utils", "lock"];
	taskPaths.forEach((folder) => {
		const tasksPath = path.join(__dirname, "tasks", folder);
		fs.readdirSync(tasksPath)
			.filter((_path) => _path.includes(".ts"))
			.forEach((task) => {
				require(`${tasksPath}/${task}`);
			});
	});
}

const config: HardhatUserConfig = {
	solidity: {
		compilers: [
			{
				version: "0.8.27",
				settings: {
					viaIR: true,
				},
			},
		],
	},
	networks: {
		hardhat: {
			allowUnlimitedContractSize: true,
		},
		alephZeroTestnet: {
			url: `https://alephzero-sepolia.drpc.org`,
			accounts: PRIVATE_KEY !== undefined ? [PRIVATE_KEY] : [],
		}
	},
};

export default config;
```

RPCエンドポイントには、 `https://alephzero-sepolia.drpc.org`を指定しています。

これは公式サイトからの情報で以下のページから引っ張ってきました！

https://docs.alephzero.org/aleph-zero/build/development-on-evm-layer

### テストネット用のファウセットの入手方法

次にテストネット用のファウセットの取得方法ですが、以下のサイトいずれかが選択肢としてあります。

時間はかかりますが、沢山入手できる**drpc**の方をおすすめします！

https://drpc.org/faucet/alephzero

https://thirdweb.com/aleph-zero-testnet

### プロジェクトのセットアップ

ここまできたらあと一歩です。

次に環境変数用の`.env`ファイルを作成して秘密鍵の情報を設定します。

```txt
PRIVATE_KEY=""
```

そして以下のコマンドで必要なライブラリをインストールします。

```bash
yarn
```

### デプロイしてみよう！

インストールまで終わったら以下のコマンドでコンパイルして問題ないことを確認します。

```bash
yarn compile
```

問題なければいよいよデプロイです！

```bash
yarn deploy:Lock --network alephZeroTestnet
```

しばらく待つと、`ignition/deployments/chain-2039/deployed_addresses.json`というファイルが生成されると思うのでそれを確認します！

```json
{
  "LockModule#Lock": "0xAa363921A48Eac63F802C57658CdEde768B3DAe1"
}
```

ちゃんとデプロイされているみたいです！

念の為、Block Explorerの方でも確認します！

https://evm-explorer-testnet.alephzero.org/address/0xAa363921A48Eac63F802C57658CdEde768B3DAe1

大丈夫そうですね！！

設定さえ問題なければ、他のEVM対応のチェーンと同じようにデプロイすることが確認できました！！

## Hardhat + viem で Aleph Zero テストネットに触ってみよう！

これだけだとつまらないので、Hardhatのタスク機能を使って、Aleph Zero テストネットの情報を取得するタスクをいくつか作ってみました！

### チェーンの基本情報を取得するタスク

まず、ガス代などの情報を表示させるタスクを解説していきます！

実行方法は以下のコマンドを打つだけです！

```bash
yarn getChainInfo --network alephZeroTestnet
```

すると以下のように情報を表示してくれます！

```bash
################################### [START] ###################################

      Chain ID: 2039
      Block Number: 1031859
      Transaction Count: 2
      Gas Price: 0.00000004 ETH
    
################################### [END] ###################################
```

実装内容を確認していきます！

```ts
import { task } from "hardhat/config";
import { HardhatRuntimeEnvironment } from "hardhat/types";
import { formatEther } from "viem";
import { alephZeroTestnet } from "../../helpers/constants";

/**
 * 【Task】	getChainInfo of connected chain
 */
task("getChainInfo", "getChainInfo of connected chain").setAction(
	async (taskArgs: any, hre: HardhatRuntimeEnvironment) => {
		console.log(
			"################################### [START] ###################################"
		);

		const publicClient = await hre.viem.getPublicClient({
			chain: alephZeroTestnet
		});
		const chainId = await publicClient.getChainId();
		const blockNumber = await publicClient.getBlockNumber();
		const count = await publicClient.getBlockTransactionCount();
		const gasPrice = await publicClient.getGasPrice();
		const gasPriceInEther = formatEther(gasPrice);

		console.log(`
      Chain ID: ${chainId}
      Block Number: ${blockNumber}
      Transaction Count: ${count}
      Gas Price: ${gasPriceInEther} ETH
    `);

		console.log(
			"################################### [END] ###################################"
		);
	}
);
```

**viem**の基本的なメソッドを呼び出しているだけのシンプルなタスクです。

一点、注意が必要なこととして **Aleph Zero**はVeimの標準対応のチェーンではないのでカスタムチェーンとして追加してあげる必要があります！

https://viem.sh/docs/actions/wallet/addChain.html

カスタムチェーンの型情報は以下で確認ができます。

https://github.com/wevm/viem/blob/main/src/types/chain.ts

今回だと下記の部分です。

```ts
const publicClient = await hre.viem.getPublicClient({
			chain: alephZeroTestnet
		});
```

alephZeroTestnetの中身は別ファイルで定義しており以下の通りとなっています。

```ts
import { Chain } from "viem";

// テストネットの設定
export const alephZeroTestnet: Chain = {
    id: 2039,
    name: "Aleph Zero Testnet",
    nativeCurrency: {
      name: "Test Aleph",
      symbol: "tAZERO", // テストネット用のシンボル
      decimals: 18, // Aleph Zeroのネイティブトークンの小数点桁数
    },
    blockExplorers: {
      default: {
        name: "Aleph Zero Testnet Explorer",
        url: "https://evm-explorer-testnet.alephzero.org", // テストネット用のブロックエクスプローラーURL
      },
    },
    rpcUrls: {
      default: {
        http: ["https://alephzero-sepolia.drpc.org"], // Aleph Zero TestnetのRPC URL
        webSocket: ["wss://rpc.testnet.alephzero.org/ws"], // WebSocket RPC URL
      },
    },
    testnet: true, // テストネットなのでtrue
    contracts: {
      ensRegistry: undefined, 
      ensUniversalResolver: undefined,
      multicall3: undefined, 
      universalSignatureVerifier: undefined,
    },
  };
```

これで他のチェーンと同じように操作ができます！

### ウォレットの残高を取得するタスク

次にウォレットの残高を取得するタスクを作成してみました。

実行方法は以下のコマンドを打つだけです。

```bash
yarn getBalance --network alephZeroTestnet
```

以下のように残高情報を出力してくれます。

```bash
################################### [START] ###################################
Balance of 0x51908f598a5e0d8f1a3babfa6df76f9704dad072: 34.80392468 ETH
################################### [END] ###################################
```

実装内容を確認していきます。

```ts
import { task } from "hardhat/config";
import { HardhatRuntimeEnvironment } from "hardhat/types";
import { formatEther } from "viem";
import { alephZeroTestnet } from "../../helpers/constants";

/**
 * 【Task】get the balance of the account
 */
task("getBalance", "getBalance").setAction(
	async (taskArgs: any, hre: HardhatRuntimeEnvironment) => {
		console.log(
			"################################### [START] ###################################"
		);
		
		const [bobWalletClient] = await hre.viem.getWalletClients({
			chain: alephZeroTestnet
		});
		const publicClient = await hre.viem.getPublicClient({
			chain: alephZeroTestnet
		});
		

		const bobBalance = await publicClient.getBalance({
			address: bobWalletClient.account.address,
		});

		console.log(
			`Balance of ${bobWalletClient.account.address}: ${formatEther(
				bobBalance
			)} ETH`
		);

		console.log(
			"################################### [END] ###################################"
		);
	}
);
```

### コントラクトの読み取り系メソッドを呼び出してみる。

次に先ほどデプロイしたコントラクトのメソッドをタスクファイルから呼び出してみたいと思います！！

以下のコマンドで実行できます！

```bash
yarn callReadMethod --network alephZeroTestnet
```

問題なければ、コントラクトの情報を取得してくるメソッドが処理されて以下のような結果が出力されます！！

```bash
################################### [START] ###################################

            LockModule#Lock 's address is 0xAa363921A48Eac63F802C57658CdEde768B3DAe1
        

            unlockTimes : 1893456000
            ownerAddress: 0x51908F598A5e0d8F1A3bAbFa6DF76F9704daD072
            contractBalance: 0.001 ETH
        
################################### [END] ###################################
```

実装内容を確認していきます！

```ts
import { task } from "hardhat/config";
import { HardhatRuntimeEnvironment } from "hardhat/types";
import { getContractAddress } from "../../helpers/contractJsonHelper";
import { formatEther } from "viem";
import { alephZeroTestnet } from "../../helpers/constants";

/**
 * 【Task】	call read method of sample contract
 */
task("callReadMethod", "call read method of sample contract").setAction(
	async (taskArgs: any, hre: HardhatRuntimeEnvironment) => {
		console.log(
			"################################### [START] ###################################"
		);

		// get wallet client
		const [owner] = await hre.viem.getWalletClients({
			chain: alephZeroTestnet
		});
		const publicClient = await hre.viem.getPublicClient({
			chain: alephZeroTestnet
		});
		// get chain ID
		const chainId = (await publicClient.getChainId()).toString();
		// get contract name
		const contractName = `LockModule#Lock`;
		// get contract address
		const contractAddress = getContractAddress(chainId, contractName);

		console.log(`
            ${contractName} 's address is ${contractAddress}
        `);

		// create Contract instance
		const lock = await hre.viem.getContractAt(
			"Lock",
			contractAddress as `0x${string}`,
			{
				client: { 
					public: publicClient,
					wallet: owner
				},
			}
		);

		// call read method
		const unlockTime = await lock.read.unlockTime();
		const ownerAddress = await lock.read.owner();
		// get contract's balance
		const contractBalance = await publicClient.getBalance({
			address: contractAddress as `0x${string}`,
		});

		console.log(`
            unlockTimes : ${unlockTime}
            ownerAddress: ${ownerAddress}
            contractBalance: ${formatEther(contractBalance)} ETH
        `);

		console.log(
			"################################### [END] ###################################"
		);
	}
);
```

前半部分はこれまでのタスクファイルとほぼ同じです！

publicClientやWalletClientの他、コントラクトをインスタンス化する時にカスタムチェーンの設定を追加しています。

他に注目すべき点としてデプロイする度にコントラクトアドレスを書き換える必要が内容にヘルパーメソッドとして、`getContractAddress`メソッドを追加で実装しています。

このメソッドを使うことで、チェーンIDとコントラクト名を指定してあげることでJSONファイルに格納されている値を取ってくることができます。

これで常に最新のコントラクトのアドレスを取得することが可能になります！

このメソッドが実装されているのは、 `helpers/contractJsonHelper.ts`ファイルになります！

```ts
import fs from "fs";
import path from "path";

/**
 * デプロイされたアドレス情報をjsonファイルから取得するヘルパーメソッド
 * @param chainId チェーンID
 * @param contractName  コントラクト名 <コントラクト名>Module#<コントラクト名>の形式で指定する。
 * @returns
 */
export function getContractAddress(
	chainId: string,
	contractName: string
): string | undefined {
	try {
		// ファイルパスを構築
		const filePath = path.join(
			__dirname,
			"../",
			"ignition",
			"deployments",
			`chain-${chainId}`,
			"deployed_addresses.json"
		);

		// JSONファイルの内容を読み込み
		const fileContent = fs.readFileSync(filePath, "utf-8");

		// JSONをオブジェクトにパース
		const deployedAddresses = JSON.parse(fileContent);

		// 指定されたコントラクト名のアドレスを返す
		return deployedAddresses[contractName];
	} catch (error) {
		console.error("Error reading contract address:", error);
		return undefined;
	}
}
```

これだけあれば開発もサクサク進められそうですね！！

## まとめ

いかがでしたでしょうか？

!inkで実装する方はRustに近い形になるので全然別物になると思いますが、EVM Layerの方であればサクッと始められそうです！！

この記事が少しでも皆さんの参考になれば幸いです！！

ここまで読んでいただきありがとうございました！！！

### 参考文献

1. [テストネット Faucet](https://drpc.org/faucet/alephzero)