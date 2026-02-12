---
title: "圧倒的な高速取引を実現するYellowProtocolについて調べてみた！"
emoji: "🌻"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["Web3","Ethereum","Typescript","ERC","blockchain"]
published: false
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