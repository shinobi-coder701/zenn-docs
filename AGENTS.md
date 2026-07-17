# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## リポジトリ概要

Zenn（zenn.dev）と連携した技術ブログ記事のリポジトリ。コードベースではなくコンテンツ（Markdown 記事）が主体で、`main` ブランチへの push が Zenn への公開に直結する。

## コマンド

```bash
npm i                                # zenn-cli のインストール
npx zenn new:article --slug スラッグ --title タイトル --type tech --emoji 🛠   # 新規記事作成
npx zenn new:book                    # 新規本作成
npx zenn preview                     # ローカルプレビュー（記事の表示確認）
```

ビルド・lint・テストは存在しない。検証はプレビューでの目視確認。

## ディレクトリ構成と規約

- `articles/` — 日本語の Zenn 記事（本体）。フロントマターは Zenn 形式：`title` / `emoji` / `type: "tech"` / `topics`（配列）/ `published`（true で公開）。下書きは `published: false` で作成する。
- `en/` — 英語版と Dev.to 版。命名は `<元スラッグ>-en.md`（英語翻訳）、`<元スラッグ>-devto.md`（Dev.to 投稿用。変換には devto-optimizer-skill を使う）。
- `images/<記事スラッグ>/` — 記事ごとの画像ディレクトリ。記事内からは `/images/<記事スラッグ>/xxx.png` の絶対パスで参照する。
- `slides/` — Marp 形式の登壇スライド。生成要件（Front Matter、16:9、サイバーパンク調テーマ等）は `AGENTS.md` に定義されている。
- `memo/`, `prompts/`, `data/` — 下書きメモ・プロンプト・素材置き場。公開対象ではない。

## 執筆ワークフロー

このリポジトリには記事執筆用の Subagent と Skill が整備されており、積極的に使うことがプロジェクトルール（`.claude/rules/proactive-subagents-and-skills.md`）で定められている。

- 記事の新規執筆・構成案・タイトル提案・リライト → `tech-blog-writer` エージェント（`technical-writing-skill` を適用）
- 記事のレビュー・品質採点・AI 臭チェック → `tech-blog-reviewer` エージェント（`tech-blog-reviewer-skill` を適用）
- AI っぽい文体の除去 → `ai-smell-remover` スキル
- Dev.to への転載用変換（ZFM → Forem Markdown）→ `devto-optimizer-skill`
- スライド作成・レビュー → `marp-slides` / `marp-presen-review` スキル（要件は `AGENTS.md` 参照）

記事は日本語で執筆する（`en/` 配下の英訳・Dev.to 版を除く）。

## 注意点

- `.github/rules/`・`.github/skills/` は `.claude/` 配下と同内容のミラー。ルールやスキルを更新する場合は両方を同期させる。
- `published: true` にした記事は push 時点で公開されるため、公開可否は必ずユーザーに確認する。
