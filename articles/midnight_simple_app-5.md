---
title: "予測市場、賭けた瞬間に晒されるのが嫌だったのでゼロ知識証明で隠してみた"
emoji: "🌙"
type: "tech"
topics: ["blockchain", "ゼロ知識証明", "typescript", "react", "web3"]
published: true
publication_name: "midnight"
---

## はじめに

**Polymarket**のような予測市場アプリをみていて、ずっと気になっていたことがあります。

https://polymarket.com/ja

**誰が何に賭けたか、ほぼリアルタイムで丸見えなことです**。

大口が特定の結果に大きく張った瞬間、それを見た他の参加者が同じ方向に追随します。オッズはその追随によって動きます。これは別に不正でも何でもなく、公開型の台帳を使えば当然そうなります。ただ、「自分の予想を先に晒したくない」という素朴な欲求には応えられていないと思います。

じゃあ、投票が締め切られるまで中身を隠しておける予測市場を作れないか。

これを試すために**Midnight**というブロックチェーンを使った `Hidden League Forecast` を作ってみました。

架空のサッカーリーグの勝者を当てるだけのMVPです(ワールドカップ終わっちゃいましたね...)！

:::message
**予測市場とは？**

将来の出来事に関する予測内容を価格として表現する仕組みです！

例えばワールドカップでどこの試合が勝つかなどですね！

予測市場について学びたい方は、以下の資料が大変参考になります！
https://zenn.dev/barabara/books/prediction-markets-structure
:::

Compact というスマートコントラクト用のプログラミング言語でバックエンドを実装しています。

:::message
コミット・リビール方式とゼロ知識証明を組み合わせて「予想の中身は隠したまま、賭け金の集計だけは公開する」を実現しています。
:::

この記事では、コントラクトのコードの中身の解説を交えながら

:::message
今回のアプリではテストネットを使っています！
:::

## 作ってみたアプリのデモ動画

[!['altテキスト'](/images/midnight_simple_app-5/youtube-thumbnail.png)](https://youtu.be/G4T-L-rVgzU)

![Lace Walletに接続し、マーケットのデプロイまたは参加を選ぶトップ画面](/images/midnight_simple_app-5/0.jpg)
*Lace Walletを接続すると、Shielded Addressと残高が表示されます。ここで新規マーケットをデプロイするか、既存のコントラクトアドレスを入力して参加するかを選びます。*

## 全体の流れ

やっていることは非常にシンプルです。

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

:::message
ポイント

ステップ2の時点では「どのチームに賭けたか」がチェーン上のどこにも記録されないことです。記録されるのは「賭け金の額」と「コミットメント(後で照合するためのハッシュ値)」だけです。
:::

ステップ3の開示まで、他の参加者はおろか運営者にも見えません。

## Compactで実装したスマートコントラクト

Midnight の Compact は **「この値は証明の中では使うが、台帳には一切書き込まない」** という変数(witness)を扱える言語です。逆に、台帳に書き込む値は `disclose()` を通すことを強制されます。

「秘密の値をそのままログに残しちゃった」みたいな事故を型レベルで防いでくれます。

秘密鍵、選んだチーム、ソルト(塩)。この3つはすべて witness として定義しています。

```compact
witness local_secret_key(): Bytes<32>;
witness get_selected_team(): Team;
witness get_prediction_salt(): Bytes<32>;
witness store_prediction(team: Team, stake: Uint<64>, salt: Bytes<32>): [];
```

台帳側の変数はこちらです。

```compact
export ledger phase:                 MarketPhase;
export ledger admin_key:             Bytes<32>;
export ledger commitments:           Map<Bytes<32>, Bytes<32>>;
export ledger stakes:                Map<Bytes<32>, Uint<64>>;
export ledger participants:          Set<Bytes<32>>;
export ledger revealed:              Set<Bytes<32>>;
// ... 各チームのプールなど
```

`commitments` に入るのはハッシュ値だけで、`stakes` に入るのは金額だけです。「誰が」「いくら」賭けたかは公開情報ですが「何に」賭けたかはこの時点でまだ存在しません。

## コミット：ハッシュだけを台帳に残す

実際に賭けるときに呼ぶ処理がこちらです。

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

`persistentHash` の第一要素に `"forecast:pick:v1"` という固定文字列を混ぜているのは、ドメイン分離(domain separation)と呼ばれる定石です。同じ入力値でも用途ごとに別のタグを混ぜておけば、別の回路で偶然同じハッシュ値が出て混同する という事故を防げます。参加者キーの導出(`derive_participant_key`)でも `"forecast:participant:v1"` という別のタグを使っています。

:::message
ソルトが必要な理由は、賭け金の範囲が狭いからではありません。`stake`（賭け金）は `commit_prediction` の時点で `stakes` に平文のまま書き込まれるので、外部の観察者にとって賭け金はそもそも推測不要な公開情報です。

本当の弱点は `team` の選択肢が4つしかないことです。ソルトがなければ、観察者は「参加者キー・公開済みの賭け金」を使って team=0〜3 の4通りをそれぞれハッシュ化するだけで、どれが台帳上のコミットメントと一致するか一瞬で特定できてしまいます。ランダムな256bitのソルトを混ぜることで、この4択総当たりを不可能にしています。
:::

実際の画面では、チームと賭け金(Confidence points)を選んでから「Seal my forecast」を押します。

この時点ではチームの内訳(左側の一覧)はまだ動きません。

![チームと賭け金を選び、Seal my forecastを押す直前のコミット画面](/images/midnight_simple_app-5/2.jpg)
*Harbor Whalesに370ポイントを賭けようとしている状態です。左のチーム一覧はまだ「SEALED」表示のみで、内訳は一切公開されていません。*

「Seal my forecast」を押すとZK Proofの生成が始まり、その間はこういうトーストが出ます。

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

これにより「開示したチームが、確かにコミット時に自分が選んだチームである」ことが保証されます。ブラウザのローカルに保存された `selectedTeam` や `salt` を後から書き換えて、有利なチームに乗り換えるといった行為はこの assert で弾かれます。実際、Vitestのシミュレーターテストにも次のようなケースがあります。

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

割り算より前に、実は「そもそもこの人は請求していいのか」を確認する前段があります。省略せずに全部載せます。

```compact
export circuit claim_reward(reward: Uint<64>): [] {
  const public_reward = disclose(reward);
  assert(phase == MarketPhase.resolved && result_set, "Market is not resolved");
  const key = derive_participant_key(local_secret_key());
  const public_key = disclose(key);
  assert(revealed.member(public_key), "Prediction was not revealed");
  assert(!claimed.member(public_key), "Reward already claimed");
  const team = get_selected_team();
  const salt = get_prediction_salt();
  const stake = stakes.lookup(public_key);
  const expected = make_prediction_commitment(key, team, stake, salt);
  assert(disclose(expected == commitments.lookup(public_key)), "Prediction commitment mismatch");
  assert(disclose(team == winning_team), "Prediction did not win");

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

前半の5行は、`reveal_prediction` と同じ「witnessから読み直した値でコミットメントを再計算し、台帳と一致するか確認する」というパターンをもう一度やっています。これにより、他人の `stake` や `team` を騙って請求することはできません。加えて `revealed.member` で「そもそも開示済みか」、`!claimed.member` で「まだ請求していないか」、`team == winning_team` で「勝ったチームを選んでいたか」を確認しています。この4つのassertが揃って初めて、二重請求や他人の当選金の横取りが防がれます。

:::message
`total_pool * stake` のような掛け算はUint<64>同士でも、Compactの型システムが積の値域(`Uint<0..(2^64-1)^2>`)をそのまま保持するため、暗黙に64bit幅へ丸められて桁あふれする心配はありません(手元で `compact compile` して確認済みです)。実際、`Uint<64>` へ明示的に丸め込む箇所だけ `as Uint<64>` キャストが書かれています。
:::

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

裏を返すとこのローカルストアが消えたらもう詰みだということでもあります。README にもそのまま書いた注意書きがこちらです。

:::message alert
今の実装には、複数マーケットを併用する場合の制約もあります。`PredictionMarketPrivateStateId` はネットワーク・ウォレット単位の固定キーで、コントラクトアドレスごとには分かれていません。つまり同じウォレットで2つ目のマーケットに `commit_prediction` すると、その `store_prediction` が1つ目のマーケット用の `selectedTeam` / `salt` を上書きしてしまい、1つ目をリビールできなくなります。

さらに `derive_participant_key` は `local_secret_key()` だけから決まる値なので、同じウォレットであれば `participant_key`(そして自分がデプロイした場合は公開情報である `admin_key` も)は別マーケットでも同じ値になります。単一マーケット内の「誰が何に賭けたか」は隠せていますが、「同じウォレットが複数のマーケットに関わっている」という横のつながりまでは隠せていない、という制約です。1マーケット完結のデモとしては割り切っていますが、複数マーケット運用を想定するなら `privateStateId` をコントラクトアドレスで分ける・鍵導出にマーケット固有の値を混ぜる、といった対応が必要です。
:::

:::message alert
コミット後・開示前にブラウザのデータを消したり、別デバイスに乗り換えたりするとその予想は二度と開示できなくなります。

秘密鍵もソルトもサーバー側のどこにもバックアップされていないのでUXの課題です....
:::

これは「永続的な匿名性」ではなく「一時的なプライバシー」だと割り切っている部分でもあります。開示は自分の意思で行う操作であり、開示すれば当然そのチームは公開情報になります。マーケットが終わった後まで匿名性を維持する設計にはしていません。

この「ローカルにしかない」感覚は、2つの画面を並べるとわかりやすいです。

![コミット直後、自分のブラウザだけがHarbor Whalesを選んだことを覚えている画面](/images/midnight_simple_app-5/4.jpg)
*コミットした本人のブラウザでは「Forecast: Harbor Whales」がそのまま見えています。これは台帳から読んでいるのではなく、このタブが自分のprivate stateを表示しているだけです。*

![別のブラウザ/ウォレットで解決済みマーケットを開くと、自分の予想は何も保存されていない画面](/images/midnight_simple_app-5/1.jpg)
*同じ解決済みマーケットでも、予想していないブラウザプロフィールで開くと「No personal forecast is stored in this browser profile」としか出ません。台帳にはAmber Foxesの勝利という公開結果しかなく、誰がどのチームを選んでいたかはprivate stateを持つ本人にしかわかりません。*

## 実際に動かす

コードだけ眺めてもコミット・リビールの照合が本当に効いているかは分かりにくいと思いますので気になる方は実際に動かしてみましょう！

> **Devcontainer**の設定ファイルを用意したのでぜひそちらを使ってみてください！

前提環境:

- Bun 1.2.x
- Compact CLI 0.30.0

```bash
bun install
bun run contract compact   # .compact から回路・証明鍵・ZKIRを生成
bun run test                # コントラクトのシミュレーターテスト
```

テスト実行結果例

```text
✓ src/test/prediction-market.test.ts (10 tests) 1142ms

 Test Files  1 passed (1)
      Tests  10 passed (10)
```

この10件には、前述の 

- **「ローカル状態を書き換えてから開示すると弾かれる」** 
- **「賭け金の範囲外・重複コミットは拒否される」** 
- **「勝ったプールが0のチームは結果として選べない」** 
- **「複数勝者がいてもフロア除算で総配当がプールを超えない」** 

といったケースが含まれています。

ブラウザでの動作まで見たい場合は、コントラクトをデプロイした後に`bun run build` の後に `bun run dev` でVite開発サーバーを立て、Lace WalletをPreviewネットワークに接続して試すのが一番手っ取り早い方法です！

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

## 注意事項

このアプリは試作品なので外部情報を取り込む部分など本格的な予測市場アプリにするために不足している点が何点かあります。

- **単一の運営者(Steward)を信頼する構成**になっています。マーケットをデプロイしたウォレットがそのまま結果を確定させる権限を持ちます。外部オラクルや紛争解決の仕組みはありません
- フェーズ遷移は `open → reveal → awaiting_result → resolved` の一方向のみで、**取り消しや巻き戻しができません**。特に「開示が0件のままリビールを締め切る」とそのマーケットはもう誰も報酬を請求できない状態になってしまうので今後の改善点です
- 賭けているのは実資産ではなく**このアプリ専用のデモ用のポイント**で、二次流通市場や許可なしのマーケット作成もサポートしていません

本番でこの手のプライバシー予測市場を作るなら、マルチシグやオプティミスティックオラクルによる結果確定、明示的な締め切り管理、資産カストディの設計、そして外部監査が必要です。

今回は学習や検証を目的としているため、「コミット・リビールとゼロ知識証明の組み合わせを、実際に手を動かして理解する」ところまでにしています。

## まとめ

匿名じゃんけんアプリに続いて予測市場アプリもMidnight上で作ってみました！

Midnight専用のAgent SKILLも発表されて、大分開発しやすくなりました！

https://midskills.sevryn.xyz/

皆さんもMidnightを使って何かを実装してみてはいかがでしょうか？

ソースは全部公開しているので、気になった部分は実際に `bun run test` を回しながら読んでみてください！

https://github.com/mashharuki/midnight-prediction-market-sample-app

ここまで読んでいただきありがとうございました！！

## 参考

- [Midnight Network](https://midnight.network/)
- [本記事のリポジトリ(コントラクト・フロントエンド・CLIを含む)](https://github.com/mashharuki/midnight-prediction-market-sample-app)
