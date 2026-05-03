---
marp: true
theme: excel
paginate: true
size: 16:9
html: true
style: |
  /* @theme excel
     Excel Theme for Marp — Clean, professional presentation design
     Supports Japanese and English content
  */
  
  /* =========================================
     Base
     ========================================= */
  section {
    --accent:      #3b82f6;
    --accent-warm: #f59e0b;
    --dark:        #0f172a;
    --dark-2:      #1e293b;
    --muted:       #64748b;
    --border:      #e2e8f0;
    --bg-subtle:   #f8fafc;
  
    width: 1280px;
    height: 720px;
    box-sizing: border-box;
    font-family: "Hiragino Sans", "BIZ UDGothic", "Yu Gothic Medium",
                 "Noto Sans JP", "Segoe UI", -apple-system, sans-serif;
    background: #ffffff;
    color: #1e293b;
    padding: 48px 72px 58px;
    font-size: 24px;
    line-height: 1.65;
    display: flex;
    flex-direction: column;
    position: relative;
  }
  
  section::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent), var(--accent-warm));
  }
  
  section::after {
    font-size: 0.5em;
    color: var(--muted);
    bottom: 20px;
    right: 40px;
    letter-spacing: 0.04em;
  }
  
  h1 {
    font-size: 2.0em;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 14px;
    line-height: 1.2;
    letter-spacing: -0.02em;
  }
  
  h2 {
    font-size: 1.45em;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 18px;
    padding-bottom: 10px;
    border-bottom: 3px solid var(--accent);
    line-height: 1.3;
  }
  
  h3 {
    font-size: 1.05em;
    font-weight: 600;
    color: var(--accent);
    margin: 14px 0 8px;
  }
  
  p { margin: 8px 0; }
  
  ul, ol { margin: 8px 0; padding-left: 1.4em; }
  li { margin: 5px 0; }
  ul > li::marker { color: var(--accent); font-size: 1.1em; }
  ol > li::marker { color: var(--accent); font-weight: 700; }
  
  strong { color: var(--accent); font-weight: 700; }
  em     { color: var(--accent-warm); font-style: normal; font-weight: 600; }
  
  code {
    font-family: "JetBrains Mono", "Fira Code", "Source Code Pro", monospace;
    background: var(--bg-subtle);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 6px;
    font-size: 0.82em;
    color: #be123c;
  }
  
  pre {
    background: #0f172a;
    border-radius: 10px;
    padding: 18px 22px;
    margin: 10px 0;
    flex-shrink: 0;
  }
  
  pre code {
    background: none;
    border: none;
    color: #e2e8f0;
    padding: 0;
    font-size: 0.75em;
    line-height: 1.6;
  }
  
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
    font-size: 0.88em;
  }
  
  th {
    background: var(--accent);
    color: white;
    padding: 8px 14px;
    text-align: left;
    font-weight: 600;
  }
  
  td {
    padding: 7px 14px;
    border-bottom: 1px solid var(--border);
  }
  
  tr:nth-child(even) td { background: var(--bg-subtle); }
  
  blockquote {
    border-left: 4px solid var(--accent);
    background: var(--bg-subtle);
    margin: 10px 0;
    padding: 10px 18px;
    border-radius: 0 6px 6px 0;
    color: var(--muted);
    font-size: 0.95em;
  }
  
  hr {
    border: none;
    border-top: 2px solid var(--border);
    margin: 16px 0;
  }
  
  section.title {
    background: linear-gradient(145deg, #0f172a 0%, #1e3a5f 55%, #0f2944 100%);
    color: white;
    justify-content: flex-end;
    padding-bottom: 64px;
  }
  
  section.title::before { height: 6px; }
  
  section.title h1 {
    color: white;
    font-size: 2.4em;
    letter-spacing: -0.03em;
    max-width: 86%;
    border-bottom: none;
    margin-bottom: 0;
  }
  
  section.title h2 {
    color: rgba(255,255,255,0.65);
    font-size: 1.0em;
    font-weight: 400;
    border-bottom: none;
    margin-top: 12px;
  }
  
  section.title p {
    color: rgba(255,255,255,0.5);
    font-size: 0.8em;
    margin-top: 28px;
  }
  
  section.section {
    background: var(--accent);
    color: white;
    justify-content: center;
  }
  
  section.section::before {
    background: rgba(255,255,255,0.25);
  }
  
  section.section h2 {
    color: white;
    font-size: 2.0em;
    border-bottom: 2px solid rgba(255,255,255,0.4);
    padding-bottom: 12px;
  }
  
  section.section p {
    color: rgba(255,255,255,0.8);
    font-size: 0.9em;
  }
  
  section.lead {
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  
  section.lead h1 {
    font-size: 2.5em;
    border-bottom: none;
  }
  
  section.lead h2 {
    border-bottom: none;
    color: var(--muted);
    font-weight: 400;
  }
  
  section.dark {
    background: #0f172a;
    color: #e2e8f0;
  }
  
  section.dark h1 { color: white; }
  
  section.dark h2 {
    color: white;
    border-color: var(--accent);
  }
  
  section.dark code {
    background: #1e293b;
    border-color: #334155;
    color: #94a3b8;
  }
  
  section.dark td { border-color: #334155; }
  section.dark tr:nth-child(even) td { background: #1e293b; }
  section.dark blockquote { background: #1e293b; }
  
  section.ending {
    background: linear-gradient(145deg, #0f172a 0%, #1e3a5f 100%);
    color: white;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  
  section.ending::before { height: 6px; }
  
  section.ending h1 {
    color: white;
    font-size: 2.8em;
    border-bottom: none;
    margin-bottom: 12px;
  }
  
  section.ending h2 {
    color: rgba(255,255,255,0.65);
    border-bottom: none;
    font-weight: 400;
    font-size: 1.0em;
  }
  
  section.ending p {
    color: rgba(255,255,255,0.5);
    font-size: 0.82em;
    margin-top: 20px;
  }
  
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 36px;
    align-items: start;
  }
  
  .columns.col-3    { grid-template-columns: 1fr 1fr 1fr; gap: 24px; }
  .columns.col-6-4  { grid-template-columns: 3fr 2fr; }
  .columns.col-4-6  { grid-template-columns: 2fr 3fr; }
  .columns.middle   { align-items: center; }
  
  .card {
    background: var(--bg-subtle);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 6px 0;
  }
  
  .card.accent  { border-left: 4px solid var(--accent);      background: rgba(59,130,246,0.04); }
  .card.warn    { border-left: 4px solid var(--accent-warm); background: rgba(245,158,11,0.04); }
  .card.success { border-left: 4px solid #22c55e;            background: rgba(34,197,94,0.04); }
  .card.danger  { border-left: 4px solid #ef4444;            background: rgba(239,68,68,0.04); }
  
  .highlight {
    background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(245,158,11,0.08));
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 10px;
    padding: 14px 22px;
    font-size: 1.05em;
    font-weight: 600;
    text-align: center;
    margin: 10px 0;
  }
  
  .number {
    font-size: 2.8em;
    font-weight: 800;
    color: var(--accent);
    line-height: 1.0;
    display: block;
    letter-spacing: -0.03em;
  }
  
  .number.warm { color: var(--accent-warm); }
  
  .tag {
    display: inline-block;
    background: var(--accent);
    color: white;
    font-size: 0.6em;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
    vertical-align: middle;
    letter-spacing: 0.03em;
    margin: 0 3px;
  }
  
  .tag.warm    { background: var(--accent-warm); }
  .tag.success { background: #22c55e; }
  .tag.danger  { background: #ef4444; }
  .tag.outline { background: none; border: 1.5px solid var(--accent); color: var(--accent); }
  
  .icons {
    display: flex;
    gap: 20px;
    justify-content: center;
    align-items: flex-start;
    margin: 16px 0;
  }
  
  .icon-item { text-align: center; flex: 1; }
  .icon-item .icon  { font-size: 2.2em; display: block; margin-bottom: 6px; }
  .icon-item .label { font-size: 0.75em; font-weight: 600; color: var(--muted); }
  
  .progress {
    height: 8px;
    background: var(--border);
    border-radius: 4px;
    overflow: hidden;
    margin: 6px 0 12px;
  }
  
  .progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--accent-warm));
    border-radius: 4px;
  }
  
  .steps { counter-reset: step; }
  .step {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin: 10px 0;
  }
  .step::before {
    counter-increment: step;
    content: counter(step);
    background: var(--accent);
    color: white;
    font-weight: 700;
    font-size: 0.85em;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
  }
---

<!-- _class: title -->

# 開発者のためのSovereign AI: IronClaw 深掘り解説
## 〜Rust製のセキュアなOpenClaw〜

Haruki | AWS Community Builder

---

# 本日のゴール

<div class="card accent">

<strong>機密情報やAPIキー</strong>を安全に扱える自律型AIエージェントの概要と構築方法を理解する

</div>

---

# 本日のポイント

<div class="steps">

<div class="step"><strong>深刻な脆弱性:</strong> 既存エージェントから<strong>機密情報が漏洩</strong>する根本原因</div>
<div class="step"><strong>解決策:</strong> IronClawが提示する<strong>多層防御アーキテクチャ</strong></div>
<div class="step"><strong>究極の安全:</strong> <strong>Rust、WASM、TEE</strong>による鉄壁のガード</div>
<div class="step"><strong>ゼロ・エクスポージャー:</strong> AIに<strong>鍵を見せない</strong>革新的なロジック</div>
<div class="step"><strong>エコシステム:</strong> 自己拡張するツール群と<strong>1クリックデプロイ</strong></div>


---

# 既存のAIエージェントが抱える「秘密情報漏洩」の罠

<div class="card danger">

### 致命的なリスク
従来のエージェントは<strong>生のAPIキー</strong>を環境変数やプロンプトに保持します。<br/>LLMが巧妙なプロンプト注入で騙されればすべての鍵が盗まれます。

</div>

<div class="highlight">
現在のエージェントは「セキュリティ後退型」です。<br/>一時的な利便性のために、開発者の責務である安全性を犠牲にしています。
</div>

---

# 既存のAIエージェントが抱える「秘密情報漏洩」の罠

<div class="card warn">

### 放置できない問題
- <strong>ログの露出:</strong> ベクトルDBに機密情報がインデックス化される
- <strong>プロバイダー特権:</strong> クラウド運営者がすべてのデータにアクセス可能
- <strong>プライバシー欠如:</strong> 実行時の思考プロセスが外部に筒抜け

</div>

<div class="highlight">
現在のエージェントは「セキュリティ後退型」です。<br/>一時的な利便性のために、開発者の責務である安全性を犠牲にしています。
</div>

---

<!-- _class: lead -->

# そこで IronClaw だ！  
## Near AIが開発したRust製のセキュアなAIエージェント

---

![bg](./../images/nearai_ironclaw-1/0.png)

---

![bg](./../images/nearai_ironclaw-1/1.png)

---
# 「暗号化ボルト」でAPIキーを厳重に保護

<div class="columns col-3">
<div class="card accent">

### 耐タンパ性
<strong>AES-256-GCM</strong>で保存データを秘匿。たとえ物理的にディスクを奪われても、中身の解読は不可能。
</div>
<div class="card success">

### ハードウェアとの密結合
<strong>Apple Secure Enclave</strong>等の安全な専用チップと連携。
</div>
<div class="card warn">

### 痕跡を残さないメモリ管理
使用した秘密情報はメモリ上から<strong>瞬時に完全抹消</strong>。メモリに残る「わずかな痕跡」すら許しません。
</div>
</div>

<br/>

<div class="highlight">
単に隠すのではなく、<strong>権限のないコードからは物理的にアクセス不可能</strong>な状態を作り出します。
</div>

---

# Rust & WASMによる強力なサンドボックス
<div>

### 妥協のない安全性と性能
- <strong>Rustエンジン:</strong> nullポインタやバッファオーバーフローを排除。
- <strong>ガベージコレクションなし:</strong> リアルタイムな推論を支える決定論的なパフォーマンス。

</div>

---

# Rust & WASMによる強力なサンドボックス

<div class="card accent">

### 厳格なWASM境界
すべてのツールは<strong>WebAssembly</strong>上で動作。
- <strong>ディスクアクセス禁止</strong> (明示的な許可制)
- <strong>ネットワーク制限</strong> (許可リスト方式)
- <strong>実行リソース制限</strong> (無限ループの強制終了)

</div>

---

# Near AI Cloudが可能にする堅牢な隔離空間

<div class="columns middle">
<div>

<span class="number">TEE</span>

</div>
<div>

- <strong>機密コンピューティング:</strong> <br/>CPUレベルの暗号化。OSや管理者であっても実行内容を覗けません。
- <strong>リモート・アテステーション:</strong><br/> 実行されているコードのハッシュ値を検証し、改ざんがないことを証明。
- <strong>Nearエコシステム:</strong> <br/>分散型の信頼基盤により、中央集権的な監視を排除します。

</div>
</div>

---

# 4層の多層防御アーキテクチャ

<div class="steps">
<div class="step">

<strong>セーフティ・フィルター:</strong> LLMの出力をリアルタイム監視し、偶発的なデータ漏洩を未然に防ぎます。
</div>
<div class="step">

<strong>WASMアイソレーション:</strong> カスタムツールを軽量かつ制限された環境で隔離実行します。
</div>
<div class="step">

<strong>Dockerによる硬化:</strong> 複雑なビルドタスクに対し、クリーンで隔離された実行空間を提供します。
</div>
<div class="step">

<strong>ホスト側インジェクション:</strong> LLMkからは機密性の高い情報を<strong>完全に見えない状態</strong>に保ちます。
</div>
</div>

---

# ゼロ・エクスポージャー：AIに鍵を見せない革新

<div class="columns col-4-6">
<div class="card">

### 従来
LLM: <br/>鍵 `sk-123` を使ってリポジトリ作成
<strong>結果:</strong> <br/>鍵が履歴に残り、漏洩のリスク。 ❌

</div>
<div>

### IronClaw
1. LLMがツール実行（例: `create_repo`）を要求
2. <strong>ホスト・プロキシ</strong>が要求をインターセプト
3. プロキシが<strong>ボルト</strong>から鍵を安全に取得
4. プロキシがAPI実行し、<strong>結果のみ</strong>をLLMに返す

</div>
</div>

<div class="highlight">
LLMを「脳」、ホスト・プロキシを「<strong>安全な手</strong>」として役割を完全に分離します。
</div>

---

# 既存エージェント vs IronClaw

| セキュリティ機能 | 一般的なPythonエージェント | IronClaw (Near AI) |
| --- | --- | --- |
| <strong>メモリ管理</strong> | ガベージコレクタ (遅延あり) | <strong>所有権モデル (高速・安全)</strong> |
| <strong>ツール隔離</strong> | なし / プロセスレベル | <strong>WASM / TEE (ハードウェア隔離)</strong> |
| <strong>資格情報の扱い</strong> | LLMに直接渡される | <strong>ホスト境界で注入 (非露出)</strong> |
| <strong>プロバイダーの秘匿性</strong> | 運営者が閲覧可能 | <strong>エンドツーエンド暗号化 (TEE)</strong> |
| <strong>スケーラビリティ</strong> | リソース消費大 | <strong>軽量かつ検証可能</strong> |

---

# 自己拡張するエージェント：ツール・メモリ・自動化

<div class="columns col-3">
<div class="card accent">

### ユニバーサルMCP
<strong>Model Context Protocol</strong>を通じて、あらゆる外部サービスと安全に連携。
</div>
<div class="card success">

### 無限のコンテキスト
高速なローカルキャッシュと<strong>暗号化されたベクトル検索</strong>を組み合わせたハイブリッドメモリ。
</div>
<div class="card warn">

### オートパイロット
自律的なジョブスケジューリングと、<strong>自己修復機能</strong>を備えたワークフロー実行。
</div>
</div>

---

# 1クリックでデプロイ！始め方の4ステップ

<div class="columns col-4">
<div class="card accent">

### 1. 接続
`agent.near.ai` にアクセスし、セキュアなIDを連携します。
</div>
<div class="card success">

### 2. 設定
「LLMと「スキル」（ツール）を選択します。
</div>
<div class="card warn">

### 3. 保護
IronClaw ボルトにシークレットを保存。
</div>
<div class="card danger">

### 4. 起動
Near AI Cloudで即座にデプロイ。
</div>
</div>

---

# Near AIがもたらす「自分専用」の信頼できるAI

<div class="columns col-3">
<div class="card">

### パーソナル守護者
巨大IT企業にデータを渡すことなく、資産や健康状態を管理するエージェント。
</div>
<div class="card">

### 信頼不要の経済
オンチェーン検証を活用し、ユーザーの代わりに自律的に取引を行うエージェント。
</div>
<div class="card">

### オープンな標準
「Sovereign（主権）」が特殊機能ではなく、AIの当たり前となる世界へ。
</div>
</div>

<div class="highlight">
「インフラを所有していないなら、そのAIも所有していないのと同じだ」 <br/> Near AI 創設者 (Transformer共著者) Illia Polosukhin
</div>

---

# 今日から始めよう！ IronClaw ！！

<div>
<div>

- <strong>監査可能な透明性:</strong> 最大限の安全性と透明性を確保するために設計されたアーキテクチャ。
- <strong>開発者ファースト:</strong> プライバシーを重視するエンジニアによる、エンジニアのための設計。
- <strong>試す:</strong> <strong>agent.near.ai</strong> で今すぐにデプロイ！

---

![bg](./../images/nearai_ironclaw-1/6.png)

---

![bg](./../images/nearai_ironclaw-1/2.png)

---

![bg](./../images/nearai_ironclaw-1/5.png)

---

![bg](./../images/nearai_ironclaw-1/7.png)

---

![bg](./../images/nearai_ironclaw-1/8.png)

---

![bg](./../images/nearai_ironclaw-1/9.png)

---

![bg](./../images/nearai_ironclaw-1/11.png)

---

![bg](./../images/nearai_ironclaw-1/12.png)

---

<!-- _class: ending -->

# Thank you!
## Build Secure. Build Sovereign.

[agent.near.ai](https://agent.near.ai) | [github.com/nearai/ironclaw](https://github.com/nearai/ironclaw)

🦞 **IronClaw: Rust製のセキュアなAI エージェント**