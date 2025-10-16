---
marp: true
theme: default
class: lead
paginate: true
size: 16:9
math: katex
header: "Codex Meetup Japan #1 | 2025-10-14"
footer: "@harukikondo | Spec駆動開発 × Codex"
---

<!-- _class: lead -->
<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
# Spec駆動開発 × Codex CLI
## Web3ハッカソンを数時間で制する方法
### 伝説のテックエバンジェリスト / @harukikondo

<!-- speaker: 冒頭で自己紹介とハッカソン入賞の実績を提示し、Codex CLIとSpec駆動開発の組み合わせに興味を持ってもらう。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## 今日のゴール
- ハッカソンで「時間が足りない」を終わらせる
- Spec駆動開発のコアとCodex CLIの役割を理解する
- 明日から実践できるコンテキスト準備術を持ち帰る

<!-- speaker: 目的を明確化し、参加者に10分の投資で得られる価値を提示する。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## なぜ今 AI駆動開発？
- 要件整理からテスト作成までAIが担う時代
- GitHub Copilot / Cursor / Claude Code… ツール乱立
- でも「仕様がふわっと」で破綻するケースが急増

<!-- speaker: AIツールが増えたが結果が出ない理由を共有し、Spec駆動開発への導線を敷く。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## Spec駆動開発とは？
- **仕様( Spec )をAIと共に極めてから実装に入る**
- AIは優秀な実装エージェント、人間は監督兼PM
- 仕様 → 設計 → タスク → 実装 の順序を徹底

<!-- speaker: Spec駆動の定義を端的に説明し、「順序の厳守」が鍵だと強調する。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## 3つのフェーズ
1. **準備**: ゴール, 情報, コンテキストを同期
2. **Spec生成**: 要件 → 設計 → タスクをAIで出力
3. **実装**: AI実装と人間レビューをループ

<!-- speaker: フェーズごとに誰が何をするか、レビューゲートがあることを強調。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
<!-- _vCenter: true -->
## フェーズ構造図

<div class="diagram-steps diagram-steps--compact">
  <div class="diagram-step">
    <div class="diagram-step__index">1</div>
    <div class="diagram-step__body">
      <h3>Phase 1 準備</h3>
      <p>ゴール定義 / 情報収集 / コンテキスト整形</p>
    </div>
  </div>
  <div class="diagram-step">
    <div class="diagram-step__index">2</div>
    <div class="diagram-step__body">
      <h3>Phase 2 Spec生成</h3>
      <p>要件レビュー → 設計レビュー → タスク分解</p>
    </div>
  </div>
  <div class="diagram-step">
    <div class="diagram-step__index">3</div>
    <div class="diagram-step__body">
      <h3>Phase 3 実装</h3>
      <p>AI実装と人間レビューで承認まで回す</p>
    </div>
  </div>
</div>

<p class="diagram-note">数字の順に左→右へ進むフロー</p>

<!-- speaker: 図を使って3フェーズの流れを視覚的に再確認し、レビューサイクルを強調。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## 最強な理由
- **意図のズレ激減**: 仕様レビューで初動の手戻りを潰す
- **速度と品質の両立**: タスクごとの短サイクルで検証
- **学習サイクルが回る**: 仕様テンプレが資産として残る

<!-- speaker: 実際にどの指標が改善したか（開発スピード、品質）をハッカソン経験と絡めて語る。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## ツールスタック
### Kiro
- Spec作成を前提にしたAWS発AI IDE
- `steering`でプロダクト哲学を常に読み込ませる
### Codex CLI
- Codexエージェントをローカルから制御
- `.codex/`設定でKiro流ワークフローを再現

<!-- speaker: Kiroで得た体験をCodex CLIにも移植できた話を共有。設定ファイルの一貫性が重要。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## Spec駆動ワークフロー実践
- `.kiro/specs` で土台を同期
- レビュー承認済みの成果物だけ次工程へ
- タスクはAI実装と人間レビューで前進

<!-- speaker: レビューをサボらないこと、タスクは細切れにすることを具体例とともに紹介。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
<!-- _vCenter: true -->
## ワークフロー図

<div class="diagram-flowgrid">
  <div class="diagram-steps diagram-steps--row">
    <div class="diagram-step">
      <div class="diagram-step__index">1</div>
      <div class="diagram-step__body">
        <h3>.kiro/specs</h3>
        <p>テンプレ確認と更新</p>
      </div>
    </div>
    <div class="diagram-step">
      <div class="diagram-step__index">2</div>
      <div class="diagram-step__body">
        <h3>要件ドキュメント</h3>
        <p>AI生成 → 人間承認</p>
      </div>
    </div>
    <div class="diagram-step">
      <div class="diagram-step__index">3</div>
      <div class="diagram-step__body">
        <h3>設計ドキュメント</h3>
        <p>構成定義 → レビュー</p>
      </div>
    </div>
  </div>
  <div class="diagram-flowgrid__arrow">⇩</div>
  <div class="diagram-steps diagram-steps--row">
    <div class="diagram-step">
      <div class="diagram-step__index">4</div>
      <div class="diagram-step__body">
        <h3>タスクボード</h3>
        <p>粒度調整と優先順位付け</p>
      </div>
    </div>
    <div class="diagram-step">
      <div class="diagram-step__index">5</div>
      <div class="diagram-step__body">
        <h3>AI実装</h3>
        <p>Codex CLIでタスク遂行</p>
      </div>
    </div>
    <div class="diagram-step">
      <div class="diagram-step__index">6</div>
      <div class="diagram-step__body">
        <h3>人間レビュー</h3>
        <p>承認 or フィードバック</p>
      </div>
    </div>
  </div>
</div>

<p class="diagram-note">上段左→右、矢印で下段へ。フィードバック時のみステップ5へ戻る。</p>

<!-- speaker: ドキュメントとレビューの往復を図で指し示し、ボトルネックの可視化を促す。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## コンテキストエンジニアリング術
- ライブラリ名・バージョン・使い方を明記
- 最小構成テンプレートを添付してズレを減らす
- フォルダ構成・命名規約・品質基準を記述
- 背景ストーリーまで伝えてAIをチームメイト化

<!-- speaker: OnChainKitやMiniApp Kitを例に、テンプレ提供が効いた実体験を語る。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## MCPでAIを増強
- **context7**: ライブラリ知識を即参照
- **sequential-thinking**: 思考のチェーンを構造化
- **serena**: リポジトリ全体を俯瞰して依存を把握
- 必要な能力を後付けできるのがMCPの強み

<!-- speaker: MCPを導入した結果、未知のライブラリでも迷わず進めた話をする。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## PizzaDAO Mini Hackathonでの実践
- 数時間でWeb3ネイティブゲームを完成し入賞

<!-- speaker: タイムラインを臨場感を持って語り、短時間で成果を出せた要因を振り返る。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
<!-- _vCenter: true -->
## 当日のタイムライン

<ul class="diagram-timeline">
  <li><span class="time">前日夜</span><span class="event">Specテンプレ整理 / ライブラリ調査</span></li>
  <li><span class="time">09:00</span><span class="event">Kiroで要件・設計・タスク承認</span></li>
  <li><span class="time">13:00</span><span class="event">Codex CLIで実装とレビュー</span></li>
  <li><span class="time">17:00</span><span class="event">デプロイとデモ準備</span></li>
  <li><span class="time">19:00</span><span class="event">プレゼンで入賞決定</span></li>
</ul>

<!-- speaker: タイムラインを指し示し、各フェーズでの意思決定スピードを強調。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## Mini Pizza Game 解体新書
- Farcaster Mini App × Vercelの即時配信
- OnChainKit + WagmiでウォレットUXを一元化
- スコア連動NFTミントまでSpecで自動化

<!-- speaker: 画像の代わりに構成要素を口頭で説明し、Specがあったからこそ繋がったと強調。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
<!-- _vCenter: true -->
## Mini Pizza Game アーキテクチャ

<div class="diagram-steps diagram-steps--arch">
  <div class="diagram-step">
    <div class="diagram-step__index">1</div>
    <div class="diagram-step__body">
      <h3>ユーザー</h3>
      <p>Farcaster Mini Appを起動</p>
    </div>
  </div>
  <div class="diagram-step">
    <div class="diagram-step__index">2</div>
    <div class="diagram-step__body">
      <h3>Farcaster Mini App</h3>
      <p>UI提供 / 行動トラッキング</p>
    </div>
  </div>
  <div class="diagram-step">
    <div class="diagram-step__index">3</div>
    <div class="diagram-step__body">
      <h3>Vercel Edge</h3>
      <p>APIルーティングとスコア計算</p>
    </div>
  </div>
  <div class="diagram-step">
    <div class="diagram-step__index">4</div>
    <div class="diagram-step__body">
      <h3>OnChainKit + Wagmi</h3>
      <p>ウォレット接続と署名</p>
    </div>
  </div>
  <div class="diagram-step">
    <div class="diagram-step__index">5</div>
    <div class="diagram-step__body">
      <h3>Base Smart Contract</h3>
      <p>スコア記録 / イベント発火</p>
    </div>
  </div>
  <div class="diagram-step">
    <div class="diagram-step__index">6</div>
    <div class="diagram-step__body">
      <h3>NFT Mint</h3>
      <p>スコア連動NFT発行</p>
    </div>
  </div>
</div>

<p class="diagram-note">Specに沿って1→6でデータが流れ、必要に応じて4→3で結果を返す</p>

<!-- speaker: 各コンポーネントの役割とデータフローを図で示し、Specで安全に接続できた理由を補足。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## 人間側のマインドセット
- **インプット癖**: トレンド/コミュニティ/公式ドキュメント
- **毎日手を動かす**: テンプレ化してAIへの餌を増やす
- **PM視点**: 目標→タスク分解→フィードバックを回す

<!-- speaker: AI時代こそ人間の役割が増す点を伝え、参加者自身の習慣に落とし込ませる。 -->

---

<!-- _backgroundColor: #050b14 -->
<!-- _color: #d7f9ff -->
## Call to Action
- 自分のプロジェクトにSpecテンプレを1つ作ってみる
- Codex CLIにMCP＋コンテキストを即セットアップ
- ハッカソンや社内PoCで「AI監督モード」を試す

<!-- speaker: 具体的な次の一歩を提示し、今夜・明日に行動してもらう。 -->

---

<style>
:root {
  --accent-neo: #68feda;
  --accent-warm: #f8ff5a;
  --bg-night: #050b14;
  --panel: #0d1f2d;
  --text-main: #d7f9ff;
}

section {
  background: var(--bg-night);
  color: var(--text-main);
  font-family: "Fira Code", "游ゴシック体", "Yu Gothic", sans-serif;
  letter-spacing: 0.02em;
}

h1, h2, h3 {
  color: var(--accent-neo);
}

strong {
  color: var(--accent-warm);
}

a {
  color: var(--accent-neo);
  text-decoration: none;
  border-bottom: 1px solid rgba(104,254,218,0.4);
}

blockquote, pre, code {
  background: rgba(20,40,60,0.7);
  border-left: 4px solid var(--accent-neo);
}

li {
  margin-bottom: 0.4em;
}

.diagram-steps {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  justify-content: center;
  max-width: min(88vw, 840px);
  margin: 0 auto;
}

.diagram-steps--compact {
  max-width: min(80vw, 660px);
}

.diagram-steps--row {
  max-width: min(90vw, 820px);
}

.diagram-steps--wide {
  max-width: min(90vw, 900px);
}

.diagram-steps--arch {
  max-width: min(90vw, 880px);
}

.diagram-flowgrid {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
}

.diagram-flowgrid__arrow {
  font-size: 1.5rem;
  color: var(--accent-neo);
}

.diagram-step {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  background: rgba(13,31,45,0.85);
  border: 1px solid rgba(104,254,218,0.28);
  border-radius: 12px;
  padding: 0.9rem 1rem;
  min-width: 190px;
  max-width: 240px;
  flex: 1 1 200px;
  box-shadow: 0 0 16px rgba(104,254,218,0.08);
}

.diagram-steps--arch .diagram-step {
  border-color: rgba(248,255,90,0.25);
  box-shadow: 0 0 16px rgba(248,255,90,0.08);
}

.diagram-step__index {
  font-size: 1.1rem;
  font-weight: 700;
  line-height: 1;
  background: rgba(104,254,218,0.2);
  color: var(--accent-neo);
  border: 1px solid rgba(104,254,218,0.35);
  border-radius: 999px;
  padding: 0.45rem 0.75rem;
  flex-shrink: 0;
}

.diagram-steps--arch .diagram-step__index {
  background: rgba(248,255,90,0.2);
  color: var(--accent-warm);
  border-color: rgba(248,255,90,0.35);
}

.diagram-step__body h3 {
  margin: 0 0 0.3rem 0;
}

.diagram-step__body p {
  margin: 0;
  font-size: 0.9em;
  line-height: 1.3;
}

.diagram-note {
  margin-top: 0.8rem;
  text-align: center;
  font-size: 0.9em;
  color: rgba(215,249,255,0.8);
}

.diagram-timeline {
  list-style: none;
  padding: 0;
  margin: 0 auto;
  display: grid;
  gap: 0.7rem;
  max-width: min(72vw, 520px);
}

.diagram-timeline li {
  display: grid;
  grid-template-columns: minmax(80px, 30%) 1fr;
  align-items: center;
  background: rgba(13,31,45,0.85);
  border-left: 3px solid var(--accent-neo);
  padding: 0.65rem 1rem;
  border-radius: 10px;
}

.diagram-timeline .time {
  font-weight: 700;
  color: var(--accent-warm);
}

.diagram-timeline .event {
  color: var(--text-main);
}
</style>
