---
title: "AWS Summit AI-DLCハッカソンを戦い抜くために工夫したこと"
emoji: "🤖"
type: "tech"
topics: ["aws","ai","ハッカソン","lean","スペック駆動開発"]
published: true
---

# はじめに

皆さん、こんにちは！

先日**AWS Summit Japan2026**に合わせて開催された**AWS Summit Japan 2026 AI-DLC ハッカソン**に参加してきました。

今回のハッカソンは**AI-DLC**に沿って**人をダメにするサービスを作る**という非常に難しいお題が提示されたものでした！

https://pages.awscloud.com/summit-japan-2026-hackathon-reg.html

エントリー数は117チームとかなりの激戦となりましたが、最終的に3位に入賞することができました！

https://x.com/haruki_web3/status/2070433400918553035

## プロダクトのGitHub

https://github.com/mashharuki/AWS-SummitHackathon-2026

今回の技術ブログでは、ハッカソンで戦い抜くために**AI-DLC**をどのように使いとして恩恵を最大限享受するために工夫したことを共有させていただきます！

# AI-DLCって何？

## AI-DLCの概要

**AI-DLC**は、AWS が提唱する AI 時代の新しい開発手法 **AI-DLC（AI-Driven Development Lifecycle）** のことで、AIが実行し人間が監督するという役割分担でソフトウェア開発全体を再構築するAI時代の新しい開発手法というものです。

詳細は以下の記事やGitHubにも掲載されていますのでここでは簡単に概要だけまとめさせていただきます。

https://zenn.dev/aws_japan/articles/aidlc-workflows

https://github.com/awslabs/aidlc-workflows/tree/main

AI-DLCのワークフローは大きく3ステップに分かれます。

- **要件定義・設計にあたるInceptionフェーズ**
- **実装にあたるConstructionフェーズ**
- **運用にあたるOperationフェーズ**

## cc-sddとかと何が違う？

スペック駆動開発を実践する上で他に有名なものとして**cc-sdd**もあると思います。

https://github.com/gotalab/cc-sdd

大まかな流れはcc-sddとAI-DLCでは同じです。

要件定義→設計→実装 という流れはほぼ同じで細かい部分が異なっています。

そして実際に使い込んでみて**AI-DLC**はエンタープライズ企業での実務利用をかなり意識して設計されていると感じました。

AIに指示した内容やその結果生成された出力内容のサマリーが audit.md というファイルに事細かにまとめられていきます。

https://github.com/mashharuki/AWS-SummitHackathon-2026/blob/main/aidlc-docs/audit.md

こうすることで過去に遡り誰がどのタイミングでどのような考えの元AIと協調してプロダクトを開発したかということが振り返られるようになっている点が非常に魅力的だと思います。

このaudit.mdはcc-sddにはない部分です。それにInceptionフェーズで生成される要件定義・設計にあたるドキュメントの生成量もcc-sddと比較して非常に充実していると感じました。

https://github.com/mashharuki/AWS-SummitHackathon-2026/tree/main/aidlc-docs

さらにもう一つ違うのがOperationフェーズで、作ったプロダクトのデプロイメントまでケアしてくれるドキュメントを生成してくれるというものです。

例えばAWS CDKを使ってプロダクト用のCDKスタックとそのセットアップ手順・デプロイコマンドまで丁寧にまとめてくれます。

https://github.com/mashharuki/AWS-SummitHackathon-2026/blob/main/aidlc-docs/operations/deploy-e2e-verification.md

cc-sddで同じようなこともできますが、その際は明示的に指示する必要が出てきます。

# AI-DLCハッカソンで工夫したこと

AI-DLCの標準機能は上述した通りの内容です。

ここからはハッカソンで実践した工夫をまとめていきます！

## 要件定義のドキュメントの質とゴールイメージのすり合わせが重要

まず僕たちのチームで実践した工夫はInceptionフェーズを何度も何度も回してチームメンバー間でゴールイメージをすり合わせしたことです。

cc-sddと違い、要件定義・設計段階に生成されるドキュメントが豊富で読み合わせしやすいという点もAI-DLCの特徴だと思いました。

1次選考にすすむまでに4,5回以上は作って→見直して→アップデートしてを繰り返してゴールに向けてのドキュメントの質を徹底的に高めました！

### AI-DLC用のサブエージェントとSKILLを作成

AI-DLCを実践するにサブエージェントとSKILLを事前に作成して回してみました。

https://github.com/mashharuki/AWS-SummitHackathon-2026/blob/main/.claude/agents/aidlc-specialist.md

https://github.com/mashharuki/AWS-SummitHackathon-2026/tree/main/.claude/skills/aidlc-workflow-guide

また、今回のハッカソンの開催概要や審査基準などまとめた専用のレビュー用SKILLとハッカソン向けにプロダクトを最適化させる戦略SKILLも作成してInceptionフェーズでの成果物の質を高めるように工夫してみました！

https://github.com/mashharuki/AWS-SummitHackathon-2026/tree/main/.claude/skills/aws-summit-hackathon-reviewer

https://github.com/mashharuki/AWS-SummitHackathon-2026/tree/main/.claude/skills/hackathon-strategist

## 環境セットアップは大事！

2つ目に工夫したことは、事前の環境セットアップを人間の手で実施したことです！

具体的にはpnpmものレポプロジェクトのセットアップ、フロントエンド、バックエンド、CDK用のプロジェクトそれぞれの最低限のプロジェクトのベース部分を事前に実装してからAI-DLCの実装フェーズを回しました。

環境構築はAIにとってものすごく負荷のかかる部分なのでそこはこちら側(人間側)で担当して、AIにはロジック設計や実装に集中してもらいました！

そして採用予定の技術スタックのAgent SKILLは徹底的に整備し、サブエージェントも拡充してから実装に移りました！

MCPの数も最小限にして、 **AWS MCP Server**、**Serena MCP**、**CodeGraph MCP**を重点的に使うようにしました！

https://github.com/mashharuki/AWS-SummitHackathon-2026/blob/main/.claude/.mcp.json

結果、このように整備したおかげで多忙の中でも確実にゴールに向かってプロダクトを開発することができました！！

## Leanを使ってプログラムの安全性を数学的に担保

そして最後に工夫したこととして、実装予定のロジックの安全性を数学的に担保するために**Leanによる形式検証のフェーズ**をAI-DLCに取り込んだことです！

https://github.com/leanprover/lean4

Leanはいくつかある形式検証を実現させるためのアプローチのうち**定理証明**を行うために開発されたプログラミング言語になります！

普通のテスト駆動開発はAI-DLCも含めてスペック駆動開発と合わせて実践されている方が多いと思います。

僕たちはもう一歩踏み込んでそこに形式検証のチェックを組み込みました。

テストと異なり、数式でバグがないことを証明するため網羅的にチェックすることが可能な点が形式検証の特徴です。

実際にソースコード監査会社ではこの形式検証を用いている企業があります！

https://www.certik.com/

自分たちのプロダクトではSlack内のチャット履歴、アカウント名、メールアドレスなどプライバシーに関する重要な情報を取り扱う設計になっていたため、それらの情報を保護する暗号ロジックを実装する予定でした。

しかし、特定の条件で暗号化に用いるハッシュ関数の出力値が一致してしまうという潜在的なバグがあったのですがそれをこの**Leanを用いた形式検証で事前に発見しました**。

形式検証のフェーズを取り入れることで**AI-DLC**がより強固な開発手法になったと思います！

もちろん、形式検証やLeanについても事前に徹底的にリサーチしてサブエージェントとSKILLを用意しました！

https://github.com/mashharuki/AWS-SummitHackathon-2026/tree/main/.agents/skills/lean-formal-verification/agents

https://github.com/mashharuki/AWS-SummitHackathon-2026/blob/main/.agents/skills/lean-formal-verification/SKILL.md

# まとめ

以上が**AI-DLCハッカソンで戦い抜くために工夫したこと**です！

cc-sddやplanモード、`/goal`コマンドなどAIを使って目的を達成するために様々な手法がありますが、**AI-DLCは特にエンタープライズの実務での活用を意識して提唱されたもの**だと思います。

ハッカソンで使い倒してみたので今後は実務の中でも利用を積極的に検討していこうと思います！

# 最後に

一緒に戦ってくれたチームメンバー、メンタリングしていただいたカトリョーさん、そしてハッカソン事務局の皆さんには本当に大変お世話になりました。

AWS Summit Japanという大舞台でピッチして壇上に上がる機会をいただけたことに心から感謝いたします。

そしてこれからもAI-DLCと共にチャレンジし続けていきます！
