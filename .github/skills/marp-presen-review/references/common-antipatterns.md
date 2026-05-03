# Common Antipatterns & Fixes

## Table of Contents
1. [Content Antipatterns](#1-content-antipatterns)
2. [Structure Antipatterns](#2-structure-antipatterns)
3. [Visual Antipatterns](#3-visual-antipatterns)
4. [Typography Antipatterns](#4-typography-antipatterns)
5. [Technical Antipatterns](#5-technical-antipatterns)

---

## 1. Content Antipatterns

### AP-C1: Text Wall (Severity: HIGH)

A slide with 7+ bullets or paragraph-style text.

**Before:**
```markdown
## 現在の課題

- レガシーシステムの保守コストが年々増加している
- 技術的負債が蓄積し、新機能の追加に時間がかかっている
- エンジニアの採用が難しく、既存メンバーの負荷が高い
- セキュリティパッチの適用が遅れがちになっている
- ドキュメントが整備されておらず、属人化が進んでいる
- 他システムとの連携が困難で、データのサイロ化が起きている
- テスト自動化が進んでおらず、リリースサイクルが長い
- 監視体制が不十分で、障害検知が遅れることがある
```

**After (split into 2 slides + use cards):**
```markdown
## レガシーシステムが4つの深刻な問題を引き起こしている

<div class="columns">
<div class="card accent">

### コスト増大
**保守コストが年15%増加**し、新機能開発の予算を圧迫

</div>
<div class="card danger">

### セキュリティリスク
パッチ適用の遅延で**脆弱性の残存期間が平均60日**

</div>
</div>

---

## 開発生産性とチーム体制にも影響が波及

<div class="columns">
<div class="card warn">

### 開発速度の低下
技術的負債により**新機能リリースに平均3ヶ月**を要する

</div>
<div class="card accent">

### 属人化の進行
ドキュメント不足で**ナレッジが特定メンバーに集中**

</div>
</div>
```

### AP-C2: Vague Numbers (Severity: MEDIUM)

Using "大幅に", "大きく", "多くの" instead of specific data.

**Before:**
```markdown
- 売上が大幅に増加した
- 多くのユーザーが利用している
- コストを大きく削減できる
```

**After:**
```markdown
- **売上が前年比32%増加**（¥1.2B → ¥1.58B）
- **月間アクティブユーザー15万人**が利用
- **年間運用コストを¥24M削減**できる
```

### AP-C3: Placeholder Text (Severity: HIGH)

Text like "ここに説明", "TBD", "TODO", "xxx" in slides.

**Fix**: Replace every placeholder with real content or remove the slide.

### AP-C4: No Bold Key Phrases (Severity: HIGH)

Bullets without any bold emphasis — the audience cannot scan for key points.

**Before:**
```markdown
- クラウド移行により運用コストを30%削減
- 自動スケーリングでピーク時も安定稼働
- マネージドサービス活用で運用工数を半減
```

**After:**
```markdown
- クラウド移行により**運用コストを30%削減**
- 自動スケーリングで**ピーク時も安定稼働**
- マネージドサービス活用で**運用工数を半減**
```

### AP-C5: Missing So-What (Severity: HIGH)

Data or facts presented without interpretation or conclusion.

**Before:**
```markdown
## 売上データ

- Q1: ¥250M
- Q2: ¥280M
- Q3: ¥310M
- Q4: ¥340M
```

**After:**
```markdown
## 売上は4四半期連続で成長し年間目標を8%上回った

<div class="columns">
<div>

- Q1: ¥250M
- Q2: ¥280M（**前期比+12%**）
- Q3: ¥310M（**前期比+11%**）
- Q4: ¥340M（**前期比+10%**）

</div>
<div>

<div class="highlight">

年間合計 **¥1,180M** — 目標¥1,090Mに対し **108%達成**

</div>

</div>
</div>
```

---

## 2. Structure Antipatterns

### AP-S1: No Opening Hook (Severity: MEDIUM)

Presentation jumps straight to content without setting context or creating interest.

**Fix**: Add a problem statement, surprising statistic, or question as slide 2 (after title).

### AP-S2: Missing CTA (Severity: MEDIUM)

Presentation ends with "まとめ" but no clear call to action.

**Before:**
```markdown
## まとめ

- AIを活用した業務効率化の提案をしました
- コスト削減効果が見込めます
- 今後検討を進めていきたいです
```

**After:**
```markdown
## 次のステップ：2週間以内に3つのアクションを開始

<div class="steps">
<div class="step">

**PoC環境の構築** — 1/15までにAWS上にテスト環境を準備

</div>
<div class="step">

**パイロットチーム選定** — 営業部から5名のテストユーザーを選出

</div>
<div class="step">

**経営会議での正式承認** — 2/1の経営会議で予算申請

</div>
</div>
```

### AP-S3: Random Slide Order (Severity: HIGH)

Slides could be rearranged without losing coherence — no narrative flow.

**Fix**: Identify the presentation purpose, select a framework from `story-evaluation.md`, and reorder slides to match.

### AP-S4: Topic-Label Titles (Severity: MEDIUM)

Every title is a noun phrase ("背景", "課題", "提案") instead of a message.

**Fix**: Transform each title to an assertion. See the transformation table in `story-evaluation.md`.

---

## 3. Visual Antipatterns

### AP-V1: Bullet Monotony (Severity: HIGH)

4+ consecutive slides all using the same bullet-list format.

**Fix**: Replace at least every 3rd slide with an alternative visual:

| Slide Content | Better Visual |
|---------------|--------------|
| Comparison | `.columns` two-column layout |
| 3–4 items | `.card` grid (`.columns.col-3`) |
| Numbers/KPI | `.number` component |
| Process | `.steps` component |
| Key message | `.highlight` box or `lead` class |
| Features | `.icons` + `.icon-item` |

### AP-V2: No Section Breaks (Severity: LOW)

Long deck (10+ slides) without any `section` class slides to mark transitions.

**Fix**: Add `<!-- _class: section -->` slides between major topic groups.

### AP-V3: Cramped Layout (Severity: MEDIUM)

Content fills every inch of the slide with no breathing room.

**Fix**: Reduce bullets, increase margins, use layout components that inherently create whitespace.

---

## 4. Typography Antipatterns

### AP-T1: H1 Overuse (Severity: MEDIUM)

Using `# H1` on regular content slides (should be `## H2`).

**Rule**: `# H1` is reserved for title, lead, and ending slides ONLY.

### AP-T2: Multiple Bold Phrases Per Bullet (Severity: MEDIUM)

```markdown
- **クラウド移行**により**コスト削減**と**スケーラビリティ向上**を実現
```

**Fix**: Choose the ONE most important phrase:
```markdown
- クラウド移行により**コスト削減とスケーラビリティ向上**を実現
```

### AP-T3: No Heading on Content Slide (Severity: HIGH)

Content slide without `## H2` title — audience loses orientation.

**Fix**: Every content slide must have a `## H2` title that states the slide's message.

### AP-T4: Non-Parallel Bullets (Severity: LOW)

Bullets mix grammatical structures (nouns, verbs, questions).

**Before:**
```markdown
- コストの削減
- 開発スピードを上げる
- セキュリティは大丈夫？
- 運用の自動化
```

**After (all noun phrases):**
```markdown
- **コスト**の30%削減
- **開発スピード**の2倍向上
- **セキュリティ**の国際基準準拠
- **運用**の完全自動化
```

---

## 5. Technical Antipatterns

### AP-X1: Missing `html: true` (Severity: HIGH)

Using `<div>` layout components but `html: true` is not in frontmatter.
All HTML renders as literal text.

**Fix**: Add `html: true` to frontmatter.

### AP-X2: Unclosed Div Tags (Severity: HIGH)

```html
<div class="columns">
<div class="card">
Content here
</div>
<!-- Missing closing </div> for .columns -->
```

**Fix**: Ensure every `<div>` has a matching `</div>`. Count opening vs closing tags.

### AP-X3: No Embedded CSS (Severity: MEDIUM)

Frontmatter references `theme: excel` but CSS is not embedded in `style:` block.
File won't render correctly without external theme setup.

**Fix**: Embed the full excel-theme.css contents in the `style:` frontmatter block.

### AP-X4: Missing Slide Separator Spacing (Severity: LOW)

```markdown
Content here
---
Next slide
```

**Fix**: Add blank lines around `---`:
```markdown
Content here

---

Next slide
```

### AP-X5: Invalid Slide Class (Severity: MEDIUM)

Using `<!-- _class: highlight -->` or other non-existent classes.

**Valid classes**: `title`, `section`, `lead`, `dark`, `ending` (or no class for default).
