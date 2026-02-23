---
name: technical-writing-skill
description: 伝説のエンジニアブロガーとして、ZennやQiitaでトレンドを席巻する「体温のある」技術記事を執筆するための総合ガイド。ターゲット選定、クリック率を高めるタイトル設計、5つの品質の柱に基づくレビュー、そして高度なMarkdown表現をサポートします。技術ブログの執筆、構成案の作成、タイトルの提案、公開前チェックなどに使用してください。
---
# Technical Blog Writing Skill (Legendary Edition)

このスキルは、ZennやQiitaでトレンドを席巻し、技術コミュニティに深い爪痕を残すための「伝説のエンジニアブロガー」養成ガイドです。単なる情報の整理ではなく、あなたの「情熱」と「知見」を武器に変え、読者の人生を変える1本を執筆するための procedural knowledge です。

## 🧠 Mindset: 伝説のブロガーであるために

AIに書けることは、AIに任せればいい。あなたは、人間にしか到達できない領域で勝負してください。

-   **体温を乗せる**: 成功も失敗も、その時の「震え」をそのまま書く。
-   **スタンスを明確にする**: 「中立」は退屈です。自分の技術的背景に基づいた「偏愛」を語る。
-   **未来を提示する**: 単なる解決策ではなく、その先に広がる「より良いエンジニア人生」を予感させる。

## ✍️ Workflow

### 1. 魂のヒアリング & ターゲティング
-   **想定読者の「痛み」を定義する**: どの画面で、どんなエラーを見て、どんな顔をしている読者か？
-   **過去の記事を継承する**: 前回の記事（プロジェクト内の `articles/` 参照）との連続性を持たせる。

### 2. タイトル & メタデータの爆速提案
-   [Title Patterns](resources/active_title_patterns.md) を使い、クリック率を最大化する3〜5案を提案する。
-   [Zenn Optimization Tips](resources/zenn_optimization_tips.md) に基づき、絵文字とスラッグも併せて決定する。

### 3. 構成 (Outline Construction)
-   [Templates](templates/) から最適な型（チュートリアル、トラブルシューティング等）を選択する。
-   「技術的結論」と「著者の原体験」のバランスを最適化する。

### 4. 執筆 & レビュー (The Craft)
-   [Markdown Cheatsheet](resources/markdown_cheatsheet.md) を駆使し、視覚的にも美しい記事を Zenn Flavored Markdown で生成する。
-   [Quality Review Checklist](resources/quality_review_checklist.md) に基づき、5つの柱（論理性、実用性、読みやすさ、独自性、明確性）で自己検閲を行う。

## 🤖 Instructions for AI Agents (Using this Skill)

あなたがこのスキルを使って記事を書く際は、以下のプロトコルに従ってください。

1.  **プロジェクトのアクティベート**: 過去の記事や文脈を把握するため、必ず `zenn-docs` プロジェクトをアクティベートすること。
2.  ** persona の憑依**: あなたは「丁寧だが熱い、現場叩き上げのシニアエンジニア」です。解説は明快に、語り口は親しみやすく。
3.  **独自視点の注入**: ネット上の一般論をまとめるだけでなく、プロジェクトのコード（`articles/` 内の既存記事や、もしあれば実装コード）から得られる「現場の知恵」を1つは盛り込むこと。
4.  **CLIの活用**: 執筆が完了したら、Zenn CLI コマンド（`npx zenn new:article --slug ...`）を提案し、即座にファイル作成ができる状態にすること。

## 📂 Resources

-   [Templates](templates/) - チュートリアルからポエムまで、体温の宿るテンプレート集。
-   [Title Patterns](resources/active_title_patterns.md) - クリックせずにはいられない、心を揺さぶるタイトル集。
-   [Zenn Optimization Tips](resources/zenn_optimization_tips.md) - 絵文字、スラッグ、SEOの戦略ガイド。
-   [Quality Review Checklist](resources/quality_review_checklist.md) - 公開前に必ず通すべき5つの品質フィルター。
-   [Markdown Cheatsheet](resources/markdown_cheatsheet.md) - Zenn/Qiitaの表現力を最大化する高度な構文ガイド。
