---
title: "Aleph Zeroを学ぼう！！"
emoji: "✨"
type: "tech" 
topics: ["Web3","Blockchain","ゼロ知識証明","EVM","WASM"]
published: true
---

![](/images/alpha_zero_1/0.jpeg)

## はじめに

皆さん、こんにちは。

今回は、**Aleph Zero** というブロックチェーンをテーマにした記事を執筆していこうと思います！

現在ハッカソンプラットフォーム**Akindo**と**Aleph Zero**のチームがタッグ組んでWaveHackというプログラムを実施中です！

https://app.akindo.io/wave-hacks/RDOqoON4ZSvJjW71

**WaveHack** ってなんだという方は以下の記事をご参照ください！

ファウンダーである金城さんの想いがまとめられています！！！

https://note.com/shinkinjo/n/n313d1e931ebf

---

## Aleph Zeroとは

では早速 Aleph Zeroについてまとめていきたいと思います！

### 概要

Aleph Zeroは、WASMベースのL1とEVM互換のL2を持ち、高速でスケーラブルなブロックチェーンです。

![](/images/alpha_zero_1/A0_logotype_horizontal_graphite.png)

独自のピアレビュー済みコンセンサスプロトコルに基づいて構築されています。**Substrateスタックと統合し**、従来の分散型台帳技術の課題であるスピード、検証時間、スケーラビリティ、セキュリティの問題を解決しています。

Substrateを使っている点は、 **Astar Network(L1の方)と同じですね！**

Aleph Zeroのユニークな特徴として以下の2点が挙げられます。

- サブセカンドのトランザクション処理が可能なこと。
- ZKプライバシー証明が可能なこと。

### 主な機能

- #### zkOS
  zkOSはZKプライバシーシステムで、サブセカンドでの証明時間を達成することが可能です。
  　
  WASMおよびEVM互換のネットワークで、アプリケーションにシームレスに統合できるPrivacy-as-a-Service（PaaS）を提供します。

- #### zkToolkit
  zkToolkitは、Aleph Zeroチームによって開発されたツールセットで、既存のアプリにzkOSプライバシーレイヤーを簡単に統合できるよう支援します。

- #### Aleph Zero EVM L2
  Aleph ZeroのEVMは、EVM互換のLayer 2ブロックチェーンです。
  　
  Arbitrum Orbitスタックに基づき、250msのオンデマンドブロックタイムを持ち、幅広い業界の互換性を実現しています。
  　
  エンドポイントなどは以下で確認ができます！
  https://docs.alephzero.org/aleph-zero/build/development-on-evm-layer
  　
  テストネット用のファウセットは以下で入手できるようです。
  https://drpc.org/faucet/alephzero

- #### Aleph Zero WASM L1
  Aleph Zero WASM L1は、RustのeDSLである **ink!** を利用し、WASMにコンパイルされるLayer 1スマートコントラクトパレットです。

  **1nk!** は、Astar NetworkでWASM用のスマートコントラクトを開発する時にも利用されるプログラミング言語です。
  　
  サブセカンドのファイナリティを特徴とし、約170のバリデータノードが稼働しています。

- #### AlephBFT
  AlephBFTは、2019年のAdvances in Financial Technologies（AFT）会議で発表されたピアレビュー済みのコンセンサスアルゴリズムです。**Proof of Stake（PoS）と有向非巡回グラフ（DAG）** を組み合わせた手法を採用しています。これにより、高速な取引処理、低コスト、優れたスケーラビリティを実現しています。

- #### Aleph Zero Data Availability Layer
  Aleph Zeroの低コストなストレージ手数料と高いスループットを活用し、他のチェーンがデータを保存するためのレイヤーとして利用できます。

  DAG（Directed Acyclic Graph）技術を利用し、高速で分散型の効率的なシステムを実現しています。 あの**Sui Network**もDAGを使って高速なスループットを実現させています。
  　
  これにより、低コストで高速なトランザクション処理が可能になります。

- #### MOST
  MOSTは、Aleph ZeroとEthereum、Aleph Zero WASM L1、Aleph Zero EVM L2間のネイティブブリッジングソリューションです。   
  　
  EthereumからAleph ZeroエコシステムにETHやステーブルコインなどのトークンをブリッジする際に、手数料が軽減されます。

### Aleph Zeroが提供する価値

Aleph Zeroは、Web3エコシステムが必要とする以下の3点を課題を解決することを目指しています。

- #### パフォーマンス
  Aleph Zeroは、プライバシー保護されたアプリケーションやそうでないアプリのどちらにも高速な処理を提供します。
  　
  多くのブロックチェーンがネットワークの速度問題を解決していますが、Aleph Zeroはその中でも特に高速で、スムーズなユーザー体験を提供します。

- #### プライバシー
  現在、オンチェーンプライバシーはWeb3において広く採用されていません。
  　
  その主な理由は、既存のプライバシーソリューションが複雑すぎ、Web3エコシステムと統合されていないことにあります。
  　
  Aleph Zeroでは、簡単で高速なプライバシー対応アプリケーションを提供し、より多くのユーザーがこれを活用できるようにします。

- #### セキュリティ
  Aleph Zeroは、複数のセキュリティ層を提供します。
  　
  個人のセキュリティを高めるプライバシー保護、企業データの機密性を保つためのツールが搭載されています。これにより、エンタープライズレベルのセキュリティも実現します。

### AZEROコインのユースケース

Aleph Zeroのネイティブトークンである**AZERO**は、以下のような場面で使われます。

- #### バリデータノードのステーキング
  ネットワークをセキュリティ面で強化するためにAZEROがステーキングされます。
- #### 分散型取引所（DEX）のスワップ手数料
  Aleph Zero内のDEXでの取引手数料として使用されます。
- #### Aleph Zero WASMの手数料
  WASMベースのスマートコントラクトを実行する際の手数料として使われます。
- #### Aleph Zero EVMの手数料
  EVM互換の環境での手数料として使用されます。
- #### zkOSプライバシー操作のガストークン
  プライバシー保護のためのzkOS操作においてガスとして機能します。
- #### ガバナンスの投票プロセス
  エコシステム内でのガバナンス投票にも使用されます。

**AZERO**の供給状況は以下の通りとなっています

- **現在の循環供給量：302,136,160**
- **総供給量：374,361,335**
- **最大供給量：520,000,000**
- **ステーキングされている割合：63.6%**

### AZEROを取り扱っている取引所

公式サイトによると以下の取引所が対応しているみたいです。

![](/images/alpha_zero_1/1.png)

### Aleph Zero対応ウォレット

こちらも公式サイトからの引用です。  
有名どころのウォレットも対応していますね。

![](/images/alpha_zero_1/2.png)

### Aleph Zeroのエコシステム

Aleph Zeroは注目されているだけあってすでに様々なアプリケーションとも連携しています。

- #### Dapp
  - ArtZero
  - AZERO Punks
  - CLST
  - PanoramaSwap

- #### インテグレーション系
  - Gatenox
  - Subscan
  - SupraOracles

- #### パートナー
  - 10Clouds
  - AngelBlock
  - Cardinal Cryptography
  - Crypto Climate Accord
  - Flidy Technologies
  - P-OPS
  - UBIK Capital

Aleph Zeroのエコシステムについてもっと詳しく知りたいという場合は以下のサイトを参照することをおすすめします！

https://alephzero.org/ecosystem

### 規制準拠について

Aleph Zeroは、スイスの金融市場監督局（FINMA）から「No-actionレター」を取得しており、AZEROコインの発行がスイスの法律に準拠していることが確認されています。

---

## まとめ

いかがでしたでしょうか？

**Aleph Zero**をよく分かっていなかったので自分の学習したことを復習する意味でも記事を執筆してみました。

Astar Network(L1)とSuiのいいとこどりをしてゼロ知識証明をフル活用しているブロックチェーンといったイメージです。

やっぱり**Rust**系のプログラミング言語が書けないと色々キツくなってきたので本気で勉強しにいかないといけなそうですね。

今回はここまでになります。

ここまで読んでいただきありがとうございました！！

---

## さらにAleph Zeroについて場合

YouTubeや公式サイトが参考になります！！

https://alephzero.org/

https://www.youtube.com/@AlephZero

最新情報をキャッチアップしたい場合は、Xのアカウントをフォローすると良さそうです！

https://x.com/Aleph__Zero

Discordもあるみたいです！

https://discord.gg/alephzero

---

### 参考文献
1. [Aleph Zero 公式サイト](https://alephzero.org/)
2. [Aleph Zero Youtubeチャンネル](https://www.youtube.com/@AlephZero)
3. [Aleph Zeroとは？ - プライバシー強化ブロックチェーンの新時代とDeutsche Telekomとの協力](https://note.com/panda_lab/n/ne7984bb7e95a)
4. [アレフゼロ（AZERO）への投資 – 知っておくべきことすべて](https://www.securities.io/ja/investing-in-aleph-zero/)
5. [Aleph Zero 開発者ドキュメント](https://docs.alephzero.org/aleph-zero)
6. [ホワイトペーパー集](https://docs.alephzero.org/aleph-zero/explore/audit-and-research-papers)
7. [テストネット用Faucetサイト](https://drpc.org/faucet/alephzero)