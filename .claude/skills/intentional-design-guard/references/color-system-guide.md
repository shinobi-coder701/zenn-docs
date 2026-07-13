# Color System Guide

デザイントークンとしてのカラーパレット構築手順。
「コンセプト → 主色 → ニュートラル → アクセント」の順で設計する。

---

## 目次

1. [構築手順](#構築手順)
2. [CSS テンプレート](#css-テンプレート)
3. [Tailwind 統合](#tailwind-統合)
4. [ムード別パレット例](#ムード別パレット例)
5. [背景表現テクニック](#背景表現テクニック)
6. [アンチパターン](#アンチパターン)

---

## 構築手順

### Step 1: 主色の決定

- ブランドカラーがあればそれを主色にする
- なければ、Step 1 の「ムード/トーン」から連想される色を1色選ぶ
- **紫系 (`#6B21A8`〜`#7C3AED` 範囲) は AI シグナルのため回避**

| ムード | 推奨色相範囲 | 例 |
|--------|-------------|-----|
| 信頼・権威 | ネイビー〜ダークブルー (210°-230°) | `#1e3a5f` |
| 軽快・親しみ | ティール〜エメラルド (160°-180°) | `#0d9488` |
| 専門・精密 | スレートブルー〜チャコール (200°-220°) | `#334155` |
| 温かみ | テラコッタ〜アンバー (15°-35°) | `#c2652a` |
| 先鋭・前衛 | チャートリューズ〜ライム (75°-95°) | `#84cc16` |
| 高級・洗練 | ダークゴールド〜オリーブ (40°-55°) | `#92702a` |
| 雑誌・エディトリアル | 赤〜朱 (0°-15°) | `#b91c1c` |

### Step 2: ニュートラル群の導出

**純粋なグレー（R=G=B）は使わない。** 主色の色相を 5〜15% 混ぜたニュートラルを作る。

手順:
1. 主色の HSL 色相を取得
2. 彩度を 3〜8% に下げる
3. 明度を段階的に変える（95%, 90%, 80%, 40%, 20%, 10%）

```
例: 主色がネイビー (hsl(220, 60%, 25%)) の場合
  --neutral-50:  hsl(220, 8%, 96%)   ← ほぼ白だが微青み
  --neutral-100: hsl(220, 6%, 92%)
  --neutral-200: hsl(220, 5%, 85%)
  --neutral-500: hsl(220, 4%, 46%)
  --neutral-800: hsl(220, 5%, 18%)
  --neutral-950: hsl(220, 8%, 8%)    ← ほぼ黒だが微青み
```

### Step 3: アクセント色の追加

主色から以下のいずれかの関係でアクセント色を1〜2色追加:

| 関係 | 色相差 | 特徴 |
|------|--------|------|
| 補色 | ±180° | 最大コントラスト、強い視覚的緊張 |
| 分割補色 | ±150° or ±210° | 補色より穏やか、使いやすい |
| 類似色 | ±30° | 調和的、統一感重視 |
| トライアド | ±120° | バランスの取れた三角配色 |

---

## CSS テンプレート

```css
:root {
  /* === カラートークン === */
  /* 主色 */
  --color-primary: #1e3a5f;
  --color-primary-light: #2a5082;
  --color-primary-dark: #142942;

  /* アクセント */
  --color-accent: #c2652a;
  --color-accent-light: #e8863f;

  /* ニュートラル（主色の色相を混ぜる） */
  --color-surface: hsl(220, 8%, 96%);
  --color-surface-alt: hsl(220, 6%, 92%);
  --color-surface-elevated: hsl(0, 0%, 100%);
  --color-border: hsl(220, 5%, 85%);

  /* テキスト */
  --color-text: hsl(220, 8%, 12%);
  --color-text-muted: hsl(220, 4%, 46%);
  --color-text-inverse: hsl(220, 8%, 96%);

  /* セマンティック */
  --color-success: #16a34a;
  --color-warning: #d97706;
  --color-error: #dc2626;
  --color-info: var(--color-primary-light);
}
```

### ダークテーマ対応

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-surface: hsl(220, 8%, 8%);
    --color-surface-alt: hsl(220, 6%, 12%);
    --color-surface-elevated: hsl(220, 5%, 16%);
    --color-border: hsl(220, 5%, 22%);
    --color-text: hsl(220, 8%, 92%);
    --color-text-muted: hsl(220, 4%, 60%);
  }
}
```

---

## Tailwind 統合

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: 'var(--color-primary)',
          light: 'var(--color-primary-light)',
          dark: 'var(--color-primary-dark)',
        },
        accent: {
          DEFAULT: 'var(--color-accent)',
          light: 'var(--color-accent-light)',
        },
        surface: {
          DEFAULT: 'var(--color-surface)',
          alt: 'var(--color-surface-alt)',
          elevated: 'var(--color-surface-elevated)',
        },
      },
    },
  },
}
```

**禁止**: `bg-blue-500`, `text-purple-600` 等の Tailwind デフォルト色の直接使用。必ず `extend` 経由で登録した意味名を使うこと。

---

## ムード別パレット例

### Confident（信頼・権威）
```css
--color-primary: #1e3a5f;     /* ネイビー */
--color-accent: #c2652a;      /* テラコッタ */
--color-surface: hsl(220, 8%, 96%);
--color-text: hsl(220, 8%, 12%);
```

### Playful（軽快・親しみ）
```css
--color-primary: #0d9488;     /* ティール */
--color-accent: #f59e0b;      /* アンバー */
--color-surface: hsl(170, 6%, 97%);
--color-text: hsl(170, 8%, 15%);
```

### Technical（専門・精密）
```css
--color-primary: #334155;     /* スレート */
--color-accent: #06b6d4;      /* シアン */
--color-surface: hsl(215, 5%, 97%);
--color-text: hsl(215, 8%, 10%);
```

### Warm（温かみ）
```css
--color-primary: #92400e;     /* アンバーブラウン */
--color-accent: #059669;      /* エメラルド */
--color-surface: hsl(30, 10%, 97%);
--color-text: hsl(30, 8%, 12%);
```

### Edgy（先鋭・前衛）
```css
--color-primary: #18181b;     /* ほぼ黒 */
--color-accent: #84cc16;      /* ライム */
--color-surface: hsl(0, 0%, 98%);
--color-text: hsl(240, 5%, 10%);
```

### Luxury（高級・洗練）
```css
--color-primary: #44403c;     /* ストーン */
--color-accent: #b45309;      /* ダークゴールド */
--color-surface: hsl(30, 6%, 96%);
--color-text: hsl(30, 5%, 12%);
```

---

## 背景表現テクニック

グラデーション以外で深みと個性を出す手法。

### 1. SVG ノイズテクスチャ

```css
.surface-textured {
  background-color: var(--color-surface);
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
}
```

### 2. 幾何学パターン（ドット）

```css
.surface-dots {
  background-color: var(--color-surface);
  background-image: radial-gradient(var(--color-border) 1px, transparent 1px);
  background-size: 20px 20px;
}
```

### 3. 多層 box-shadow による奥行き

```css
.card-depth {
  box-shadow:
    0 1px 2px hsl(220 5% 50% / 0.04),
    0 4px 8px hsl(220 5% 50% / 0.06),
    0 12px 24px hsl(220 5% 50% / 0.08);
}
```

### 4. グレインオーバーレイ

```css
.surface-grain::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,..."); /* ノイズ SVG */
  mix-blend-mode: overlay;
  opacity: 0.03;
  pointer-events: none;
}
```

### 5. backdrop-filter（ガラスモーフィズム代替）

```css
.glass {
  background: hsl(220 8% 96% / 0.7);
  backdrop-filter: blur(12px) saturate(1.2);
  border: 1px solid hsl(220 5% 85% / 0.5);
}
```

---

## アンチパターン

| パターン | なぜ NG か | 代替 |
|---------|-----------|------|
| `bg-gradient-to-r from-purple-500 to-blue-500` | AI スロップの最大シグナル | 主色ベースの単色 + テクスチャ |
| `bg-white` + カラフルカード群 | 色に意味がなく散漫 | ニュートラル surface + アクセント1色 |
| `gray-100`〜`gray-900` をそのまま | 無機質、プロジェクト感ゼロ | 主色混ぜニュートラル |
| 黒背景 + ネオングロー | サイバーパンク量産型 | ダーク surface + 落ち着いたアクセント |
| 5色以上の均等使用 | 焦点が分散 | 主色 + アクセント1〜2色に絞る |
