---
title: "MastraとJPYC SDKで作る金融AIエージェント！"
emoji: "🪙"
type: "tech" 
topics: ["Mastra", "TypeScript", "MCP", "生成AI", "Web3"]
published: false
---

![](/images/jpyc_ai_agent-1/0.jpeg)

# はじめに

みなさん、こんにちは！

今回の記事は、 アドベントカレンダーの[AIエージェント構築＆運用 Advent Calendar 2025](https://qiita.com/advent-calendar/2025/agents)と[Model Context Protocol(MCP) Advent Calendar 2025](https://qiita.com/advent-calendar/2025/mcp)への応募を兼ねた記事となっています！！

**ステーブルコイン**を自然言語で操作できたら面白くないですか？！

今回は、**JPYC SDK**を使って**JPYC**を操作できる**AIエージェント**を作成してみましたのでその実装内容を深く掘り下げていきます！！！

ぜひ最後まで読んでいってください！

:::message
**この記事の対象読書**

- JPYC SDKについて知りたい人
- JPYC SDKをMCP化させる方法を知りたい人
- ステーブルコインについて知りたい人
- 自作したMCPをMastraに組み込む方法を知りたい人
- Web3とAIを掛け合わせたアプリの開発方法を学びたい人
:::

# JPYC?ステーブルコイン？何それ？

突然ですが、皆さんは**JPYC**という**日本円建てステーブルコイン**をご存知でしょうか？

https://jpyc.jp/

**JPYC**は、2025年に金融庁が国内で初めて承認した**日本円建てのステーブルコイン**ですでに流通している新しいデジタル通貨です！

https://www.nikkei.com/article/DGXZQOUB146U80U5A810C2000000/

:::message
ステーブルコインとは？

法定通貨と価値が**1:1**で連動しているデジタル通貨
Ethereumなどパブリックブロックチェーンで発行しているケースが多い
:::

ステーブルコインの実態は**スマートコントラクト**と呼ばれるプログラムであり、ステーブルコインはこの**スマートコントラクト**のロジックに基づいて処理が実行されます。

スマートコントラクトのソースコードは以下のサイトで確認することができます。

https://etherscan.io/token/0xe7c3d8c9a439fede00d2600032d5db0be71c3c29#code

さらにパブリックブロックチェーン上で発行されているので**どのくらい流通していて誰がいつどのくらい送金したのかを追跡することが可能**となっています！

以下は、**キリフダ株式会社**というスタートアップが作成したJPYC用のモニタリングダッシュボードです！  

https://dune.com/kirifuda_hq/jpyc-dashboard

現在は、 **Ethereum**、**Polygon**、**Avalanche**という3つのパブリックブロックチェーンで流通しています。

**Dune**というブロックチェーン用のアナリティクスツールを使っており、**ブロックチェーン**に特化した**BigQuery** + **Locker**だと思ってもらえればOKです！

https://dune.com/

---

ちなみにドル建てのステーブルコインとして**USDC**というものも存在します。

https://www.circle.com/usdc

:::message
**USDC**の発行元は**Circle**という会社です。
:::

---

前置きが長くなりましたが、実態はプログラムであることが分かっていただけたと思います。

**これを自然言語で操作できたらめっちゃUI/UX向上しそうですよね！！**

なので **そのAI Agentを作ってみたよ！** というのが今回の趣旨になります！

今回作成したAI Agentは、学習コンテンツとしてOSSでも公開しています！

よろしければぜひご覧ください！

> UNCHAINの教材リンク

https://buidl.unchain.tech/JPYC/AI-Agent-JPYC-ChatApp/

# 今回作ったもの

**「でどんなもの作ったの？！」**

ということなのですが....

アプリのデモはこちらになります！！

https://x.com/UNCHAIN_tech/status/1984860259698327591

**JPYC SDK**をMCP化させて**Mastra**製のAI Agentから自然言語で残高情報を問い合わせたり、誰かに送金したりすることが可能となっています！！

## システム構成図

今回のAI Agentのシステム構成は以下のようになっており、**フルサーバーレスなアプリ構成となっています**！

![](/images/jpyc_ai_agent-1/jpyc.drawio.png)

## 技術スタック

採用している技術スタックは主に以下となります！

- **プログラミング言語**
  - TypeScript
- **Web3系**
  - JPYC SDK 
  - Viem
- **AI系**
  - Mastra
  - MCP
- **フロントエンド系**
  - Next.js
  - Tailwind CSS
- **フォーマッター＆リンター**
  - Biome

# 実装でポイントとなる箇所

今回のアプリで重要となったポイントを解説します！

## JPYC SDKのMCP化

まずは **JPYC SDK**の**MCP**から！

https://github.com/jcam1/JPYCv2

**JPYC SDK**はTypeScriptで実装されており、**Ethereum**や**Polygon**など複数のブロックチェーンに対応しています！

これを **Anthropic**社が発表した**MCP**の規格に準拠してMCP化させてみました！

https://github.com/modelcontextprotocol/typescript-sdk

コード一式は以下に格納されています

https://github.com/unchain-tech/jpyc-ai-agent/tree/complete/external/mcp

まずJPYC SDKを初期化し各メソッドを呼び出すコードを実装する必要があります！

> JPYC SDKの実装については以下の解説を参照ください！

::::details jpyc.tsについて

今回はSDKが提供している機能のうち、

- **残高取得**
- **操作先ブロックチェーン切り替え**
- **送金**
- **総供給量取得**

の4つのメソッドを使うことにしました！

```ts
import { JPYC, type IJPYC, SdkClient, type ISdkClient } from "@jpyc/sdk-core";
import type { Hex } from "viem";
import type { PrivateKeyAccount } from "viem/accounts";

// サポートするチェーン
export type SupportedChain = "sepolia" | "amoy" | "fuji";

// JPYC SDKで使用するチェーンIDのマッピング
const CHAIN_ID_MAP: Record<SupportedChain, number> = {
	sepolia: 11155111, // Ethereum Sepolia
	amoy: 80002, // Polygon Amoy
	fuji: 43113, // Avalanche Fuji
};

const CHAIN_NAMES: Record<SupportedChain, string> = {
	sepolia: "Ethereum Sepolia",
	amoy: "Polygon Amoy",
	fuji: "Avalanche Fuji",
};

// チェーンごとのRPC URL
const RPC_URLS: Record<SupportedChain, string> = {
	sepolia: "https://ethereum-sepolia-rpc.publicnode.com",
	amoy: "https://rpc-amoy.polygon.technology",
	fuji: "https://api.avax-test.network/ext/bc/C/rpc",
};

// 現在選択されているチェーン（デフォルトはSepolia）
let _currentChain: SupportedChain = "sepolia";
let _jpycInstance: IJPYC | null = null;
let _account: PrivateKeyAccount | null = null;

/**
 * JPYC SDKインスタンスを生成するメソッド
 * @param chain
 */
function createJpycInstance(chain: SupportedChain) {
	// 環境変数の検証
	if (!process.env.PRIVATE_KEY) {
		throw new Error("PRIVATE_KEY environment variable is required");
	}

	const chainId = CHAIN_ID_MAP[chain];

	// SdkClientの初期化
	const sdkClient: ISdkClient = new SdkClient({
		chainId,
		rpcUrl: RPC_URLS[chain],
	});

	// アカウントの作成
	_account = sdkClient.configurePrivateKeyAccount({
		privateKey: process.env.PRIVATE_KEY as Hex,
	});

	// Clientの生成
	const client = sdkClient.configureClient({
		account: _account,
	});

	// JPYC SDKインスタンスの作成
	_jpycInstance = new JPYC({
		env: "prod",
		contractType: "jpycPrepaid",
		localContractAddress: undefined,
		client,
	});
}

/**
 * JPYC SDKインスタンスを取得するメソッド
 * @returns
 */
function getJpycInstance(): IJPYC {
	if (!_jpycInstance) {
		createJpycInstance(_currentChain);
	}
	return _jpycInstance!;
}

/**
 * チェーンを切り替える関数
 * @param chain
 */
export function switchChain(chain: SupportedChain): void {
	if (!CHAIN_ID_MAP[chain]) {
		throw new Error(
			`Unsupported chain: ${chain}. Supported chains: sepolia, amoy, fuji`,
		);
	}
	_currentChain = chain;
	// JPYC SDKインスタンスを再作成
	createJpycInstance(chain);
}

/**
 * 現在のチェーンを取得する関数
 * @returns
 */
export function getCurrentChain(): SupportedChain {
	return _currentChain;
}

/**
 * チェーンの表示名を取得する関数
 * @param chain
 * @returns
 */
export function getChainName(chain?: SupportedChain): string {
	const targetChain = chain || _currentChain;
	return CHAIN_NAMES[targetChain] || "Ethereum Sepolia";
}

/**
 * 現在のアカウントアドレスを取得する関数
 * @returns
 */
export function getCurrentAddress(): Hex {
	if (!_account) {
		// アカウントが未初期化の場合、JPYC SDKインスタンスを初期化
		getJpycInstance();
	}
	return _account!.address;
}

/**
 * JPYC操作インターフェース（JPYC SDKを使用）
 */
export const jpyc = {
	/**
	 * 総供給量を取得するメソッド
	 * @returns
	 */
	async totalSupply(): Promise<string> {
		try {
			const jpycInstance = getJpycInstance();
			// JPYC SDKのtotalSupply関数を呼び出す
			const result = await jpycInstance.totalSupply();
			// numberをstringに変換して返す
			return result.toString();
		} catch (error: any) {
			console.error("[jpyc.totalSupply] Error:", error);

			// コントラクトが存在しない場合のエラーハンドリング
			if (
				error.message?.includes("returned no data") ||
				error.message?.includes("0x")
			) {
				const chainName = getChainName(_currentChain);
				throw new Error(
					`JPYCコントラクトが${chainName}にデプロイされていないか、アドレスが正しくありません。` +
						`Ethereum Sepoliaでお試しください。`,
				);
			}

			throw new Error(`Failed to get total supply: ${error.message}`);
		}
	},

	/**
	 * JPYCの残高を取得するメソッド
	 * @param params
	 * @returns
	 */
	async balanceOf(params: { account: Hex }): Promise<string> {
		try {
			const jpycInstance = getJpycInstance();
			// JPYC SDKのbalanceOf関数を呼び出す
			const result = await jpycInstance.balanceOf({ account: params.account });
			// numberをstringに変換して返す
			return result.toString();
		} catch (error: any) {
			console.error("[jpyc.balanceOf] Error:", error);

			// コントラクトが存在しない場合のエラーハンドリング
			if (
				error.message?.includes("returned no data") ||
				error.message?.includes("0x")
			) {
				const chainName = getChainName(_currentChain);
				throw new Error(
					`JPYCコントラクトが${chainName}にデプロイされていないか、アドレスが正しくありません。` +
						`現在のチェーンを確認してください。`,
				);
			}

			throw new Error(`Failed to get balance: ${error.message}`);
		}
	},

	/**
	 * JPYCを送金するメソッド
	 * @param params
	 * @returns
	 */
	async transfer(params: { to: Hex; value: number }): Promise<string> {
		try {
			const jpycInstance = getJpycInstance();
			// JPYC SDKのtransfer関数を呼び出す
			// SDKはnumberを受け取り、内部で適切に変換する
			const hash = await jpycInstance.transfer({
				to: params.to,
				value: params.value,
			});

			return hash;
		} catch (error: any) {
			console.error("[jpyc.transfer] Error:", error);
			throw new Error(`Failed to transfer: ${error.message}`);
		}
	},
};
```
::::

これで核の部分は実装できました！

後は、 **MCP用のライブラリ**を使って実装することが必要になってきます！

具体的に**MCP化**に必要なことは以下の4つです。

これはツールごとに必要になってきます。

- `ツールの説明文の作成(重要)`
- `入力スキーマの定義`
- `具体的な処理内容の実装`
- `エラーハンドリングの実装`

Mastraとの統合を考えて`@mastra/core`を使ってまずはツールの定義を行います。

```ts
/**
 * JPYC Tools for Mastra
 *
 * JPYC SDKの機能をMastraツールとして提供
 */

import { createTool } from "@mastra/core/tools";
import { z } from "zod";
import {
	getChainName,
	getCurrentAddress,
	getCurrentChain,
	jpyc,
	type SupportedChain,
	switchChain,
} from "./jpyc/sdk";

// エクスプローラーURLマッピング
const EXPLORER_URLS: Record<SupportedChain, string> = {
	sepolia: "https://sepolia.etherscan.io/tx/",
	amoy: "https://amoy.polygonscan.com/tx/",
	fuji: "https://testnet.snowtrace.io/tx/",
};

/**
 * JPYC残高照会ツール
 * 指定したアドレスのJPYC残高を照会します（現在選択されているテストネット）
 */
export const jpycBalanceTool = createTool({
	id: "jpyc_balance",
	description:
		"指定したアドレスのJPYC残高を照会します（現在選択されているテストネット）。アドレスが指定されていない場合は、現在のウォレットアドレスの残高を返します。",
	inputSchema: z.object({
		address: z
			.string()
			.optional()
			.describe(
				"残高を照会するEthereumアドレス（省略時は現在のウォレットアドレス）",
			),
	}),
	execute: async ({ context }) => {
		try {
      // ウォレットアドレスを取得
			const { address } = context;
			// 現在接続中のチェーン情報を取得
			const currentChain = getCurrentChain();
			const chainName = getChainName(currentChain);

			// アドレスが指定されていない場合は、現在のアカウントアドレスを使用
			const targetAddress = address || getCurrentAddress();
      // 残高取得メソッドを呼び出す
			const balanceString = await jpyc.balanceOf({
				account: targetAddress as `0x${string}`,
			});

			console.log(
				`jpyc_balance: address=${targetAddress}, balance=${balanceString} JPYC`,
			);

			return {
				success: true,
				address: targetAddress,
				balance: `${balanceString} JPYC`,
				balanceRaw: balanceString,
				chain: currentChain,
				chainName: chainName,
			};
		} catch (error: unknown) {
			return {
				success: false,
				error: error instanceof Error ? error.message : String(error),
			};
		}
	},
});

/**
 * JPYC送金ツール
 * JPYCトークンを指定したアドレスに送金します（現在選択されているテストネット）
 */
export const jpycTransferTool = createTool({
	id: "jpyc_transfer",
	description:
		"JPYCトークンを指定したアドレスに送金します（現在選択されているテストネット）。例: 10 JPYCを0x123...に送る",
	inputSchema: z.object({
		to: z.string().describe("送信先のEthereumアドレス (0xから始まる42文字)"),
		amount: z.number().describe("送金額（JPYC単位、例: 10）"),
	}),
	execute: async ({ context }) => {
		try {
			const { to, amount } = context;
			// 現在接続中のチェーン情報を取得
			const currentChain = getCurrentChain();
			const chainName = getChainName(currentChain);

			// SDKのtransferメソッドを呼び出してJPYCを送金する
			const txHash = await jpyc.transfer({
				to: to as `0x${string}`,
				value: amount,
			});

			const explorerUrl = EXPLORER_URLS[currentChain];

			return {
				success: true,
				message: `✅ ${amount} JPYCを ${to} に送金しました（${chainName}）`,
				transactionHash: txHash,
				explorerUrl: `${explorerUrl}${txHash}`,
				chain: currentChain,
				chainName: chainName,
			};
		} catch (error: unknown) {
			return {
				success: false,
				error: error instanceof Error ? error.message : String(error),
			};
		}
	},
});

/**
 * チェーン切り替えツール
 * JPYCを操作するテストネットを切り替えます
 */
export const jpycSwitchChainTool = createTool({
	id: "jpyc_switch_chain",
	description:
		"JPYCを操作するテストネットを切り替えます。対応チェーン: sepolia (Ethereum), amoy (Polygon), fuji (Avalanche)。ユーザーが「Sepoliaで」「Amoyに切り替えて」「Avalancheで実行」などと言った場合に使用します。",
	inputSchema: z.object({
		chain: z
			.enum(["sepolia", "amoy", "fuji"])
			.describe(
				"切り替え先のチェーン: sepolia (Ethereum Sepolia), amoy (Polygon Amoy), fuji (Avalanche Fuji)",
			),
	}),
	execute: async ({ context }) => {
		try {
			const { chain } = context;
			// 接続前のチェーンを取得
			const previousChain = getCurrentChain();
			// チェーンを切り替え
			await switchChain(chain as SupportedChain);

			const newChainName = getChainName(chain as SupportedChain);
			const previousChainName = getChainName(previousChain);

			return {
				success: true,
				message: `✅ チェーンを ${previousChainName} から ${newChainName} に切り替えました`,
				previousChain: previousChain,
				newChain: chain,
				chainName: newChainName,
			};
		} catch (error: unknown) {
			return {
				success: false,
				error: error instanceof Error ? error.message : String(error),
			};
		}
	},
});

/**
 * 現在のチェーン取得ツール
 * 現在選択されているテストネットを取得します
 */
export const jpycGetCurrentChainTool = createTool({
	id: "jpyc_get_current_chain",
	description:
		"現在選択されているテストネットを取得します。ユーザーが「今どのチェーン？」「現在のネットワークは？」などと聞いた場合に使用します。",
	inputSchema: z.object({}),
	execute: async () => {
		try {
			// 現在接続中のチェーン情報を取得
			const currentChain = getCurrentChain();
			const chainName = getChainName(currentChain);

			return {
				success: true,
				chain: currentChain,
				chainName: chainName,
				address: getCurrentAddress(),
			};
		} catch (error: unknown) {
			return {
				success: false,
				error: error instanceof Error ? error.message : String(error),
			};
		}
	},
});

/**
 * 総供給量照会ツール
 * 現在選択されているテストネットでのJPYCの総供給量を照会します
 */
export const jpycTotalSupplyTool = createTool({
	id: "jpyc_total_supply",
	description:
		"現在選択されているテストネットでのJPYCの総供給量を照会します。ユーザーが「総供給量は？」「流通量を教えて」などと聞いた場合に使用します。",
	inputSchema: z.object({}),
	execute: async () => {
		try {
			// 現在接続中のチェーン情報を取得
			const currentChain = getCurrentChain();
			const chainName = getChainName(currentChain);
			// SDKのtotalSupplyメソッドを呼び出して総供給量を取得する
			const totalSupply = await jpyc.totalSupply();

			return {
				success: true,
				totalSupply: `${totalSupply} JPYC`,
				totalSupplyRaw: totalSupply,
				chain: currentChain,
				chainName: chainName,
			};
		} catch (error: unknown) {
			return {
				success: false,
				error: error instanceof Error ? error.message : String(error),
			};
		}
	},
});

/**
 * すべてのJPYCツールをエクスポートする
 */
export const jpycTools = {
	jpyc_balance: jpycBalanceTool,
	jpyc_transfer: jpycTransferTool,
	jpyc_switch_chain: jpycSwitchChainTool,
	jpyc_get_current_chain: jpycGetCurrentChainTool,
	jpyc_total_supply: jpycTotalSupplyTool,
};
```

そしてこれを使って**McpServer**コントスラクターを使ってMCPサーバー化させます。

```ts
/**
 * JPYC MCP Server
 *
 * このサーバーはJPYC SDKの機能をMCPプロトコル経由で公開します。
 * HTTP/SSEを使用して、MCPClientから接続できるようにします。
 */
import "dotenv/config";
import { MCPServer } from "@mastra/mcp";
import http from "node:http";
import { jpycTools } from "./tools"; // ツールを読み込む

const PORT = process.env.MCP_PORT || 3001;

/**
 * JPYC MCP Server インスタンス
 */
const server = new MCPServer({
	name: "jpyc-sdk",
	version: "1.0.0",
	tools: jpycTools, //割り当てるツールの指定
});

/**
 * HTTPサーバーを作成してMCPServerを統合
 */
const httpServer = http.createServer(async (req, res) => {
	console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);

	// CORSヘッダーを設定（Next.jsアプリからのアクセスを許可）
	res.setHeader("Access-Control-Allow-Origin", "*");
	res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
	res.setHeader("Access-Control-Allow-Headers", "Content-Type");

	if (req.method === "OPTIONS") {
		res.writeHead(200);
		res.end();
		return;
	}

	// ヘルスチェックエンドポイント
	if (req.url === "/health" && req.method === "GET") {
		res.writeHead(200, { "Content-Type": "application/json" });
		res.end(JSON.stringify({ status: "ok", server: "jpyc-mcp-server" }));
		return;
	}

	// MCP SSEエンドポイント
	try {
		await server.startSSE({
			url: new URL(req.url || "", `http://localhost:${PORT}`),
			ssePath: "/sse",
			messagePath: "/message",
			req,
			res,
		});
	} catch (error) {
		console.error("MCP Server error:", error);
		if (!res.headersSent) {
			res.writeHead(500, { "Content-Type": "application/json" });
			res.end(JSON.stringify({ error: "Internal server error" }));
		}
	}
});

// サーバー起動
httpServer.listen(PORT, () => {
	console.log(`
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║          🚀 JPYC MCP Server is running!                   ║
║                                                            ║
║  SSE Endpoint:     http://localhost:${PORT}/sse               ║
║  Message Endpoint: http://localhost:${PORT}/message           ║
║  Health Check:     http://localhost:${PORT}/health            ║
║                                                            ║
║  Available Tools:                                          ║
║    - jpyc_balance           (残高照会)                     ║
║    - jpyc_transfer          (送金)                         ║
║    - jpyc_switch_chain      (チェーン切り替え)             ║
║    - jpyc_get_current_chain (現在のチェーン取得)           ║
║    - jpyc_total_supply      (総供給量照会)                 ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
  `);
});

// エラーハンドリング
httpServer.on("error", (error) => {
	console.error("HTTP Server error:", error);
	process.exit(1);
});

// graceful shutdown
process.on("SIGTERM", () => {
	console.log("SIGTERM signal received: closing HTTP server");
	httpServer.close(() => {
		console.log("HTTP server closed");
		process.exit(0);
	});
});

process.on("SIGINT", () => {
	console.log("\nSIGINT signal received: closing HTTP server");
	httpServer.close(() => {
		console.log("HTTP server closed");
		process.exit(0);
	});
});
```

これでMCP化の部分はOKです！！

## MastraへのMCP組み込み方

今回試した方法は、 **Next.js**アプリへの直接統合になります。

以下のように **MCP クライアント**の設定を行います。

```ts
import { MCPClient } from "@mastra/mcp";

/**
 * JPYC MCPサーバーを呼び出すためのMCPクライアント
 */
export const jpycMCPClient = new MCPClient({
	servers: {
		// JPYC MCPサーバーのURLを設定する(MCPサーバー事前に起動しておくこと)
		"jpyc:mcp-server": {
			url: new URL(
				process.env.JPYC_MCP_SERVER_URL || "http://localhost:3001/sse",
			),
		},
	},
});
```

後は、**Mastra**が提供している機能を使って**AI Agent**化させればOKです！！

```ts
import { Agent } from "@mastra/core/agent";
import { claude } from "./model";

/**
 * JPYC エージェント
 *
 * MCP経由でJPYC SDKツールを使用するエージェント
 */
export const jpycAgent = new Agent({
	name: "JPYC Assistant",
	description:
		"JPYCトークンの操作をサポートするAIアシスタント（マルチチェーン対応）",
	model: claude, //モデル割り当て
	tools: async () => {
    // MCPClient経由でツールを動的に取得
		const { jpycMCPClient } = await import("@/lib/mastra/mcp/client");
		const tools = await jpycMCPClient.getTools();
		// biome-ignore lint/suspicious/noExplicitAny: MCPツールの型とMastraツールの型の互換性の問題
		return tools as any;
	},
	instructions: `
あなたはJPYC（日本円ステーブルコイン）の操作をサポートするAIアシスタントです。

対応テストネット: Ethereum Sepolia, Avalanche Fuji
デフォルトチェーン: Ethereum Sepolia

以下の操作が可能です：
1. **チェーン切り替え**: テストネットを変更
2. **送金**: 指定したアドレスにJPYCを送金（現在選択中のチェーン）
3. **残高照会**: アドレスのJPYC残高を確認（現在選択中のチェーン、アドレス省略時は自分の残高）
4. **総供給量照会**: JPYCの総供給量を確認（現在選択中のチェーン）

ユーザーの自然言語の指示を解釈し、適切なツールを呼び出してください。

## 名前を使った操作について:
メッセージの最後に[ユーザー情報]として、ユーザーの名前と友達リストが含まれている場合があります。
- 「太郎に100JPYC送って」のような名前を使った送金指示の場合、友達リストから該当する名前のアドレスを探してjpyc_transferを実行してください
- 「太郎の残高教えて」のような場合、友達リストから該当する名前のアドレスを探してjpyc_balanceを実行してください
- 「残高教えて」や「私の残高」のような場合は、自分のアドレスを使用してjpyc_balanceを実行してください
- 友達リストに該当する名前がない場合は、「{名前}さんは友達リストに登録されていません」と返答してください

例:
- "Sepoliaに切り替えて" → jpyc_switch_chain (chain: "sepolia")
- "Amoyで実行して" → jpyc_switch_chain (chain: "amoy")
- "Avalancheに変更" → jpyc_switch_chain (chain: "fuji")
- "現在のチェーンは?" → jpyc_get_current_chain
- "0x123...に10JPYC送って" → jpyc_transfer
- "太郎に100JPYC送って" → 友達リストから太郎のアドレスを探してjpyc_transfer
- "私の残高を教えて" または "残高教えて" → jpyc_balance (addressなし、または自分のアドレス)
- "太郎の残高教えて" → 友達リストから太郎のアドレスを探してjpyc_balance
- "0x123...の残高を教えて" → jpyc_balance (address: "0x123...")
- "JPYCの総供給量は?" または "流通量教えて" → jpyc_total_supply
- "Amoyで0x123...に10JPYC送って" → まずjpyc_switch_chain、次にjpyc_transfer

## 重要な回答スタイル:
- **カジュアルで親しみやすい会話調で返答してください**
- **ユーザーの名前が登録されている場合、適宜名前を使って親しみやすく返答してください**
- 絵文字（💰、📊、✅など）は使わないでください
- 引用符（"""）やマークダウンの太字（**）は最小限にしてください
- チャットアプリのような自然な会話を心がけてください

## 回答例:
- **送金成功時**:
  「{to} に {amount} JPYC送りました！トランザクションは[こちらで確認]({explorerUrl})できます（{chainName}）」
  名前を使った場合: 「{friendName}さんに {amount} JPYC送りました！トランザクションは[こちらで確認]({explorerUrl})できます（{chainName}）」

- **残高照会時**:
  「{chainName}チェーンの残高は {balance} JPYC です」
  自分の名前がある場合: 「{userName}さんの{chainName}チェーンの残高は {balance} JPYC です」
  友達の残高の場合: 「{friendName}さんの{chainName}チェーンの残高は {balance} JPYC です」

- **総供給量照会時**:
  「現在の{chainName}での総供給量は {totalSupply} JPYC です」

- **チェーン切り替え時**:
  「{newChain} に切り替えました」

- **エラー時**:
  「エラーが発生しました: {errorMessage}」

重要:
- リンクは必ずマークダウン形式で表示してください（例: [こちらで確認](https://sepolia.etherscan.io/tx/0x...)）
- 数値は読みやすいように適宜カンマ区切りにしてください
  `.trim(),
});
```

以上でポイントとなった箇所の解説は終了です！

# 動かし方

では最後に動かし方について解説を行います！

## セットアップ

まずはリポジトリを自分のアカウントにフォークしてきてローカルにクローンしましょう！

```bash
git clone --recurse-submodules https://github.com/YOUR_USERNAME/jpyc-ai-agent.git
cd jpyc-ai-agent
```

とりあえず試してみたい方はブランチを`complete`に切り替えてください。

そして依存関係をインストールします。

```bash
pnpm install
```

次に環境変数用のファイルを作成します。

```bash
cp .env.local.example .env.local
```

以下の値を設定する必要があります(モデルの部分は使いたいやつだけセットすればOKです)。

```txt
# ⚠️ 本番環境では絶対に使用しないでください！テストネット専用です
# テストネット用の秘密鍵
PRIVATE_KEY=0x... 

# AI API Keys(自分の使いたいモデルに必要なAPIキーをセットしてください。 ※ Claudeを推奨)
OPENAI_API_KEY=sk-proj-... # OpenAI APIキー
GOOGLE_GENERATIVE_AI_API_KEY= # Gemini APIキー
ANTHROPIC_API_KEY= # Claude APIキー
# JPYC MCPサーバーURL
JPYC_MCP_SERVER_URL="http://localhost:3001/sse"
```

## ビルド

次にMCPとアプリの両方をビルドします！

:::message
アプリ起動前に必ず実行してください。
:::

```bash
pnpm build
```

エラーが出なければOKです！

## MCPサーバーを起動させる

以下のコマンドでMCPサーバーを起動させます！

```bash
pnpm run mcp:dev
```

これで、 `http://localhost:3001` でJPYC MCPサーバーが立ち上がります。

## アプリを起動させる

ではいよいよアプリの起動です！！

```bash
pnpm run dev
```

アプリケーションが `http://localhost:3000` で起動します。

**もしAIチャットの出力がオブジェクト形式になっている場合は `src/lib/mastra/agent.ts`で使用しているモデルを別のもの(geminiなど)に切り替えてみてください。**

うまくいけば冒頭で紹介したデモのように自然言語で自分の資産を問い合わせたりすることが可能になっているはずです！

テストネット用のJPYCは以下のサイトで取得が可能です！

https://faucet.jpyc.jp/

# まとめ

今回は以上となります！

今後やってみたいこととしては**Cloud Run**上で動かしてみたりとか**MCPに認証機能を追加**してみることなどですかね。決済が求められる具体的なユースケースと合わせて使ってみても良いなと思っています！

**A2A**を使って他のタスクを担当するAI Agentと組み合わせてマルチAI Agentを実装してみるというのも面白そうです！

MCPの認可に関連する動きとして**OAuth2.1**が注目されているみたいなのでそっちにもアンテナを貼りたいなと思っています。

https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization

https://serverless.co.jp/blog/pfwq650kp0/

---

**金融**と密接にくっついてしまってはいますが、インフラテクノロジーとしては非常に大きな可能性もっているのが**ブロックチェーン**だと考えています。

データを永続的に保存し、**Lambda**のように独自のロジックを実装したプログラムを自由にデプロイし、公開できる....

それって、**めちゃくちゃ面白くないですか？！**

今回は少しでも**Web3**とかも面白さとかも伝えらればと思って記事を書いてみました〜〜！！

この記事が少しでも皆さんの参考になれば幸いです！

本当にここまで読んでいただきありがとうございました！！

# 参考文献

https://mastra.ai/

https://github.com/mastra-ai/mastra

https://github.com/modelcontextprotocol/typescript-sdk

https://github.com/jcam1/JPYCv2