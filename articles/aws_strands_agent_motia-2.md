---
title: "Motia × Strands Agent SDKで作るAIエージェント開発入門2"
emoji: "🚀"
type: "tech"
topics: ["aws", "typescript", "AI", "StrandsAgent", "motia"]
published: false
---

## はじめに

こんにちは！

今回の記事は**Motia**と**Strands Agent SDK**を使ったAIエージェント開発をテーマに記事の第2回目の記事となります！

https://zenn.dev/mashharuki/articles/aws_strands_agent_motia-1

前回の記事でAPIサーバーとして動かすところまでは試したので今回はフロントエンドから呼び出してみる部分についてまとめている記事になります！

ぜひ最後まで読んでいってください！

# 今回試したソースコード

以下のGitHubリポジトリに格納してあります！

https://github.com/mashharuki/Motia-Strands-Agent-Sample

# APIで実装した機能とエンドポイント一覧

GET /tickets チケット一覧取得 (Node.js)
POST /tickets チケット新規作成 (Node.js)
POST /tickets/triage チケットトリアージ (Python)
POST /tickets/escalate チケットエスカレーション (Python)
POST /tickets/ai-assistant AIアシスタント呼び出し (Node.js)

# フロントエンドの解説

フロントエンドは**React.js**+**Vite**で実装しています！

基本的にはAPIを呼び出しているだけなので通常のバックエンドとのインテグレーションに近いイメージです。

## UI

UI構成はサイドバー + トップバー + メインコンテンツ + AIパネルという感じです！

![](/images/aws_strands_agent_motia-2/0.png)

ダッシュボード的な感じで今開いているチケットの一覧と状況を把握できるような見た目になっています！

![](/images/aws_strands_agent_motia-2/1.png)

![](/images/aws_strands_agent_motia-2/2.png)

![](/images/aws_strands_agent_motia-2/3.png)

![](/images/aws_strands_agent_motia-2/4.png)

AIアシスタント機能は右側のチャット欄にテキストを入力することで利用することが可能です！

ツールとしてチケットの一覧を取得する機能が実装してあるので今開いているチケットの状況を聞くことが可能です！

![](/images/aws_strands_agent_motia-2/5.png)


## ポイントとなる実装部分

# まとめ