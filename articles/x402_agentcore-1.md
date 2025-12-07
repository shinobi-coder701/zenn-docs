---
title: "Amazon Bedrock AgentCoreとCDKとMastraとx402で構築する金融AIエージェント！"
emoji: "🤖"
type: "tech" 
topics: ["Mastra", "TypeScript", "AWS", "生成AI", "Web3"]
published: false
---

![](/images/x402_agentcore-1/0.jpeg)

# はじめに

みなさん、こんにちは！

実は今回紹介するAI Agentは先日開催された **AI Buidlers Day プレイベント**でお話しさせていただいたAI Agentと同じになります。

> イベントページ

https://jawsug.connpass.com/event/375739/

そこでは話しきれなかった細かい技術スタックの説明を解説していきますのでぜひ最後まで読んでいってください！！

> スライド

https://speakerdeck.com/mashharuki/amazon-bedrock-agentcore-x-aws-cdk-x-mastra-x-x402-deci-shi-dai-jin-rong-ai-agentwozuo-rou

> アーカイブ動画

https://www.youtube.com/watch?v=ZkcUtJVnwKI&themeRefresh=1

# この記事の対象読書

- x402について知りたい人
- x402 MCPサーバーの実装方法が知りたい人
- MastraをAgentCore上で動かす方法を知りたい人
- CDKでAgentCoreをデプロイしてみたい人
- AgentCore上にデプロイしたAI Agentをフロントエンドから呼び出す方法を知りたい人

# 今回作ったもの

<デモを挟む>

## システム構成図

## 技術スタック

- **AWS**
  - CDK
  - Amazon Bedrock AgentCore
  - ECS
    - Fargate
  - Lambda
  - ALB
- **Web3**
  - x402
  - Base Sepolia
  - solidity
  -  ERC20
  - Openzeppelin
  - USDC
- **AI Agent**
  - mastra
    - Next.js のサーバーコンポーネントの部分のみを利用(Honoとかの方がいいかも...)
  - MCP
- **フロントエンド**
  - Next.js

# 実装でポイントとなった箇所

## AgentCore上にデプロイするAI AgentのDockerfile

## Mastraの実装

## AgentCore上にデプロイしたAI Agentとフロントの繋ぎこみ

# 動かし方

## セットアップ

## コマンド

# まとめ

# 参考文献