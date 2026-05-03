# Layout & Component Anti-Patterns

均等・反復・テンプレート的なレイアウトを避け、
文脈に応じた意図あるレイアウトを設計するためのパターン集。

---

## 目次

1. [レイアウトのアンチパターンと代替](#レイアウトのアンチパターンと代替)
2. [セクション構成の代替パターン](#セクション構成の代替パターン)
3. [コンポーネントのアンチパターンと代替](#コンポーネントのアンチパターンと代替)
4. [余白リズムの設計](#余白リズムの設計)
5. [グリッド破壊テクニック](#グリッド破壊テクニック)

---

## レイアウトのアンチパターンと代替

### 1. 均等3列カードグリッド

**AI スロップ:**
```html
<div class="grid grid-cols-3 gap-6">
  <div class="card">同じ構造</div>
  <div class="card">同じ構造</div>
  <div class="card">同じ構造</div>
</div>
```

**代替 A: 非対称グリッド（2:1 比率）**
```html
<div class="grid grid-cols-3 gap-6">
  <div class="col-span-2">メインコンテンツ（大きく）</div>
  <div>サブコンテンツ</div>
</div>
```

**代替 B: サイズ混在グリッド**
```html
<div class="grid grid-cols-4 gap-4">
  <div class="col-span-2 row-span-2">フィーチャー（大）</div>
  <div>項目A</div>
  <div>項目B</div>
  <div class="col-span-2">項目C（横長）</div>
</div>
```

**代替 C: リスト形式**
```html
<div class="space-y-4">
  <div class="flex items-center gap-6 border-b pb-4">横並びリスト項目</div>
  <div class="flex items-center gap-6 border-b pb-4">横並びリスト項目</div>
</div>
```

### 2. Hero → Features → Testimonials → CTA 定型構成

**代替構成パターン:**

| パターン名 | 構成 | 適するケース |
|-----------|------|-------------|
| **ストーリーテリング** | Problem → Solution → How It Works → Evidence → Action | プロダクトLP |
| **マガジンレイアウト** | Large Visual → Text Block → Grid → Quote → Visual | ブランドサイト |
| **データファースト** | Key Metric → Explanation → Details → Action | B2B/SaaS |
| **逆ピラミッド** | 結論(CTA) → 根拠 → 詳細 → 補足 | コンバージョン重視 |
| **ジグザグ** | 左画像/右テキスト → 右画像/左テキスト → ... | 機能紹介 |

### 3. 全カード同一 `rounded-2xl shadow-lg`

**代替:**
- カードの重要度に応じてシャドウの深さを変える
- 一部はボーダーのみ、一部はシャドウ、一部は背景色差で区別
- カード枠なし + 余白のみで区切る
- 角丸を混在させる（`rounded-sm` と `rounded-xl` の対比）

---

## セクション構成の代替パターン

### パターン 1: Bento Grid（ベントーグリッド）

```
┌──────────────┬─────┐
│              │     │
│   Feature A  │  B  │
│   (Large)    │     │
├─────┬────────┼─────┤
│  C  │   D    │  E  │
│     │        │     │
└─────┴────────┴─────┘
```

```css
.bento {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 1rem;
}
.bento > :first-child { grid-column: 1 / 3; }
```

### パターン 2: Overlap（重なり）

```
┌───────────────────┐
│   Background      │
│   Section         │
│        ┌──────────┴───┐
│        │  Overlapping  │
└────────┤  Card         │
         └──────────────┘
```

```css
.overlap-section { position: relative; padding-bottom: 4rem; }
.overlap-card {
  position: relative;
  margin-top: -3rem;
  margin-inline: 2rem;
}
```

### パターン 3: Split Screen（分割画面）

```
┌────────────┬────────────┐
│            │            │
│   Text     │   Visual   │
│   Content  │            │
│            │            │
└────────────┴────────────┘
```

テキストと画像を50/50で分割。一方をスティッキーにすることで、スクロール時の視覚的緊張を作る。

### パターン 4: Single Column + Pull Quote

```
┌──────────────────────────┐
│         Narrow text      │
│         column           │
│                          │
│  ┌─────────────────────┐ │
│  │  PULL QUOTE (wider) │ │
│  └─────────────────────┘ │
│                          │
│         Narrow text      │
│         continues        │
└──────────────────────────┘
```

本文は `max-width: 65ch` で狭く、引用や強調だけ幅を広げる。

### パターン 5: Asymmetric Sidebar

```
┌──────┬──────────────────┐
│      │                  │
│ Nav  │    Main Content  │
│ 200px│    (fluid)       │
│      │                  │
│      ├─────────┬────────┤
│      │  Card A │ Card B │
│      │  60%    │ 40%    │
└──────┴─────────┴────────┘
```

サイドバーは固定幅、メインコンテンツ内のグリッドも非対称。

---

## コンポーネントのアンチパターンと代替

### Feature Card（アイコン + タイトル + テキスト）

**AI スロップ:**
```html
<div class="text-center p-6 rounded-2xl shadow-lg">
  <div class="text-4xl mb-4">🚀</div>
  <h3 class="text-xl font-bold mb-2">Feature Name</h3>
  <p class="text-gray-600">Description text here...</p>
</div>
```

**代替 A: 横並び + ボーダーアクセント**
```html
<div class="flex gap-4 border-l-4 border-primary pl-4">
  <div>
    <h3 class="font-semibold">Feature Name</h3>
    <p class="text-text-muted mt-1">Description</p>
  </div>
</div>
```

**代替 B: 番号付きリスト**
```html
<div class="flex gap-6">
  <span class="text-5xl font-heading font-light text-accent">01</span>
  <div>
    <h3 class="font-semibold">Feature Name</h3>
    <p class="text-text-muted mt-2">Description</p>
  </div>
</div>
```

**代替 C: 画像/図解ベース**
カードの代わりに、各機能を図解やスクリーンショットで示し、テキストは最小限に。

### CTA ボタン

**AI スロップ:**
```html
<button class="bg-gradient-to-r from-purple-500 to-blue-500 text-white px-8 py-4 rounded-full text-lg font-bold">
  Get Started Now →
</button>
```

**代替 A: 控えめだが明確**
```html
<button class="bg-primary text-text-inverse px-6 py-3 rounded font-medium tracking-wide">
  Get Started
</button>
```

**代替 B: テキストリンク風**
```html
<a class="inline-flex items-center gap-2 text-primary font-semibold border-b-2 border-primary pb-1 hover:gap-3 transition-all">
  Get Started <span aria-hidden="true">→</span>
</a>
```

**代替 C: アウトラインボタン**
```html
<button class="border-2 border-primary text-primary px-6 py-3 rounded hover:bg-primary hover:text-text-inverse transition-colors">
  Get Started
</button>
```

### Hero セクション

**AI スロップ:** 中央揃え大見出し + サブテキスト + グラデーション背景 + 2つのCTAボタン

**代替パターン:**
- 左寄せテキスト + 右に大きなビジュアル（Split Hero）
- テキストのみ、フォントサイズとウェイトの対比で魅せる（Type-driven Hero）
- フルブリード画像 + テキストオーバーレイ（Visual-first Hero）
- 小さな見出し + 大きなインタラクティブ要素（Demo-first Hero）

---

## 余白リズムの設計

全セクション同一パディングは NG。コンテンツの重要度と文脈で変える。

### リズムの基本

CSS Custom Property で base unit を定義:
```css
:root {
  --space-unit: 1rem; /* 16px */
}
```

セクション間の余白をリズミカルに変化させる:

| セクション遷移 | 余白 | 理由 |
|-------------|------|------|
| Hero → 次セクション | `8 * var(--space-unit)` | ブレス。Heroの余韻 |
| 同系統セクション間 | `4 * var(--space-unit)` | 連続性を示す |
| 話題転換 | `6 * var(--space-unit)` | 明確な区切り |
| フッター前 | `10 * var(--space-unit)` | 終結感 |

### セクション内の余白

```css
.section-heading { margin-bottom: calc(2 * var(--space-unit)); }
.section-body    { margin-bottom: calc(3 * var(--space-unit)); }
.section-cta     { margin-top: calc(4 * var(--space-unit)); }
```

---

## グリッド破壊テクニック

均等グリッドから脱出するための具体的テクニック。

### 1. スパン変更

```css
.grid-varied {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1.5rem;
}
/* 子要素ごとにスパンを変える */
.item-feature { grid-column: span 4; }
.item-small   { grid-column: span 2; }
.item-wide    { grid-column: span 3; }
```

### 2. auto-fit + minmax（自然な折り返し）

```css
.grid-natural {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}
```

### 3. Masonry 風（CSS Grid + dense）

```css
.grid-masonry {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-flow: dense;
  gap: 1rem;
}
.tall { grid-row: span 2; }
.wide { grid-column: span 2; }
```

### 4. Flexbox ラップ + 不均一幅

```css
.flex-varied {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.flex-varied > * { flex: 1 1 300px; }
.flex-varied > :first-child { flex-basis: 60%; }
```

### 5. CSS Subgrid（モダンブラウザ）

```css
.parent { display: grid; grid-template-columns: repeat(4, 1fr); }
.child  { display: grid; grid-template-columns: subgrid; grid-column: span 2; }
```
