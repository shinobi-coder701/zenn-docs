---
title: "UniswapV4に対応したオリジナルHookを作ってみよう！"
emoji: "🦄"
type: "tech"
topics: ["Web3","blockchain","DEX","solidity","Ethereum"]
published: false
---

# はじめに

先日 **ETH Global**が主催する**HackMoney2026**に参加する機会があり**UniswapV4**を使ったHookを開発する機会がありました。

https://ethglobal.com/events/hackmoney2026

調べる中で色々と分かったことがあるので学びをシェアするために記事を書きました。

ぜひ最後まで読んでいってください！

# Uniswapとは

# DEXとは

# UniswapV4でできるようになったこと

# UniswapV4に対応したオリジナルHookを作ってみよう！

## サンプルコード

https://github.com/mashharuki/defi-uniswap-v4

## 動かし方

### Devcontainerを立ち上げる

まずはDevcontainerを起動させましょう！

### インストール

git submoduleを使っているのでリポジトリをクローンしてきたら以下のコマンドを実行します。

```bash
git submodule update --init --recursive
```

以降のコマンドは`foundry`フォルダ配下で実行します。

### ビルド

```bash
forge build
```

### 事前準備

- Alchemy等のRPCプロバイダーでEthereumメインネット用のAPIキーを発行すること
- 上記値を環境変数にセットする。
    ```bash
    FORK_URL=
    ```

    そして環境変数有効化させます

    ```bash
    source .env
    ```
- 次に以下のコマンドで最新ブロック高を取得する
    ```bash
    FORK_BLOCK_NUM=$(cast block-number --rpc-url $FORK_URL)
    echo $FORK_BLOCK_NUM
    ```
- 次に以下のコマンドでSaltを発行する
    ```bash
    forge test --match-path test/FindHookSalt.test.sol -vvv
    ```

    ここで得られたSALTを環境変数にセットする

    ```bash
    SALT=
    ```

    そして再度有効化させます。

    ```bash
    source .env
    ```

    これで準備OKです！

### テスト

それではテストしてみましょう！

```bash
forge test
```

以下のように1機能ずつテストしていく

#### CounterHook

```bash
forge test --fork-url $FORK_URL --fork-block-number $FORK_BLOCK_NUM --match-path test/CounterHook.test.sol -vvv
# 回答の方を実行する場合は FOUNDRY_PROFILE=solutionをつける
FOUNDRY_PROFILE=solution forge test --fork-url $FORK_URL --fork-block-number $FORK_BLOCK_NUM --match-path test/CounterHook.test.sol -vvv
```

テスト実行結果例

```bash
Suite result: ok. 3 passed; 0 failed; 0 skipped; finished in 44.85s (42.33s CPU time)

Ran 1 test suite in 50.55s (44.85s CPU time): 3 tests passed, 0 failed, 0 skipped (3 total tests)
```

#### フラッシュローン

```bash
forge test --fork-url $FORK_URL --fork-block-number $FORK_BLOCK_NUM --match-path test/Flash.test.sol -vvv
```

```bash
Logs:
  Borrowed amount: 1e9 USDC

Suite result: ok. 1 passed; 0 failed; 0 skipped; finished in 1.10s (101.25ms CPU time)
```

# まとめ

以上 UniswapV4についての解説記事になります！

Swapする前後や流動性の追加・削除に伴ってカスタムロジックを呼び出せることでuniswapの仕組みを応用したアプリが開発しやすくなっていました。

皆さんもぜひお試しあれ！

ここまで読んでいただきありがとうございました！

# 参考文献