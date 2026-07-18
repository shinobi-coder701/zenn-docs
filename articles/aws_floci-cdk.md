---
title: "ローカル環境でもfloci✖️CDK開発を爆速化する！"
emoji: "🧪"
type: "tech"
topics: ["aws", "cdk", "typescript", "floci", "docker"]
published: true
---

学習や設計検証のたびに実AWSへデプロイするのはちょっと抵抗がありますよね...(クレジットとかがあれば別ですが)。

できるならローカルで事前に検証して確実に動くようにしたい...。

そこで、オープンソースのローカルAWSエミュレーター **Floci** とAWS CDKを組み合わせて爆速でローカル環境にて開発と検証のループを回せるか検証してみました！

実際に以下の4つのパターンのシステムを作ってみました。

1. **単一リージョンのフルスタック Todoアプリ**
2. **単一リージョンのBlue/Green Todoアプリ**
3. **マルチリージョン×Blue/Green Todoアプリ**
4. **マルチリージョンKMSキー操作 API**

この記事では動いたところだけでなく、Flociと実AWSの環境切り替えの際にぶつかったところ、そしてその差を埋めるために工夫したことまで紹介します！

:::message
この記事の検証コードと画像は2026年7月時点のリポジトリを基準にしています。

Flociは活発に開発されており、対応サービスや対応APIは変化します。利用時は必ず[公式のServices Overview](https://floci.io/floci/services/)を確認してください。
:::

## この記事で分かること

| 知りたいこと | この記事で扱う内容 |
| --- | --- |
| Flociとは何か | 特徴、起動方法、AWS CLI／SDK／CDKとの接続 |
| どこまで使えるか | 今回確認した範囲と、実AWSで確認を残した範囲 |
| CDKとどう共存させるか | `target=floci\|aws`、環境差分、Outputs、スクリプト化 |
| 複雑な構成も試せるか | Blue/Green、東京／大阪、Global Table相当のアプリ構成 |
| 未対応・未検証機能をどう扱うか | 構成の縮退とProviderパターン |

## Flociとは

Flociは、ローカル環境でAWS互換APIを提供するオープンソースのエミュレーターです。単一のエンドポイント `http://localhost:4566` にAWS CLIやAWS SDKを向けて利用します。最近新しく専用のUIコンソールも追加されました！

https://floci.io/

公式ドキュメントによると、2026年7月12日現在の対応一覧にはS3、SQS、DynamoDB、Lambda、API Gateway、CloudFormation、KMS、CloudFrontなどを含む69サービスが掲載されています。

Flociの実装はJava 25とQuarkus 3.xが中心です。AWSのQuery、JSON 1.1、REST JSON、REST XMLといったワイヤープロトコルを再現するため、専用APIを覚えるのではなく、普段のAWS CLIやSDKをそのまま使えるのが特徴です。

とりあえず動かしてみたいという方は以下のDocker Compose用のyamlファイルを作って起動させれば立ち上がります！

```yaml:compose.yaml
services:
  floci:
    image: floci/floci:latest
    ports:
      - "4566:4566"
```

はい、たったのこれだけです！！

```bash
docker compose up -d

export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_DEFAULT_REGION=us-east-1
# 認証情報はダミー値でOK
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test

aws dynamodb list-tables
```

認証情報は空でなければよく、ローカル検証ではダミー値を使えます。  

## Flociでできること・できないこと

### アプリケーション統合の確認は高速に回せる

- CDKで合成したCloudFormationテンプレートのデプロイ
- S3、API Gateway、Lambda、DynamoDBをまたぐTodo CRUD
- AWS SDK for JavaScript v3を使った実リクエスト
- AWS CLIによるリソースの作成・確認
- Lambdaのコンテナ実行
- 複数スタックの依存関係とCloudFormation Outputsの確認
- CIやローカルで繰り返すsmoke test

実際にTodoアプリを動かすと、Floci本体とは別にLambdaコンテナが起動しました。

![FlociとNode.js Lambdaコンテナが起動しているDocker Desktop画面](/images/aws_floci-cdk/03-floci-lambda-container.png)

### 工夫すれば本番構成の一部も確認できる

- BlueとGreenの2環境を作り、どちらも同じDynamoDBを参照すること
- 東京／大阪×Blue／Greenの4アプリ環境を組み立てること
- 切替先のhealth checkや選択ロジック
- KMSを抽象化したAPIの作成・署名・検証フロー

flociではAWS機能を完全に再現できるわけではないので、**アプリケーション側の構造と制約を確認できた** 程度に考えておくと良いです！

### Flociだけでは保証できないこと

- 実AWSと完全に同じIAM評価や全エラーケース
- CloudFrontの世界中のエッジでの配信特性
- DynamoDB Global Tablesの実際の非同期複製遅延や競合
- KMSが管理する実鍵の保護境界
- 本番のクォータ、性能、可用性、障害特性
- 利用していないAPIアクションの互換性

:::message alert
floci上で動いても実AWSにデプロイしたらIAMポリシーに不足があってうまく動かなかった....、ということがあったので細かい部分で差異がある点は注意が必要です。AWS MCP Serverなどもちゃんと参照させながら設計・実装を進めた方が良いでしょう。
:::

## 検証の出発点はSQSとDynamoDBの最小スタック

いきなりフルスタックへ進まず、最初はSQSキューとDynamoDBのTodoテーブルだけを持つCDKスタックから始めました。

```bash
cd cdk
bun run floci:up
bun run floci:setup
bun run floci:cdk:bootstrap
bun run floci:cdk:deploy
```

その後、AWS CLIでTodoを作成・取得・更新・削除します。すべてのコマンドにエンドポイントを書くと漏れやすいため、実際には `scripts/todo.sh` に固定しました。

```bash
bun run todo create todo-1 "Flociを試す" "DynamoDB CRUDを確認する"
bun run todo get todo-1
bun run todo update todo-1 "Flociを試す" "CRUD確認済み" true
bun run todo delete todo-1
```

**エンドポイント、リージョン、アカウント、認証情報を毎回人間に入力させない** ように専用のスクリプトにラップして使うようにしました。

毎回手動で切り替えていると結構面倒くさいのでこのようにしてしまうのがおすすめです。

## 実験1：単一リージョンのフルスタックTodo

最初のシステムは、React＋Honoで作ったTodoアプリです。

### アーキテクチャ

![単一リージョンのフルスタックTodoのCDKスタック構成図](/images/aws_floci-cdk/01-full-stack-architecture.png)

主な構成要素は次のとおりです。

- React 19＋Viteのフロントエンド
- HonoのHTTP API
- API Gateway REST API
- Node.js 22 Lambda
- DynamoDB `Todos` テーブル
- 静的ファイルを置くS3バケット
- 実AWSだけで作るCloudFrontとCloudWatch Logs

APIは一覧、詳細、作成、部分更新、削除を持ちます。ZodスキーマからOpenAPI 3.1を生成し、さらに `openapi-typescript` でフロントエンド用の型を作りました。

```text
Zod schema
    ↓
OpenAPI 3.1
    ↓
TypeScript API types
    ↓
openapi-fetch client
```

これにより、ローカル開発、Floci、実AWSで同じAPI契約を使えます。

### FlociとAWSの差をCDKへ閉じ込める

このスタックの肝は、環境差をCDK側で吸収した点。アプリケーションコード側には手を入れていません。

```ts
const isAws = props.target === "aws";

const frontendBucket = new s3.Bucket(this, "FrontendBucket", {
  encryption: isAws ? s3.BucketEncryption.S3_MANAGED : undefined,
  enforceSSL: isAws,
  blockPublicAccess: isAws
    ? s3.BlockPublicAccess.BLOCK_ALL
    : new s3.BlockPublicAccess({
        blockPublicAcls: false,
        blockPublicPolicy: false,
        ignorePublicAcls: false,
        restrictPublicBuckets: false,
      }),
  publicReadAccess: !isAws,
});
```

実AWSではprivate S3＋CloudFront OACを使います。一方、このリポジトリのFloci targetではCloudFrontをスタックから外し、S3 REST URLを直接開きます。

```ts
const apiUrl = isAws
  ? api.url
  : `http://localhost:4566/restapis/${api.restApiId}/v1/_user_request_`;
```

### 実際に動かした結果

![Floci上のAPIでTodoを追加したReact画面](/images/aws_floci-cdk/02-full-stack-todo.png)

フロントエンドからTodoを追加するとAPI Gateway→Lambda→DynamoDBを通り、一覧へ反映されました。TanStack Queryの楽観更新と失敗時rollback、DynamoDB条件式による重複作成防止もテストしています。

単に画面が開くだけでなく、次の境界を一度に確認できたのが大きな収穫でした。

- S3にビルド成果物が配置されている
- フロントエンドへ正しいAPI URLが注入されている
- API GatewayのFloci固有実行URLへ到達できる
- LambdaがHonoアプリを実行できる
- LambdaのIAM権限相当でDynamoDBを読み書きできる

## 実験2：単一リージョンのBlue/Green

次は同じTodoをBlue/Green構成へ広げました。

### アーキテクチャ

![DynamoDBを共有するBlue/Green CDKスタック構成図](/images/aws_floci-cdk/04-blue-green-architecture.png)

スタックは4つに分けています。

| スタック | 役割 |
| --- | --- |
| `TodoBgDataStack` | Blue／Greenで共有するDynamoDB |
| `TodoBgBlueStack` | BlueのS3、API Gateway、Lambda |
| `TodoBgGreenStack` | GreenのS3、API Gateway、Lambda |
| `TodoBgRouterStack` | 実AWSでCloudFrontの向き先を選ぶ |

アプリ環境を作る処理は `TodoAppConstruct` にまとめ、色だけをパラメーターとして渡します。BlueとGreenでスタックをコピーしなかったのは、片側だけ設定がずれる事故を避けるためです。

### Flociでは「配信切替」より先に「2環境が健全か」を見る

Floci targetではRouterStackを作らず、BlueとGreenそれぞれのS3 URLとAPI URLをOutputsへ出します。`scripts/switch.sh` は指定色のURLとhealth responseを確認します。

```bash
pnpm switch blue
pnpm switch green
```

![実AWSのCloudFrontをBlueへ向けたTodo画面](/images/aws_floci-cdk/05-blue-environment.png)

![実AWSのCloudFrontをGreenへ切り替えたTodo画面](/images/aws_floci-cdk/06-green-environment.png)

上の2枚は最終的に実AWSのCloudFrontで切り替えたときの画面です。Flociでは同じ2環境へ直接アクセスし、実AWSではCloudFront経由で一方だけを公開する、という役割分担にしました。

ここで重要だったのは、Blueで作ったTodoをGreenから取得できたことです。アプリ環境を分離しながらデータ層は共有する、というBlue/Greenの核心をAWSにデプロイする前にローカルで確認できました。

### 詰まったのは同名のstateful resourceの衝突

単一環境版とBlue/Green版は、どちらも物理テーブル名 `Todos` を使います。同じFlociへ同時にデプロイすると競合しました。

対処は、どちらかをdestroyしてから次をデプロイすることです。ただし、これは長期的には物理名へ環境名を含める、またはCloudFormationに命名を任せる方が安全です。

学習用サンプルでは分かりやすい固定名が便利ですが、複数スタックを同居させた瞬間に弱点になります。

## 実験3：マルチリージョン×Blue/Green

3つ目は、東京と大阪の両方にBlue／Greenを配置する構成です。アプリ環境は合計4つになりました。

### アーキテクチャ

![東京と大阪にBlueとGreenを配置するマルチリージョン構成図](/images/aws_floci-cdk/07-multi-region-architecture.png)

実AWS targetでは次の構成です。

- 東京 `ap-northeast-1`: Blue／Green
- 大阪 `ap-northeast-3`: Blue／Green
- 東京と大阪にレプリカを持つDynamoDB Global Table
- 選択したリージョンと色へ配信するCloudFront
- `ACTIVE_REGION` と `ACTIVE_COLOR` による切替

切替コマンドは、いきなりCloudFrontを更新しません。先に切替候補APIの `/api/health` を呼び、期待するregionとcolorが返った場合だけRouterStackを更新します。

```bash
ACTIVE_REGION=osaka ACTIVE_COLOR=green CONFIRM_AWS_DEPLOY=yes \
  bash scripts/aws-guard.sh switch
```

### FlociではGlobal Tableを単一テーブルへ縮退した

実AWSとFlociでデータ層を分ける。これがこの実験でいちばん大きな設計判断です。

```ts
if (props.target === "aws") {
  new dynamodb.CfnGlobalTable(this, "TodoGlobalTable", {
    tableName: this.tableName,
    billingMode: "PAY_PER_REQUEST",
    streamSpecification: {
      streamViewType: "NEW_AND_OLD_IMAGES",
    },
    replicas: (props.replicaRegions ?? []).map((region) => ({ region })),
  });
} else {
  new dynamodb.Table(this, "TodoTable", {
    tableName: this.tableName,
    partitionKey: { name: "id", type: dynamodb.AttributeType.STRING },
    billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
  });
}
```

Floci targetでは4つのLambdaを同じDynamoDBテーブルへ接続します。これで確認できるのは次の範囲です。

- 4環境が独立したLambda、API Gateway、S3を持つ
- regionとcolorが環境変数を通して正しく返る
- どの環境からも同じTodoを読み書きできる
- 切替スクリプトが正しい環境を選べる

一方、DynamoDB Global Tablesの非同期レプリケーション、競合解決、切替直後の複製遅延は確認できません。

そこは「ローカルで再現できた」とは扱わず、実AWSの統合確認項目として残しました。

![Floci管理画面に4つのLambdaが作成されている様子](/images/aws_floci-cdk/08-floci-four-lambdas.png)

東京Greenから作ったTodoを、大阪Greenからも参照できました。

![東京Green環境でTodoを表示した画面](/images/aws_floci-cdk/09-tokyo-green.png)

![大阪Green環境で同じTodoを表示した画面](/images/aws_floci-cdk/10-osaka-green.png)

これはGlobal Tablesの複製を証明する画像ではありません。Flociでは同じテーブルを共有しているためです。しかし、フロントエンドからバックエンドまで4組を構築し、切替先によらずAPI契約が保たれることは確認できました。

## 実験4：マルチリージョンKMSキーAPI

最後はTodoから離れ、東京のKMS primary keyと大阪のreplica keyで署名・検証するAPIを作りました。

### アーキテクチャ

![東京primaryと大阪replicaを扱うマルチリージョンKMSキーAPI構成図](/images/aws_floci-cdk/11-multiregion-key-architecture.png)

APIは次の操作を持ちます。

- key setの作成・一覧・詳細
- key setの削除予約
- 東京または大阪のキーによる署名
- 東京または大阪のキーによる検証

実AWS targetでは `ECC_NIST_P256` と `ECDSA_SHA_256` を使うKMS Multi-Region Keyを作成します。API GatewayにはAPI KeyとUsage Planを設定し、Lambdaには必要なKMS actionだけを許可します。

### KMSを無理に模倣せず、Providerを切り替えた

このリポジトリではFloci targetでKMSリソースを作らず、Node.js `crypto` を使う `LocalKmsProvider` を選びます。

```ts
const keyProvider =
  process.env.KMS_PROVIDER === "aws"
    ? new AwsKmsProvider(primaryRegion, replicaRegion)
    : new LocalKmsProvider(primaryRegion, replicaRegion);
```

ローカルProviderはP-256の鍵ペアを生成し、東京と大阪を表す2つの論理IDに同じ鍵素材を関連付けます。

```ts
const { privateKey, publicKey } = generateKeyPairSync("ec", {
  namedCurve: "prime256v1",
});

return sign("sha256", input.message, {
  key: createPrivateKey(input.keySet.localPrivateKeyPem),
  dsaEncoding: "der",
});
```

この方法で、APIの入力検証、DynamoDBへのメタデータ保存、署名・検証、エラー形式、東京／大阪の選択をローカル確認できます。

ただし、これはKMSの互換実装ではありません。実AWS KMSが持つ鍵素材の非エクスポート性、キーポリシー、CloudTrail、削除待機期間、サービス側のエラー挙動までは再現しません。

:::message
実際、最初flociで正常動作したCDKスタックを実AWSにデプロイしたらポリシーエラーが発生しました。
:::

なお、2026年7月現在のFloci公式一覧にはKMSも掲載されています。今後このサンプルを更新するなら、FlociのKMSで必要な `CreateKey`、`ReplicateKey`、`Sign`、`Verify` がどこまで対応するかを操作単位で確認し、Local Providerとの比較テストを追加したいところです。

## FlociとCDKを併用して詰まったところ

4システムを通して、同じ問題に何度か形を変えて遭遇しました。

### 1. CDK bootstrapが「アプリで使わないAWSサービス」を要求する

CDKの標準bootstrapテンプレートは、アセット管理用のECRなどを含みます。アプリ本体では使わなくても、ローカルエミュレーター側の対応状況によってbootstrapで止まる可能性があります。

そこで、リポジトリでは `bootstrap-no-ecr.yaml` を用意し、Floci用ラッパーから明示的に渡しました。

```bash
npx cdk bootstrap \
  -c target=floci \
  --template "$SCRIPT_DIR/bootstrap-no-ecr.yaml"
```

CDKをローカルエミュレーターへ向けるときは、**自分のスタックだけでなくbootstrap stackも検証対象**になります。

また、認証情報を環境変数に詰める部分もflociと実AWSで毎回切り替える必要があるため、この辺りもまとめてスクリプトにしてラップしてしまいました。

### 2. API GatewayのURLが実AWSと異なる

実AWSなら `https://{api-id}.execute-api...` ですが、今回使ったFlociのAPI実行URLは次の形でした。

```text
http://localhost:4566/restapis/{api-id}/v1/_user_request_/
```

URLをコードやREADMEへ手書きせず、CDK Outputから取り出すようにしました。これでAPI IDが変わってもデプロイスクリプトを直さずに済みます。

### 3. S3はdestroy前に空にする必要がある

フロントエンドを配置したS3バケットは、中身があるままでは削除できません。Floci用destroyでは先にバケットを列挙して空にし、続いてCDK stackを削除する順序にしました。

複雑な構成になるほど難しいのは、作成より削除の順序。マルチリージョン版ではRouter→4アプリ→データ層の順序も固定しました。

## FlociとCDKを併用する上で工夫したこと

### `target=floci|aws` をCDKの入口にする

各CDKアプリはcontextからtargetを受け取り、環境を決めます。

```ts
const target = app.node.tryGetContext("target") === "aws" ? "aws" : "floci";

const env =
  target === "floci"
    ? { account: "000000000000", region: "us-east-1" }
    : {
        account: process.env.CDK_DEFAULT_ACCOUNT,
        region: "ap-northeast-1",
      };
```

環境変数をあちこちで参照するのではなく、CDKの入口でtargetを確定します。Constructへは `target` を明示的に渡すため、どの条件分岐が環境差なのか追いやすくなりました。

### 「共通部分」と「AWSでしか検証しない部分」を分ける

今回の基本方針は次のとおりです。

| 共通 | 実AWS target | Floci target |
| --- | --- | --- |
| API契約、Hono、React、DynamoDB repository | CloudFront、OAC、Global Table、KMS | 直接URL、単一テーブル、Local Provider |

アプリケーションコードをforkせず、インフラとProviderで差を吸収しました。この境界が曖昧だと、「ローカルでは動く専用アプリ」が出来上がってしまいます。

### デプロイを一つの検証パイプラインにする

`deploy:floci` はCDK deployだけを意味しません。

```text
契約生成
  → format / lint / typecheck / test / build
  → CDK deploy
  → frontend build
  → S3 sync
  → smoke test
```

デプロイが成功してもAPIが動くとは限りません。最後にHTTPリクエストまで流すことで、「CloudFormationが成功した」より一段強い確認にしました。

### 実AWS操作にガードを付ける

AWS targetのdeploy／destroyには、次の2つを要求しました。

- STSで取得したaccount IDとの一致
- `CONFIRM_AWS_DEPLOY=yes` の明示

さらに、通常の品質確認は `synth:aws` と `diff:aws` までに留めます。ローカル開発の勢いで実AWSへdeployしないための仕組みです。

### テストで「作るもの」だけでなく「作らないもの」も確認する

Floci targetのCDKテストでは、CloudFront Distributionが0件であることを検証しています。AWS targetではprivate S3、OAC、CloudFront、`/api/*` behaviorが存在することを検証します。

```ts
template.resourceCountIs("AWS::CloudFront::Distribution", 0);
```

条件付きインフラでは、存在確認だけでなく**不在の確認**が重要でした。

## 4システムを通して分かったFlociの使いどころ

| 用途 | 所感 | 理由 |
| --- | --- | --- |
| **CDK学習** | とても相性がよい | 作成・破棄を繰り返しやすい |
| **API統合テスト** | 相性がよい | AWS CLI／SDKを同じ形で使える |
| **サーバーレス構成検証** | 相性がよい | API Gateway→Lambda→DynamoDBを通せる |
| **複数環境の構成確認** | 工夫すれば有効 | Blue／Greenや4環境を組み立てられる |
| **エッジ配信特性** | 実AWS確認が必要 | 世界中のCloudFront挙動はローカルで保証できない |
| **マルチリージョン整合性** | 実AWS確認が必要 | 非同期複製と競合は単一テーブルでは再現できない |
| **性能・可用性試験** | 対象外 | エミュレーターと本番基盤は性質が異なる |

## まとめ

FlociとCDKを使い、SQSとDynamoDBの小さなスタックから始めて、単一リージョンのフルスタック、Blue/Green、マルチリージョン×Blue/Green、マルチリージョンKMSキーAPIまで進めました。

特に学びになったのは、次の3点です。

1. **環境差はアプリではなくCDKとProviderへ閉じ込める**
2. **flociとCDKを併用する場合は環境毎の差異やデプロイ先の切り替えをスクリプトにラップする**
3. **deployをsmoke testまで含むパイプラインとして扱う**

Flociだけですべてを証明しようとすると無理が出ます。しかし、FlociでAPI契約、AWS SDK、Lambda、DynamoDB、複数スタック、切替ロジックを高速に確認できれば、実AWSで試す回数を大きく減らせます。

最初は「ローカルAWSでどこまで複雑な構成を作れるだろう」という興味から始めました。最後に残った答えは、対応サービスの数よりも、**どこまでをローカルで証明し、どこからを本番相当環境へ渡すかを設計できることの方が大切**、というものでした。

コード全体はこのリポジトリの各READMEとCDKスタックから確認できます。まずは `cdk/` のSQS＋DynamoDBから試し、次に `full-stack-serverless/` へ進むのがおすすめです！

ここまで読んでいただきありがとうございました！！

## 参考資料

- [Floci公式サイト](https://floci.io/floci/)
- [Floci Services Overview](https://floci.io/floci/services/)
- [floci-io/floci](https://github.com/floci-io/floci)
- [AWS CDK Developer Guide](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- [DynamoDB Global Tables](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html)
- [AWS KMS Multi-Region keys](https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html)
- [Deepwiki - Flociの概要](https://deepwiki.com/search/floci-localstock_5f721375-3cc3-411e-8a20-8eb7f5eb7fa9)