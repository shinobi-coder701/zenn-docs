# Marp Slides — Layout Patterns

All layout components require `html: true` to be enabled (set via Marp CLI flag or VS Code setting).

---

## 1. Default Content Slide

```markdown
## スライドのタイトル

- **重要な点**はここに書く（1行 = 1アイデア）
- 補足説明は簡潔に、最大15単語以内
- `コード` や *注意点* もここで使える
- 最大5〜6点まで

> 引用や補足コメントはブロッククォートで
```

---

## 2. Two-Column Layout

```markdown
## 比較：Before / After

<div class="columns">
<div>

### Before
- 手動でのデータ集計
- 毎週 3時間 の作業
- ヒューマンエラーが多発

</div>
<div>

### After
- **自動化で即時集計**
- *作業時間ゼロ*
- エラー率 **95% 削減**

</div>
</div>
```

### Variants
```markdown
<!-- Asymmetric: text (wide) + image/stat (narrow) -->
<div class="columns col-6-4">
<div> ... text content ... </div>
<div> ... image or metric ... </div>
</div>

<!-- Three columns for options or steps -->
<div class="columns col-3">
<div> Option A </div>
<div> Option B </div>
<div> Option C </div>
</div>
```

---

## 3. Card Grid (categorized info)

```markdown
## 3つのアプローチ

<div class="columns col-3">
<div class="card accent">

### 🚀 高速
週次リリースを実現

</div>
<div class="card warn">

### ⚠️ 課題
移行コストが発生

</div>
<div class="card success">

### ✅ 推奨
段階的移行で低リスク

</div>
</div>
```

### Single-column cards (timeline / steps)
```markdown
<div class="card accent">**Phase 1** — 現状分析（1ヶ月）</div>
<div class="card warn">**Phase 2** — パイロット導入（2ヶ月）</div>
<div class="card success">**Phase 3** — 全社展開（3ヶ月）</div>
```

---

## 4. Metrics / KPI Slide

```markdown
<!-- _class: lead -->

## 成果サマリー

<div class="columns col-3" style="margin-top:24px">
<div style="text-align:center">
<span class="number">3×</span>

開発速度向上
</div>
<div style="text-align:center">
<span class="number warm">95%</span>

バグ検出率
</div>
<div style="text-align:center">
<span class="number">¥12M</span>

年間コスト削減
</div>
</div>
```

---

## 5. Highlight Box (key takeaway)

```markdown
## まとめ

- ポイントA
- ポイントB
- ポイントC

<div class="highlight">
💡 最重要メッセージをここに1文で
</div>
```

---

## 6. Step-by-Step Process

```markdown
## 実装ステップ

<div class="steps">
<div class="step">**要件定義** — ステークホルダーとスコープを合意</div>
<div class="step">**設計** — アーキテクチャとインターフェースを決定</div>
<div class="step">**実装** — スプリント方式で2週間単位で開発</div>
<div class="step">**テスト** — 自動テスト + UAT で品質保証</div>
<div class="step">**リリース** — ブルーグリーンデプロイで無停止移行</div>
</div>
```

---

## 7. Icon Row (feature overview)

```markdown
## 主要機能

<div class="icons">
<div class="icon-item">
<span class="icon">⚡</span>
<span class="label">高速処理</span>
</div>
<div class="icon-item">
<span class="icon">🔒</span>
<span class="label">セキュア</span>
</div>
<div class="icon-item">
<span class="icon">📊</span>
<span class="label">可視化</span>
</div>
<div class="icon-item">
<span class="icon">🔄</span>
<span class="label">自動化</span>
</div>
</div>
```

---

## 8. Code Showcase (dark slide)

```markdown
<!-- _class: dark -->

## 実装例：APIクライアント

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content)
```

> `model` に最新の Claude モデルを指定
```

---

## 9. Image + Text

```markdown
## 製品スクリーンショット

<div class="columns col-4-6 middle">
<div>

### 特徴
- **直感的なUI** で操作性 ↑
- *ダッシュボード* で一元管理
- モバイル対応

</div>
<div>

![画像の説明](./images/screenshot.png)

</div>
</div>
```

---

## 10. Table for Comparison

```markdown
## ツール比較

| 項目 | **本製品** | 競合A | 競合B |
|---|---|---|---|
| 処理速度 | **3× 高速** | 標準 | 低速 |
| コスト | **¥50K/月** | ¥80K/月 | ¥120K/月 |
| サポート | **24時間** | 営業時間内 | なし |
| API | **完全対応** | 一部対応 | 非対応 |
```

---

## 11. Progress / Roadmap

```markdown
## Q1 進捗状況

**フェーズ1 — 基盤構築**
<div class="progress"><div class="progress-bar" style="width:100%"></div></div>

**フェーズ2 — パイロット**
<div class="progress"><div class="progress-bar" style="width:65%"></div></div>

**フェーズ3 — 展開**
<div class="progress"><div class="progress-bar" style="width:10%"></div></div>
```

---

## 12. Tags / Labels

```markdown
## 対応スタック

<span class="tag">Python</span>
<span class="tag">FastAPI</span>
<span class="tag warm">PostgreSQL</span>
<span class="tag success">Docker</span>
<span class="tag outline">Kubernetes</span>
```

---

## Full Slide Structure Reference

```markdown
---
marp: true
theme: excel
paginate: true
size: 16:9
html: true
style: |
  /* Paste contents of excel-theme.css here */
---

<!-- _class: title -->

# プレゼンテーションタイトル
## サブタイトルや発表者名

2026-03-03 · Your Name

---

## アジェンダ

1. 背景と課題
2. 提案内容
3. 期待効果
4. 実装計画
5. まとめ

---

<!-- _class: section -->

## 01 背景と課題

現状の問題点を整理する

---

## 現状の課題

...

---

<!-- _class: ending -->

# ありがとうございました

## Your Name · your@email.com

https://your-site.example
```

---

## Marp Directive Quick Reference

```markdown
<!-- Global (in frontmatter) -->
marp: true
theme: excel
paginate: true
size: 16:9         # or 4:3, A4
html: true
header: "Company Name"
footer: "Confidential"

<!-- Per-slide (as HTML comments) -->
<!-- _class: title -->
<!-- _class: section -->
<!-- _class: lead -->
<!-- _class: dark -->
<!-- _class: ending -->
<!-- _paginate: false -->    # hide page number on this slide
<!-- _header: "" -->         # override header for this slide
<!-- _backgroundColor: #f0f0f0 -->
<!-- _color: #333 -->
```
