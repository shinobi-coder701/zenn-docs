---
title: "Midnightで匿名予測市場アプリを作ってみた！"
emoji: "🌙"
type: "tech"
topics: ["blockchain", "ゼロ知識証明", "typescript", "react", "web3"]
published: false
publication_name: "midnight"
---

## 予測市場、だいたい「見えすぎ」問題を抱えている

Polymarketのようなオンチェーン予測市場をみていて、ずっと気になっていたことがあります。

**誰が何に賭けたか、ほぼリアルタイムで丸見えなことです**。

大口が特定の結果に大きく張った瞬間、それを見た他の参加者が同じ方向に追随します。オッズはその追随によって動きます。これは別に不正でも何でもなく、公開型の台帳を使えば当然そうなります。ただ、「自分の予想を先に晒したくない」という素朴な欲求には応えられていません。

じゃあ、投票が締め切られるまで中身を隠しておける予測市場を作れないか。誰かを信頼して秘密を預ける必要もなく、です。

これを試すために作ったのが `Hidden League Forecast` という、架空のサッカーリーグの勝者を当てるだけの小さいdAppです。使っているのは Midnight Network の Compact というスマートコントラクト言語で、コミット・リビール方式とゼロ知識証明を組み合わせて「予想の中身は隠したまま、賭け金の集計だけは公開する」を実現しています。

この記事では、実際に書いたコントラクトのコードを見せながら、何がどう隠れて何が公開されるのか、そしてハマった部分を含めて書きます。

対象読者は、コミット・リビール方式やゼロ知識証明という言葉は知っているものの、実際のコードでどう書くのかまでは見たことがない方です。Solidityなど別のスマートコントラクト言語の経験があれば読みやすいはずですが、必須ではありません。逆に、Midnight本体のプロトコル内部(証明システムの詳細など)には踏み込みません。あくまで「1つのdAppをどう設計したか」の話に絞っています。

:::message
学習目的のサンプルであり、本番資産は一切扱いません。デモポイントでの参加と、単一の運営者(Steward)を信頼する設計になっています。この制約は記事の後半で詳しく書きます。
:::

## 作ってみたアプリのデモ動画

[!['altテキスト'](/images/midnight_simple_app-5/youtube-thumbnail.png)](https://youtu.be/G4T-L-rVgzU)

![Lace Walletに接続し、マーケットのデプロイまたは参加を選ぶトップ画面](/images/midnight_simple_app-5/0.jpg)
*Lace Walletを接続すると、Shielded Addressと残高が表示されます。ここで新規マーケットをデプロイするか、既存のコントラクトアドレスを入力して参加するかを選びます。*

## 全体の流れ

やっていることはシンプルです。

```text
OPEN → REVEAL → AWAITING RESULT → RESOLVED → CLAIM
```

1. Lace Walletを接続し、マーケットをデプロイするか既存のものに参加します
2. 4チーム(Amber Foxes / Cedar Owls / Harbor Whales / Meadow Bears)から1つを選び、10〜500ポイントを賭けます
3. 運営者が予想の受付を締め切ると、参加者は自分の予想を「開示」します
4. 運営者が結果を記録します
5. 勝ったチームを選んでいた参加者は、パリミュチュエル方式(負けた側の掛け金も勝った側で山分けする方式)の報酬を請求します

```text
reward = floor(総プール × 自分の賭け金 / 勝ったチームのプール)
```

ポイントは、ステップ2の時点では「どのチームに賭けたか」がチェーン上のどこにも記録されないことです。記録されるのは「賭け金の額」と「コミットメント(後で照合するためのハッシュ値)」だけです。ステップ3の開示まで、他の参加者はおろか運営者にも見えません。

## Compactが何をしてくれるのか

Midnight の Compact は、コントラクトの中で「この値は証明の中では使うが、台帳には一切書き込まない」という変数(witness)を扱える言語です。逆に、台帳に書き込む値は `disclose()` を通すことを強制されます。うっかり秘密の値をそのままログに残す、みたいな事故を型システムレベルで防いでくれます。

コントラクト全体はこれだけしかありません(`pkgs/contract/src/prediction-market.compact`)。

```compact
witness local_secret_key(): Bytes<32>;
witness get_selected_team(): Team;
witness get_prediction_salt(): Bytes<32>;
witness store_prediction(team: Team, stake: Uint<64>, salt: Bytes<32>): [];
```

秘密鍵、選んだチーム、ソルト(塩)。この3つはすべて witness で、ブラウザのローカルにしか存在しません。台帳側の宣言はこちらです。

```compact
export ledger phase:                 MarketPhase;
export ledger admin_key:             Bytes<32>;
export ledger commitments:           Map<Bytes<32>, Bytes<32>>;
export ledger stakes:                Map<Bytes<32>, Uint<64>>;
export ledger participants:          Set<Bytes<32>>;
export ledger revealed:              Set<Bytes<32>>;
// ... 各チームのプールなど
```

`commitments` に入るのはハッシュ値だけで、`stakes` に入るのは金額だけです。「誰が」「いくら」賭けたかは公開情報ですが、「何に」賭けたかはこの時点でどこにも存在しません。

## コミット：ハッシュだけを台帳に残す

賭けるときに呼ぶ回路がこちらです。

```compact
export circuit commit_prediction(stake: Uint<64>): [] {
  const public_stake = disclose(stake);
  assert(phase == MarketPhase.open, "Predictions are closed");
  assert(public_stake >= 10 && public_stake <= 500, "Stake must be between 10 and 500 points");

  const key = derive_participant_key(local_secret_key());
  assert(!participants.member(disclose(key)), "Participant already committed");
  const team = get_selected_team();
  const salt = get_prediction_salt();
  const commitment = make_prediction_commitment(key, team, public_stake, salt);
  store_prediction(team, public_stake, salt);

  participants.insert(disclose(key));
  commitments.insert(disclose(key), disclose(commitment));
  stakes.insert(disclose(key), public_stake);
  participant_count.increment(1);
  total_pool = (total_pool + public_stake) as Uint<64>;
}
```

`team` はここで一度も `disclose()` されていません。使われているのは `make_prediction_commitment()` の入力としてだけで、その戻り値(ハッシュ)だけが `disclose(commitment)` を経て台帳に書かれます。

```compact
pure circuit make_prediction_commitment(
  participant_key: Bytes<32>,
  team: Team,
  stake: Uint<64>,
  salt: Bytes<32>
): Bytes<32> {
  const team_bytes = ((team as Field) as Bytes<32>);
  const stake_bytes = ((stake as Field) as Bytes<32>);
  return persistentHash<Vector<5, Bytes<32>>>([
    pad(32, "forecast:pick:v1"), participant_key, team_bytes, stake_bytes, salt
  ]);
}
```

`persistentHash` の第一要素に `"forecast:pick:v1"` という固定文字列を混ぜているのは、ドメイン分離(domain separation)と呼ばれる定石です。同じ入力値でも用途ごとに別のタグを混ぜておけば、別の回路で偶然同じハッシュ値が出て混同する、という事故を防げます。参加者キーの導出(`derive_participant_key`)でも `"forecast:participant:v1"` という別のタグを使っています。

ソルトを混ぜているのは、賭け金が10〜500ポイントとかなり狭い範囲しかないからです。ソルトなしだと、4チーム×491通りの賭け金の組み合わせを総当たりでハッシュ化すれば、外部の観察者でもコミットメントから元の値を逆引きできてしまいます。ランダムなソルトを混ぜることで、その総当たりを実質不可能にしています。

実際の画面では、チームと賭け金(Confidence points)を選んでから「Seal my forecast」を押します。この時点ではチームの内訳(左側の一覧)はまだ動きません。

![チームと賭け金を選び、Seal my forecastを押す直前のコミット画面](/images/midnight_simple_app-5/2.jpg)
*Harbor Whalesに370ポイントを賭けようとしている状態です。左のチーム一覧はまだ「SEALED」表示のみで、内訳は一切公開されていません。*

「Seal my forecast」を押すとZK証明の生成が始まり、その間はこういうトーストが出ます。

![「Midnight is sealing your forecast…」というトーストが表示され、証明生成中であることを示す画面](/images/midnight_simple_app-5/5.jpg)
*ここでブラウザが `commit_prediction` 回路の証明を生成しています。裏側では前述の witness(`get_selected_team` / `get_prediction_salt`)がローカルの private state から値を読み出しています。*

## リビール：証明してから公開する

締め切り後、参加者は自分の予想を「開示」します。

```compact
export circuit reveal_prediction(): [] {
  assert(phase == MarketPhase.reveal, "Market is not accepting reveals");
  const key = derive_participant_key(local_secret_key());
  const public_key = disclose(key);
  assert(participants.member(public_key), "Participant did not commit");
  assert(!revealed.member(public_key), "Prediction already revealed");

  const team = get_selected_team();
  const salt = get_prediction_salt();
  const stake = stakes.lookup(public_key);
  const expected = make_prediction_commitment(key, team, stake, salt);
  assert(disclose(expected == commitments.lookup(public_key)), "Prediction commitment mismatch");

  if (disclose(team == Team.amber_foxes)) { amber_foxes_pool = (amber_foxes_pool + stake) as Uint<64>; }
  // ... 他チームも同様
  revealed.insert(public_key);
  revealed_count.increment(1);
}
```

ここでやっていることは「コミット時に計算したのと同じハッシュを、witnessから読み直した値でもう一度計算し、台帳上のハッシュと一致することを証明する」だけです。一致すれば、ようやく `if (disclose(team == Team.amber_foxes))` のような比較を通じてチームが公開情報になり、そのチームのプールに賭け金が加算されます。

「開示したチームが、確かにコミット時に自分が選んだチームである」ことをこの照合が保証しています。ブラウザのローカルに保存された `selectedTeam` や `salt` を後から書き換えて、有利なチームに乗り換える、といったズルはこの assert で弾かれます。実際、Vitestのシミュレーターテストにも次のようなケースがあります。

```ts
it("rejects a modified private prediction", () => {
  market.setPrediction("alice", Team.amber_foxes, 100n, 11);
  market.commit("alice", 100n);
  market.closePredictions();
  market.setPrediction("alice", Team.cedar_owls, 100n, 99);
  expect(() => market.reveal("alice")).toThrow();
});
```

コミット後にローカルの選択を`cedar_owls`へ書き換えてから開示させると、ちゃんと弾かれます。これがないと「後出しで有利な方に乗り換える」というプライバシー機構の一番の意味がなくなってしまうので、地味ながら一番大事なテストだと考えています。

開示が進むと、コミット時には見えなかったチームごとの内訳がようやく画面に出てきます。

![開示後のリビール画面。Cedar Owlsが22%、Meadow Bearsが77%として公開されている](/images/midnight_simple_app-5/7.jpg)
*右の「YOUR POSITION」には自分の予想(Cedar Owls・100pt)が「revealed・awaiting the match result」として表示されています。左の一覧も、開示された分だけチーム別の内訳(%とpts)が更新されていきます。*

## 割り算をしないで割り算を検証する

パリミュチュエル方式の報酬計算 `floor(総プール × 賭け金 / 勝ったチームのプール)` は、地味に面倒な部分でした。ZK回路の中で割り算をそのまま書きたくなかったので、この設計では「割り算の結果をクライアント側で計算し、その結果が正しいことだけを回路側で検証する」という形にしています。

```compact
export circuit claim_reward(reward: Uint<64>): [] {
  const public_reward = disclose(reward);
  // ...
  const winning_pool = pool_for(winning_team);
  const payout_numerator = total_pool * stake;
  assert(public_reward * winning_pool <= payout_numerator, "Reward exceeds pari-mutuel entitlement");
  assert((public_reward + 1) * winning_pool > payout_numerator, "Reward is below floor-rounded entitlement");
  assert(total_claimed_rewards + public_reward <= total_pool, "Reward conservation violated");
  rewards.insert(public_key, public_reward);
  claimed.insert(public_key);
  total_claimed_rewards = (total_claimed_rewards + public_reward) as Uint<64>;
}
```

`r = floor(n / p)` であることは、`r × p ≤ n < (r + 1) × p` という不等式に置き換えられます。この2本のassertがまさにそれで、掛け算と比較だけで「フロア除算の結果として正しいか」を判定しています。呼び出し側が都合よく大きい `reward` を渡してきても上の不等式のどちらかで弾かれますし、逆に小さすぎる値を渡しても弾かれます。

最後の `total_claimed_rewards + public_reward <= total_pool` は、勝者全員分の請求を合計してもプールを超えられないようにする保存則のチェックです。端数処理(フロア)で余ったポイントは誰にも配られずプールに残る、という仕様になっています。これも複数勝者がいるケースのテストで確認しています。

マーケットが解決すると、勝ったチームを選んでいた参加者の画面には計算済みの報酬額と「Claim forecast points」ボタンが出てきます。

![マーケット解決後の画面。Estimated rewardが440ptsと表示され、Claim forecast pointsボタンが押せる状態](/images/midnight_simple_app-5/11.jpg)
*100pt賭けていたCedar Owlsの予想が的中し、Estimated rewardは440ptsです。この440という数字はフロントエンドが計算したものにすぎず、実際に台帳へ記録されるのは、この値を引数に `claim_reward` を呼んで上の2本のassertを通過した後です。*

## プライベートステートはブラウザの中にしかない

ここまでのコミットメント照合が成立するには、`selectedTeam` と `salt` がコミット時からリビール時までブラウザ側で保持され続けている必要があります。フロントエンド側の実装はこうなっています(`pkgs/app/src/lib/prediction-market.ts`)。

```ts
export const savePrediction = async (
  providers: PredictionMarketProviders,
  team: Team,
  stake: bigint,
): Promise<void> => {
  const current =
    (await providers.privateStateProvider.get(PredictionMarketPrivateStateId)) ?? initialPrivateState;
  const salt = current.salt ?? crypto.getRandomValues(new Uint8Array(32));
  const next: PredictionMarketPrivateState = { ...current, selectedTeam: team, stake, salt };
  await providers.privateStateProvider.set(PredictionMarketPrivateStateId, next);
};
```

回路を呼ぶ前に、選んだチームとランダムなソルトをまずローカルのプライベートステートストアに保存します。witness の `get_selected_team` や `get_prediction_salt` は、証明生成のタイミングでこのローカルストアから値を読み出すだけです。

裏を返すと、このローカルストアが消えたらもう詰みだということでもあります。README にもそのまま書いた注意書きがこちらです。

:::message alert
コミット後・開示前にブラウザのデータを消したり、別デバイスに乗り換えたりすると、その予想は二度と開示できなくなります。秘密鍵もソルトもサーバー側のどこにもバックアップされていないので、これは仕様であり、UXの課題でもあります。
:::

これは「永続的な匿名性」ではなく「一時的なプライバシー」だと割り切っている部分でもあります。開示は自分の意思で行う操作であり、開示すれば当然そのチームは公開情報になります。マーケットが終わった後まで匿名性を維持する設計にはしていません。

この「ローカルにしかない」感覚は、2つの画面を並べるとわかりやすいです。

![コミット直後、自分のブラウザだけがHarbor Whalesを選んだことを覚えている画面](/images/midnight_simple_app-5/4.jpg)
*コミットした本人のブラウザでは「Forecast: Harbor Whales」がそのまま見えています。これは台帳から読んでいるのではなく、このタブが自分のprivate stateを表示しているだけです。*

![別のブラウザ/ウォレットで解決済みマーケットを開くと、自分の予想は何も保存されていない画面](/images/midnight_simple_app-5/1.jpg)
*同じ解決済みマーケットでも、予想していないブラウザプロフィールで開くと「No personal forecast is stored in this browser profile」としか出ません。台帳にはAmber Foxesの勝利という公開結果しかなく、誰がどのチームを選んでいたかはprivate stateを持つ本人にしかわかりません。*

## ローカル環境を作るときにハマったところ

一番時間を溶かしたのは、証明サーバー(Proof Server)へのアクセス経路の違いでした。

- Preview / PreProd ネットワークでは、Laceウォレットがホストしている証明サーバーをそのまま使えます
- Standalone(Dockerで node / indexer / proof-server をローカルに立てる構成)だと、Laceの拡張機能のService WorkerがブラウザからみたLocalhost(`127.0.0.1:6300`)への直接アクセスをブロックすることがあります

これを回避するために、Standalone構成のときだけViteの同一オリジンプロキシ(`/proof-server` → ローカルの6300番ポート)を経由させています。Preview/PreProdでは逆にこのプロキシを使ってはいけません。Laceが返してくるホスト済みの証明サーバーURLをそのまま使う必要があるからです。ネットワークごとに経路が違うことに気づくまで、しばらく「なぜかStandaloneだけ証明生成が固まる」という現象に悩まされました。

もう一つは、コントラクトアドレスとプライベートステートがネットワークごとに完全に分離されている点です。Standaloneでデプロイしたアドレスは当然Previewでは存在しませんし、逆にPreviewの秘密情報をStandalone側に持ち込んでも意味がありません。当たり前ではあるものの、CLIとブラウザを行き来しながら動作確認しているとうっかり混同しがちでした。

## 実際に動かす

コードだけ眺めても、コミット・リビールの照合が本当に効いているかは分かりにくいものです。手元でシミュレーターテストを動かすのが一番早い方法です。

前提環境:

- Bun 1.2.x
- Compact CLI 0.30.0

```bash
bun install
bun run contract compact   # .compact から回路・証明鍵・ZKIRを生成
bun run test                # コントラクトのシミュレーターテスト
```

手元では以下のように10件すべて通りました。

```text
✓ src/test/prediction-market.test.ts (10 tests) 1142ms

 Test Files  1 passed (1)
      Tests  10 passed (10)
```

この10件には、前述の「ローカル状態を書き換えてから開示すると弾かれる」ケースや、「賭け金の範囲外・重複コミットは拒否される」「勝ったプールが0のチームは結果として選べない」「複数勝者がいてもフロア除算で総配当がプールを超えない」といったケースが含まれています。ブラウザでの動作まで見たい場合は、`bun run build` の後に `bun run dev` でVite開発サーバーを立て、Lace WalletをPreviewネットワークに接続して試すのが一番手っ取り早い方法です。

同梱のヘッドレスCLI(`bun run cli standalone`)の「Show market state」を使うと、同じ4フェーズの遷移をターミナルからも確認できます。

:::details CLIで見るフェーズ遷移(open → reveal → awaiting_result → resolved)
![CLIのShow market state。Phase: open, Participants: 2, Total pool: 560](/images/midnight_simple_app-5/6.jpg)
*コミット直後。2人が参加し、合計560ポイントがプールに入っていますが、チーム別プールはまだすべて0です。*

![CLIのShow market state。Phase: reveal, Revealed: 2, Team pools: cedar=100, meadow=340](/images/midnight_simple_app-5/8.jpg)
*2人とも開示を終えた状態。ここで初めてチーム別プール(cedar=100, meadow=340)が埋まります。*

![CLIのShow market state。Phase: awaiting_result](/images/midnight_simple_app-5/9.jpg)
*運営者が Close reveal を実行し、結果確定待ちのフェーズに入りました。*

![CLIのShow market state。Phase: resolved, Result: cedar_owls](/images/midnight_simple_app-5/10.jpg)
*運営者が Resolve market を実行し、Cedar Owlsの勝利が記録されました。以降は勝者だけが `claim_reward` を呼べます。*
:::

## この設計で守れていないもの

正直に書いておきます。このサンプルは「隠す」ことに寄せた設計であり、「本番の予測市場に必要な要件」はかなり削っています。

- **単一の運営者(Steward)を信頼する構成**になっています。マーケットをデプロイしたウォレットがそのまま結果を確定させる権限を持ちます。外部オラクルや紛争解決の仕組みはありません
- フェーズ遷移は `open → reveal → awaiting_result → resolved` の一方向のみで、**取り消しや巻き戻しができません**。特に「開示が0件のままリビールを締め切る」と、そのマーケットはもう誰も報酬を請求できない状態になり、詰んでしまいます
- 賭けているのは実資産ではなく**デモポイント**で、二次流通市場や許可なしのマーケット作成もサポートしていません

本番でこの手のプライバシー予測市場を作るなら、マルチシグやオプティミスティックオラクルによる結果確定、明示的な締め切り管理、資産カストディの設計、そして外部監査が必要です。今回のスコープは「コミット・リビールとゼロ知識証明の組み合わせを、実際に手を動かして理解する」ところまでにしています。

## まとめ

- 「賭けた金額」と「賭けた対象」を分離し、対象だけをハッシュの中に隠します。これだけでオンチェーン予測市場の「見えすぎ」問題にはかなり効きます
- Compactの `witness` / `disclose()` は、うっかり秘密情報を公開してしまうミスをコンパイラレベルで防いでくれます。ロジックそのもの(コミット・リビール、フロア除算の不等式変換)は言語に関係なく応用が利く考え方です
- プライバシーは「ブラウザのローカルステートが生き残っている」という前提の上に成り立っています。この前提が壊れたときにどうなるかまで含めて設計・説明しておかないと、単に「使いにくいだけの機能」になってしまいます

ソースは全部公開しているので、気になった部分は実際に `bun run test` を回しながら読んでみてください。

## 参考

- [Midnight Network](https://midnight.network/)
- [本記事のリポジトリ(コントラクト・フロントエンド・CLIを含む)](https://github.com/mashharuki/midnight-prediction-market-sample-app)
