---
title: "VibeKanbanを使ってCloudFlareWorkersにx402MCPサーバーを開発＆デプロイしてみた！"
emoji: "💵"
type: "tech" 
topics: ["blockchain","web3","cloudflare","mcp","ai"]
published: false
---

# はじめに

皆さん、こんにちは！

先日初めてちゃんと**Cloudflare Workers**について勉強してみたのでそのアウトプットの記事を書いてみました！

今回は実装で試してみたことやMCPサーバーを**Cloudflare Workers**にデプロイする方法などをシェアする記事になっています！

# CloudFlare Workerとは？

https://www.cloudflare.com/ja-jp/developer-platform/products/workers/

**Cloudflare Workers**は、**Cloudflare**社が展開しているサーバーレスコンピューティングプラットフォームです。

バンドルサイズなど一部制約がありますが、TypeScript/JavaScript製のアプリをフロントエンド感覚で簡単にデプロイすることができる点が魅力です！

その他、**KV**や**D1**など**Cloudflare**の主力サービスとも連携しやすい点が魅力と言えます！

# Honoとの相性の良さ

https://hono.dev/

Honoは、主にTypeScript/JavaScriptでWebアプリケーションやAPIを開発するための、軽量・高速・モダンなWebフレームワークです。

高速かつ軽量であるなど**Cloudflare Workersとは非常に相性が良い**です！

# Vibe Kanbanとは

https://vibekanban.com/

AIコーディングエージェント（Claude CodeやCodex）をカンバン方式（タスクの見える化）で管理し、自動化された開発フローを実現するツールです！

## cc-sdd + VibeKanban + GitWorkTreeによる開発のワークフロー

今回実装するにあたり以下のような開発ワークフローを実践してみました。

- 0. プロダクトのビジョン、コンセプトを策定する
- 1. cc-sddで要件定義と設計書、タスクリストを作成する
- 2. VibeKanbanにタスクを登録(GitHubにイシュー登録)
  ![](/images/web3_cloudflare_workers-1/0.png)
- 3. git worktreeで作業ディレクトリを準備
  ![](/images/web3_cloudflare_workers-1/1.png)
- 4. タスクの並列実行
  ![](/images/web3_cloudflare_workers-1/3.png)
- 5. 各成果物をセルフレビュー・PR作成
  ![](/images/web3_cloudflare_workers-1/5.png)

  コードレビューには**CodeRabbit**を使ってみました！

  ![](/images/web3_cloudflare_workers-1/6.png)

## cc-sddで生成したタスクをVibeKanban用のタスクに変換・登録する方法

cc-sddで生成したタスクをVibeKanban用のタスクに変換・登録するために以下のようなプロンプトを使ってみました！

```bash
@(cc-sddで生成したタスクリスト)を確認して、作業計画を Task 単位で vibe_kanban へ Task として登録してください。

タスクには以下の内容を記載します:

- 設計は @design.md を参照すること
- このタスクでの具体的な作業内容
- 依存する他のタスクや、並列作業が可能かどうか
- 並列実行できる場合は、タイトルに + をつけてください

タスクは降順に登録してください。
```

そのままGitHub イシュー化できてしまえるのが良い点ですね！

# x402とは？

https://www.x402.org/

x402は米国で著名な暗号資産交換所である**Coinbase**社が発表したステーブルコイン決済のため標準プロトコルです。

その名の通りHTTPステータスコード402 **Payment Required** を採用しており、HTTPプロトコルに準拠している点が非常に話題となりました。

**Cloudflare**社とはx402 foundationも設立している他、AI Agentとも相性が良いことから数あるブロックチェーンの技術スタックでも大きな注目を集めている技術になります。

https://blog.cloudflare.com/x402/

# 今回作ったアプリについて

## 概要

**Cloudflare Workers**にx402バックエンドサーバーとMCPサーバーをデプロイして、さらにGPT App内のチャットインターフェースから天気予報の情報を取得すると同時にステーブルコイン支払いが行われるサンプルアプリを作りました！

できること
- GPT App から get_weather ツールを呼び出して天気情報を取得
- x402 による支払い検証を通過したリクエストのみ /weather にアクセス
- Cloudflare Workers 上で x402server と mcpserver を分離デプロイ
- E2E テストで mcpserver -> x402FetchClient -> x402server の結合動作を検証

## サンプルコード

今回試したソースコードは以下のGitHubリポジトリに格納しています。

https://github.com/mashharuki/vibekanban-gitworktree-sample

### リポジトリ構成

| パス                    | 役割                                                                     | 主な技術                                                          |
| ----------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| `pkgs/x402server`       | 天気 API と x402 決済検証を提供するバックエンド                          | Hono / x402 / Cloudflare Workers / TypeScript                     |
| `pkgs/mcpserver`        | GPT App から呼び出される MCP サーバー。`x402server` を決済付きで呼び出す | Hono MCP / MCP SDK / x402 fetch / Cloudflare Workers / TypeScript |
| ルート (`package.json`) | monorepo の共通スクリプト・ワークスペース管理                            | pnpm workspace                                                    |

## 実装した機能一覧

| 機能                             | 概要                                         | 提供パッケージ            | 補足                               |
| -------------------------------- | -------------------------------------------- | ------------------------- | ---------------------------------- |
| ヘルスチェック API               | サービス稼働確認 (`/`, `/health`)            | `x402server`, `mcpserver` | 監視・疎通確認に利用               |
| 天気情報取得 API                 | 都市名を受けて天気を返却 (`/weather`)        | `x402server`              | 都市未登録時は 404                 |
| x402 課金付きアクセス制御        | `/weather` を課金保護し未決済時は 402 を返却 | `x402server`              | 価格・ネットワークは環境変数で設定 |
| MCP ツール公開                   | `get_weather` ツールを外部クライアントへ公開 | `mcpserver`               | 入力検証・エラー整形を実施         |
| x402 決済付き fetch クライアント | 支払い情報付きで `x402server` を呼び出す     | `mcpserver`               | Service Binding / URL の両方に対応 |
| E2E 結合テスト                   | MCP から backend までの通し動作を検証        | `mcpserver` テスト        | 402/404/正常系を確認               |

# ポイントなる実装部分

簡単に重要な箇所をピックアップして実装部分を紹介していきます。

## x402サーバー編

まずx402サーバーの方からになります！

環境変数を設定するので`wrangler.jsonc`に環境変数の設定が必要になります。

今回は機密性の高いものはないので**Secret**の機能は使いません。

```json
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "x402server",
  "main": "src/index.ts",
  "compatibility_date": "2026-02-23",
  "compatibility_flags": ["nodejs_compat"],
  "vars": {
    "SERVER_WALLET_ADDRESS": "0x51908F598A5e0d8F1A3bAbFa6DF76F9704daD072",
    "FACILITATOR_URL": "https://x402.org/facilitator",
    "X402_PRICE_USD": "$0.01",
    "X402_NETWORK": "eip155:84532"
  }
}
```

x402サーバーは**Hono**をベースに作っています！  
メインとなるコードは`src/app.ts`になります。

特定のルートに対してのみx402のミドルウェアが適用されるようになっています。

```ts
import { paymentMiddleware } from "@x402/hono";
import { Hono } from "hono";
import { createRoutes } from "./route";
import { createResourceServer, resolvePaymentOptions } from "./utils/config";
import type { CreateAppOptions, ErrorResponse, WeatherService } from "./utils/types";
import { createMockWeatherService } from "./weather/service";

const toErrorResponse = (statusCode: number, message: string): ErrorResponse => ({
  statusCode,
  message,
});

/**
 * Hono アプリケーションを作成します。
 * @param weatherService
 * @param options
 * @returns
 */
export const createApp = (
  weatherService: WeatherService = createMockWeatherService(),
  options: CreateAppOptions = {},
): Hono => {
  // Hono アプリ本体。テスト時は createApp に依存を差し込んで利用する。
  const app = new Hono();

  const enablePayment = options.enablePayment ?? true;

  if (enablePayment) {
    const paymentOptions = resolvePaymentOptions(options.payment);
    const resourceServer = createResourceServer(paymentOptions);
    const routes = createRoutes(paymentOptions);
    const protectedRouteKeys = new Set(Object.keys(routes));
    let resourceServerInitialization: Promise<void> | null = null;

    // 保護対象ルートの初回アクセス時のみ resource server を初期化する。
    app.use(async (c, next) => {
      const routeKey = `${c.req.method.toUpperCase()} ${c.req.path}`;

      if (!protectedRouteKeys.has(routeKey)) {
        return next();
      }

      if (!resourceServerInitialization) {
        resourceServerInitialization = resourceServer.initialize().catch((error) => {
          resourceServerInitialization = null;
          throw error;
        });
      }

      await resourceServerInitialization;
      return next();
    });

    // x402 検証ミドルウェア。createRoutes で定義したルートにのみ課金を適用する。
    app.use(paymentMiddleware(routes, resourceServer, undefined, undefined, false));
  }

  app.get("/", (c) => {
    return c.json({ status: "ok" }, 200);
  });

  /**
   * ヘルスチェック用のルート
   */
  app.get("/health", (c) => {
    return c.json({ status: "ok" }, 200);
  });

  /**
   * 天気情報を取得するルート
   */
  app.get("/weather", async (c) => {
    const city = c.req.query("city")?.trim();

    if (!city) {
      return c.json(toErrorResponse(400, "city query parameter is required"), 400);
    }

    try {
      const weather = await weatherService.getWeatherByCity(city);

      if (!weather) {
        // 入力自体は妥当だが対象都市が未登録のケース。
        return c.json(toErrorResponse(404, "city not found"), 404);
      }

      return c.json(weather, 200);
    } catch {
      // 外部 API 障害など、サービス内部失敗は 503 で返す。
      return c.json(toErrorResponse(503, "weather service unavailable"), 503);
    }
  });

  return app;
};
```

天気予報を取得するロジックについてですが、今回は検証目的ということもあり外部のAPI等を叩いているのではなく決めうちのデモデータを返す実装としています。

プロダクションレベルで作る場合はここが外部のAPIになるイメージです。

```ts
import { WeatherData, WeatherService } from "../utils/types";

// モックの天気予報データ
const MOCK_WEATHER_DATA: ReadonlyArray<WeatherData> = [
  {
    city: "Tokyo",
    condition: "Sunny",
    temperatureC: 28,
    humidity: 60,
  },
  {
    city: "Osaka",
    condition: "Cloudy",
    temperatureC: 26,
    humidity: 65,
  },
  {
    city: "New York",
    condition: "Rainy",
    temperatureC: 22,
    humidity: 72,
  },
];

const normalizeCity = (city: string): string => {
  // 引用符付き入力や "Tokyo, JP" のような表記ゆれを吸収する。
  const trimmed = city.trim().replace(/^['\"]+|['\"]+$/g, "");
  const withoutCountry = trimmed.split(",")[0]?.trim() ?? trimmed;

  return withoutCountry.toLowerCase();
};

/**
 * モックの天気予報を提供するWeatherServiceの実装を作成するファクトリーメソッド
 * @returns
 */
export const createMockWeatherService = (): WeatherService => {
  return {
    async getWeatherByCity(city: string): Promise<WeatherData | null> {
      const normalized = normalizeCity(city);

      // 都市名の正規化結果で比較し、大小文字差を無視して検索する。
      const weather = MOCK_WEATHER_DATA.find((item) => normalizeCity(item.city) === normalized);

      return weather ?? null;
    },
  };
};
```

**x402**固有の設定は`src/utils/config.ts`にまとめてあります！

x402サーバーの実装にはファシリテーターやリソースサーバーの設定が必要になります。

ここでは詳細を省きますが、ファシリテーターはx402を適用させたいAPIとブロックチェーンをつなぐ橋渡し的な要素で存在しており、支払いのための署名検証・トランザクション送信を担っています。

> ファシリテーターの詳細は以下の技術ブログでわかりやすく紹介されています！

https://zenn.dev/komlock_lab/articles/270e9273f3e7ec

ファシリテーターはオプションで自力で実装しても良いということにはなっていますが労力がかかりますので使用が推奨されています。

```ts
import { x402Client } from "@x402/axios";
import { HTTPFacilitatorClient, x402ResourceServer } from "@x402/core/server";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import type { PaymentOptions, ResolvedPaymentOptions } from "./types";

// クライアントインスタンスを作成
export const client = new x402Client();

/**
 * 必須の支払い設定をチェックするメソッド
 * @param value
 * @param key
 * @returns
 */
const requiredPaymentConfig = (value: string | undefined, key: string) => {
  if (value?.trim()) {
    return value;
  }

  throw new Error(`Missing required payment configuration: ${key}`);
};

/**
 * ファシリテーターURLを正規化します。
 * 特に、旧URLである https://facilitator.x402.org を https://x402.org/facilitator に変換します。
 * @param rawUrl
 * @returns
 */
const normalizeFacilitatorUrl = (rawUrl: string): string => {
  const trimmed = rawUrl.trim();

  if (trimmed === "https://facilitator.x402.org") {
    return "https://x402.org/facilitator";
  }

  const parsed = new URL(trimmed);
  if (parsed.hostname === "x402.org" && parsed.pathname === "/") {
    parsed.pathname = "/facilitator";
    return parsed.toString().replace(/\/$/, "");
  }

  return trimmed;
};

/**
 * 必須の支払い設定を取得します
 * @param payment
 * @returns
 */
export const resolvePaymentOptions = (payment: PaymentOptions = {}): ResolvedPaymentOptions => {
  // 引数優先、未指定時は環境変数にフォールバックする。
  const facilitatorUrl = requiredPaymentConfig(
    payment.facilitatorUrl ?? process.env.FACILITATOR_URL,
    "FACILITATOR_URL",
  );
  const normalizedFacilitatorUrl = normalizeFacilitatorUrl(facilitatorUrl);

  return {
    payTo: requiredPaymentConfig(payment.payTo ?? process.env.SERVER_WALLET_ADDRESS, "SERVER_WALLET_ADDRESS"),
    facilitatorUrl: normalizedFacilitatorUrl,
    price: requiredPaymentConfig(payment.price ?? process.env.X402_PRICE_USD, "X402_PRICE_USD"),
    network: requiredPaymentConfig(payment.network ?? process.env.X402_NETWORK, "X402_NETWORK"),
    facilitatorClient:
      payment.facilitatorClient ??
      new HTTPFacilitatorClient({
        url: normalizedFacilitatorUrl,
      }),
  };
};

/**
 * リソースサーバーインスタンスを作成する
 * @param paymentOptions
 * @returns
 */
export const createResourceServer = (paymentOptions: ResolvedPaymentOptions) => {
  // ネットワークごとの検証スキームを登録した resource server を生成する。
  return new x402ResourceServer(paymentOptions.facilitatorClient).register(
    paymentOptions.network as `${string}:${string}`,
    new ExactEvmScheme(),
  );
};
```

x402サーバーの実装の解説は以上です！

## MCPサーバー編

## Cloudflare Workersへのデプロイ方法！

ではコードの解説が終わったのでデプロイする方法を解説していきたいと思います！

### x402バックエンドサーバー

- セットアップ

  環境変数用のファイルを作成

  ```bash
  cp pkgs/x402server/.dev.vars.example pkgs/x402server/.dev.vars
  ```

- デプロイ

  ```bash
  pnpm x402server run deploy
  ```

### MCPサーバー

- セットアップ

  環境変数用のファイルを作成

  ```bash
  cp pkgs/mcpserver/.dev.vars.example pkgs/mcpserver/.dev.vars
  ```

  `X402_SERVER_URL`には上記でCloudFlare Workersにデプロイしたx402バックエンドサーバーのAPIエンドポイントURLを指定する

  (Cloudflare Workersにデプロイする場合)x402クライアント用の秘密鍵とx402バックエンドサーバーのエンドポイントの登録

  ```bash
  pnpm mcpserver run secret CLIENT_PRIVATE_KEY --name mcpserver
  pnpm mcpserver run secret X402_SERVER_URL --name mcpserver
  ```

- デプロイ

  ```bash
  pnpm mcpserver run deploy
  ```

  `https://mcpserver.<固有値>.workers.dev/mcp`をGPT AppのURLに登録すればチャットからx402の支払いができます！

# ChatGPTのチャットインターフェース内から呼び出す方法

1. MCPサーバーのエンドポイントをGPT Appに登録する
2. +ボタンから追加したアプリを選んで追加した状態で天気予報を教えてもらう
3. 天気予報が返ってきてUSDCが支払いされていればOK!

    ![](/images/web3_cloudflare_workers-1/7.png)

    ブロックエクスプローラーでステーブルコインが支払われているはず！

    ![](/images/web3_cloudflare_workers-1/11.png)

4. 検証が終わったら必ずサーバーを落とし、MCPサーバーの接続も解除して終わりです！

# まとめ



# 参考文献

- [【2026年最新】Claude Code作者が実践する「超並列駆動」開発術がエンジニアの常識を破壊していた](https://qiita.com/ot12/items/66e7c07c459e3bb7082d)
- [世界一わかりやすくGit worktreeを解説！AI駆動開発でも活用できる並列開発の方法](https://zenn.dev/tmasuyama1114/articles/git_worktree_beginner)
- [Claude Code × VibeKanban × git worktreeで実現するタスク並列実行のすすめ](https://zenn.dev/coconala/articles/379aadf643ecb8)
- [公式サイト - Vibekanban](https://vibekanban.com/)
- [GitHub - Vibekanban](https://github.com/BloopAI/vibe-kanban)
