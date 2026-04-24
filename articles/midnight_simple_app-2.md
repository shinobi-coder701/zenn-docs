---
title: "Midnight Lace Walletと接続するシンプルなアプリを作ってみよう！"
emoji: "🛡️"
type: "tech" 
topics: ["web3", "cardano", "privacy", "lacewallet", "typescript"]
published: true
publication_name: "midnight"
---

# はじめに

皆さん、こんにちは！

今回はプライバシー特化のブロックチェーンである**Midnight**とその専用ウォレットである**Lace Wallet**がテーマの記事になります！

https://www.lace.io/

公式ドキュメントにはコントラクトのデプロイや動かし方の解説は掲載されていたのですが、**Lace Wallet**とフロントエンドアプリの接続方法については見つからず試してみたらハマったポイントがいくつかあったので入門編としてシンプルなアプリを作ってみました！

ぜひ最後まで読んでいってください！

## この記事で学べること

- Lace Walletの概要が学べます
- Lace Walletと接続するシンプルなアプリの開発方法が学べます

# Lace Walletとは？

**Lace Wallet**は、 カルダノエイダの開発を担当している**IOG**が2022年6月9日に発表したCardano関連のデジタルアセットを保管・管理することができるライトウォレットです！

**Midnigt**をはじめとしたカルダノエコシステムのブロックチェーン上のデジタルアセットを管理することが可能です！

軽量なウォレットでありながらステーキングや資産の送金など多機能なウォレットとなっています。

今はカルダノエコシステムに最適化されていますが、将来的には他のブロックチェーンエコシステムにも対応していくようです！

# Lace Walletと接続するシンプルなアプリを作ろう！

## 前提条件

サンプルコードを動かす前に以下のことが必要となります！

- [Lace Wallet](https://www.lace.io/) ブラウザ拡張機能（Midnight 対応版）をインストール済みであること
- Lace の設定で **PreProd** ネットワークが選択されていること

## サンプルコードのGitHubリポジトリ

https://github.com/mashharuki/midnight-lace-react-sample-app

## アプリの起動イメージ

今回はLace Walletを接続して残高を表示するというシンプルなアプリです！

![](/images/midnight_simple_app-2/1.png)

![](/images/midnight_simple_app-2/2.png)

## アプリの機能一覧表

| 機能 | 説明 |
|---|---|
| Lace Wallet 接続 | `window.midnight.mnLace` を 100ms ポーリングで検出し接続 |
| バージョン検証 | Connector API バージョンが `>=1.0.0` か確認 |
| ネットワーク検証 | PreProd / mainnet / undeployed / preview の順に自動試行 |
| アドレス表示 | シールドアドレスをコピー可能な形式で表示 |
| 残高表示 | Shielded / Unshielded / Dust の 3 種を tDUST 単位で表示 |
| 言語切り替え | 右上ボタンで日本語 ⇆ English を即時切り替え（localStorage 永続化） |

## 技術スタック

| カテゴリ | ライブラリ / ツール |
|---|---|
| フレームワーク | React 19 + TypeScript |
| ビルド | Vite 8 |
| スタイリング | Tailwind CSS v4 (`@tailwindcss/vite`) |
| UI コンポーネント | shadcn/ui (Button, Badge, Card) + Lucide React |
| 国際化 | i18next 26 + react-i18next 17 |
| ウォレット連携 | `@midnight-ntwrk/dapp-connector-api` |
| 非同期処理 | RxJS 7 |
| パッケージマネージャー | Bun |
| フォーマッター | Biome |

## 重要な部分のソースコードの解説

基本的な考え方・構成は他のブロックチェーンアプリケーションと同じです！

専用のSDKやAPIの仕様がしっかり分かっていればすぐに接続可能なアプリケーションを開発することが可能です！

今回重要になるSDKは`@midnight-ntwrk/dapp-connector-api`です！！

これを使ってLace Walletとの接続ロジックを実装しています！

接続に関する重要な実装は全て以下のファイルにまとめてあります！

ポイントは103行目付近のところですね。

```ts
// 接続を試みる。ネットワーク不一致エラーが出たら次の候補にフォールバックする。
walletAPI = await connector.connect(networkId);
// Lace v4: getConfiguration() is on walletAPI (not connector)
const walletRaw = walletAPI as unknown as Record<string, unknown>;
```

ここで取得した`walletRaw`からウォレットアドレスなどを取得します。

```ts
let address = "";
let coinPublicKey = "";
let encryptionPublicKey = "";

if (typeof walletRaw.getShieldedAddresses === "function") {
  // getShieldedAddresses() may return an array (old versions) or a single object (new versions), so handle both cases
  const result = await (
    walletRaw.getShieldedAddresses as () => Promise<Record<string, unknown>>
  )();
  // Lace v4 returns a single object (not array):
  // { shieldedAddress, shieldedCoinPublicKey, shieldedEncryptionPublicKey }
  const entry = (Array.isArray(result) ? result[0] : result) as
    | Record<string, unknown>
    | undefined;
  if (entry) {
    address = String(entry.shieldedAddress ?? entry.address ?? "");
    coinPublicKey = String(
      entry.shieldedCoinPublicKey ?? entry.coinPublicKey ?? "",
    );
    encryptionPublicKey = String(
      entry.shieldedEncryptionPublicKey ?? entry.encryptionPublicKey ?? "",
    );
  }
}
```

残高取得は専用のReact hooksとして実装しています！

重要になるのは`fetchBalances`メソッドですね！

以下3種類のウォレットアドレスに紐づくデジタルアセットの残高を取得できます！

- `raw.getShieldedBalances`
- `raw.getUnshieldedBalances`
- `raw.getDustBalance`

```ts
import { formatBalance } from "@/lib/utils";
import type { BalanceState } from "@/utils/types";
import type { DAppConnectorWalletAPI } from "@midnight-ntwrk/dapp-connector-api";
import { useCallback, useState } from "react";

export type { BalanceState };

/**
 * ウォレット API から shielded / unshielded / dust 残高を並列取得する。
 *
 * Lace SDK の型定義には残高取得メソッドが含まれていないため、
 * unknown キャストで動的にメソッドの存在を確認してから呼び出す。
 * Promise.allSettled を使うことで、1 つが失敗しても残りの結果を受け取れる。
 */
async function fetchBalances(walletAPI: DAppConnectorWalletAPI): Promise<{
  shielded: string;
  unshielded: string;
  dust: string;
}> {
  const raw = walletAPI as unknown as Record<string, unknown>;

  // 並列で残高取得を試みる。存在しないメソッドは null を返す。
  const [shieldedResult, unshieldedResult, dustResult] =
    await Promise.allSettled([
      typeof raw.getShieldedBalances === "function"
        ? (raw.getShieldedBalances as () => Promise<unknown>)()
        : Promise.resolve(null),
      typeof raw.getUnshieldedBalances === "function"
        ? (raw.getUnshieldedBalances as () => Promise<unknown>)()
        : Promise.resolve(null),
      typeof raw.getDustBalance === "function"
        ? (raw.getDustBalance as () => Promise<unknown>)()
        : Promise.resolve(null),
    ]);

  return {
    shielded:
      shieldedResult.status === "fulfilled"
        ? formatBalance(shieldedResult.value)
        : "--",
    unshielded:
      unshieldedResult.status === "fulfilled"
        ? formatBalance(unshieldedResult.value)
        : "--",
    dust:
      dustResult.status === "fulfilled"
        ? formatBalance(dustResult.value)
        : "--",
  };
}

/**
 * 残高の取得・更新を管理するカスタムフック。
 *
 * @param walletAPI - 接続済みウォレット API。null の場合は何もしない
 * @returns balanceState: 現在の残高状態 / refresh: 手動更新トリガー関数
 */
export function useBalance(walletAPI: DAppConnectorWalletAPI | null) {
  const [balanceState, setBalanceState] = useState<BalanceState>({
    status: "idle",
  });

  /**
   * ウォレット API から残高を取得して状態を更新する関数。
   * walletAPI が null の場合は何もしない。
   * 取得中は status を "loading" に、成功したら "loaded" と残高をセット。
   * 失敗したら status を "error" にする。
   */
  const refresh = useCallback(async () => {
    if (!walletAPI) return;
    setBalanceState({ status: "loading" });
    try {
      const balances = await fetchBalances(walletAPI);
      setBalanceState({ status: "loaded", ...balances });
    } catch (e: unknown) {
      console.error("[useBalance] Failed to fetch balances:", e);
      setBalanceState({ status: "error" });
    }
  }, [walletAPI]);

  return { balanceState, refresh };
}
```

# アプリの動かし方

## クローン

```bash
git clone https://github.com/mashharuki/midnight-lace-react-sample-app.git

# フロントエンドアプリへのディレクトリに移動
cd app
```

## インストール

```bash
bun install
```

## ビルド

```bash
bun run build
```

## 起動

```bash
bun run dev
```

# まとめ

今回はここまでになります！

これで **React + Vite**で作成したアプリと**Lace Wallet**を接続させる実装方法が分かったのでフルスタックアプリケーション実装に向けて一歩前進しました！

次回は**Midnight**上にデプロイしたスマートコントラクトの機能を呼び出すところまで実装し、フルスタックアプリケーションの開発方法を解説した記事を執筆しようと思います！

ここまで読んでいただきありがとうございました！！

## 参考文献

- [Midnight公式サイト](https://www.midnight.network/)
- [Midnightドキュメント](https://docs.midnight.network/)
- [IOGが開発した新ライトウォレット”Lace”とは？](https://nagamaru-panda.blog/?p=828)