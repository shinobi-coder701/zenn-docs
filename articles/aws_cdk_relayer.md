---
title: "AWS CDKでメタトランザクション用サーバーレスAPIを実装してみた！"
emoji: "🦜"
type: "tech"
topics: ["AWS", "CDK", "Web3", "Blockchain", "TypeScript"]
published: true
---

![](/images/aws_cdk_relayer/0.png)

## はじめに

2024 年 9 月 21 日〜22 日にかけて開催されている **ServerlessDays Tokyo 2024** に参加して触発されてこの記事を執筆しました！！

https://serverless.connpass.com/event/325659/

**サーバーレスこそ至高！！！！**

そんな思いが芽生えてきました・・！！

今回は AWS と Web3 両方の技術スタックにまたがる記事となっています！！

ぜひ最後まで読んでいってください！！

## 関連用語解説

### AWS CDK

AWS CDK は、 **CloudFormation** を 1 段階抽象化させた IasC のツールです！！

https://aws.amazon.com/jp/cdk/

https://aws.amazon.com/jp/cloudformation/

**CloudFormation** や **SAM** では yaml ファイルでインフラリソースを定義する必要がありますが、 AWS CDK では TypeScript でも実装できます。

普段のプログラミングの感覚で AWS リソースを定義することができます！！

慣れるまでが大変ですが、一度使い方を覚えたら強い味方になります！！

スタックの展開・削除がコマンド一つで行えるため、非常に便利です！s

今回フロントやスマートコントラクト開発でも一部 TypeScript を使っていたので CDK を採用することによりプログラミング言語を統一させることができました。

### メタトランザクション

メタトランザクションは、ユーザーの UX を向上させるために編み出された技術です。

https://zenn.dev/web3developer/articles/8ba305ee63e715

Account Abstraction が登場するまではよく取り上げられていました。

通常、ブロックチェーン上のスマートコントラクトの書き込み系メソッドを呼び出すためには、エンドユーザーがガス代を支払ってトランザクションをブロックチェーンに送信する必要があります。

これだとユーザーは必ずガス代を事前に用意しなければいけないのでアダプションの妨げとされていました。

そこでトランザクションの署名まではエンドユーザー側で行い、ガス代が発生するトランザクションへの送信はバックエンド側に用意した EOA(リレイヤー) に肩代わりさせてしまえということで登場したのがメタトランザクションです。

## 今回実装したもの

個人で **XeneaDomainNameService** という Web3 アプリケーションを実装したのですが、メタトランザクションを実現させるためサーバーレス API を実装しました。

https://app.akindo.io/communities/ENp28mgxOh61kQBZ/products/4eBLmzqVafMg3W6a

**Xenea** というブロックチェーン上に展開している Dapp で、ENS のようにウォレットアドレスと任意の文字列の名前解決を行うものです！！

https://xenea.io/

フロントエンドは Next.js、スマートコントラクトは hardhat を使って実装しました。

そしてガスレストランザクションを実装するために API を用意する必要があったのですが、それを AWS 上に構築していました。

プロダクトの概要をまとめたスライドは以下になります！

https://www.canva.com/design/DAGOKu_d4FI/6XFr8Tb8HMvn23D6HDQ-eg/view

この中にシステム概要図があるので抜粋して紹介させていただくと

- **フロントエンド**
- **スマートコントラクト**
- **サーバーレス API**

という三つの要素から構成されているアプリになります。

![](/images/aws_cdk_relayer/1.png)

Live Demo は以下の通りです。

https://cdn-nextjs.vercel.app/

デモビデオは以下で視聴できます。

このデモでは、任意の文字列とウォレットアドレスを紐付けるための NFT を発行しているのですが、発行の際エンドユーザーはガス代を支払っていません。

それはメタトランザクションを実装しているためです。

https://youtu.be/bgzzNEvl8A4

## AWS CDK でメタトランザクション用のサーバーレス API を実装しようと思った動機

**XeneaDomainNameService** は、短期間のハッカソンを何回も繰り返す **WaveHack** で実装しました。

**WaveHack** って何？？ という方は以下の記事をご覧ください。

https://note.com/shinkinjo/n/n313d1e931ebf

**Xenea** は新興のブロックチェーンで Ethereum のようにインフラプロバイダーのサポートが手厚い状況ではありませんでした。

ユーザー体験を向上させるため、メタトランザクションを実装しようと試みたのですが、よくお世話になる OpenZeppelin Defender の対象外チェーンとなっていました・・・。

https://defender.openzeppelin.com/#/auth/sign-in?returnTo=%2F

メタトランザクション実装のためにはバックエンド用の EOA(リレイヤー)を用意する必要があるのですがそのためには秘密鍵を管理する必要があります。

Defender が使えない場合は以下のどちらかの手段を取ることになります。

**1. Next.js の `api` 配下にロジックを実装する。**
**2. 自分でリレイヤー用の API サーバーを実装する。**

1 の場合だと Next.js のプロジェクトで完結させることができますが、環境変数として秘密鍵を埋め込むことになります。

セキュリティ的にちょっと不安だったので今回は 2 の方法で実装することにしました。

個人開発で API を立てる・・・・ 、　ちょっとハードル高いな・・・。

**そうだ！！ AWS 上にサーバーレス API を実装しよう！！**

ということで AWS CDK を使ってサーバーレス API を実装してみました！！

この後コードの解説に移っていきます！！

## コードの解説

今回のコードは以下に格納されています！！

https://github.com/mashharuki/CDN

このソースコードは、ブロックチェーンアプリケーション開発用のテンプレートプロジェクトである **Scaffold-ETH-2** をベースにして作っています！！

https://github.com/scaffold-eth/scaffold-eth-2

**Scaffold-ETH2** を管理しているは **BuidlGuidl** になります！！

https://buidlguidl.com/

パッケージ管理ツールは `yarn` を使っており、モノレポ構成となっています！

```bash
.
├── CONTRIBUTING.md
├── LICENCE
├── README.md
├── docs
├── node_modules
├── package.json
├── packages
|     ├── cdk       サーバーレスAPI用
|     ├── hardhat   スマートコントラクト用
|     └── nextjs    フロント用
└── yarn.lock
```

今回は、 `cdk` ディレクトリ用フォルダの中身をメインに解説していきます。

`cdk` ディレクトリの中身は以下のようになっています。

ポイントになるのは、 `resources` ディレクトリ配下のものです。
ここに サーバーレス API のロジックの中身が実装されています。

```bash
.
├── README.md
├── bin
├── cdk.context.json
├── cdk.json
├── cdk.out
├── data
├── jest.config.js
├── lib
├── node_modules
├── package.json
├── resources       Lambda用のコードを格納。
├── test
└── tsconfig.json
```

`resources` ディレクトリの配下は以下の通りとなっています。

```bash
.
└── lambda
    ├── index.ts          メインファイル
    ├── lib
    │   └── relayer.ts    リレイヤー関連の実装をまとめたファイル
    └── util
        ├── abi.ts        forwarderコントラクトのABIファイル
        └── constants.ts  諸々の定数をまとめたファイル
```

では一つ一つのファイルを見ていきたいと思います。

- **index.ts**

  このファイルはリクエストの受付、レスポンスの送信を担当しているファイルです。

  実際にメタトランザクション用の処理を実行するのは `requestRelayer` メソッド内部です。

  ```ts
  import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";
  import { requestRelayer } from "./lib/relayer";

  /**
   * ハンドラー
   * @param event
   * @returns
   */
  export const handler = async (
    event: APIGatewayProxyEvent
  ): Promise<APIGatewayProxyResult> => {
    console.log("Received event:", JSON.stringify(event, null, 2));

    // リクエストのボディを取得
    const requestBody = JSON.parse(event.body || "{}");

    // meta txを送信するメソッド実行する
    const result = await requestRelayer(requestBody);

    let response;

    // レスポンスの構築
    if (result != null) {
      response = {
        statusCode: 200,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
        body: JSON.stringify({
          message: "send meta tx success.",
          txHash: result,
        }),
      };
    } else {
      response = {
        statusCode: 500,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
        body: JSON.stringify({
          message: "send meta tx failed.",
        }),
      };
    }

    console.log("response:", response);

    return response;
  };
  ```

- **relayer.ts**

  このファイルがロジックの肝の部分です。

  リレイヤー用の Signer インスタンスを生成し、そこをトランザクション発行元として Forwarder コントラクトの `execute` メソッドを呼び出しています。

  ここからメタトランザクションが送信され問題なく処理されればガスレスで処理を行うことができるわけです！！

  ```ts
  import { Contract, ethers } from "ethers";
  import { SAMPLEFORWARDER_ABI } from "./../util/abi";
  import { RPC_URL, SAMPLEFORWARDER_ADDRESS } from "./../util/constants";

  // 環境変数を取得する。
  const { RELAYER_PRIVATE_KEY } = process.env;

  /**
   * リクエストをブロックチェーンに送信するメソッド
   */
  export const requestRelayer = async (request: any) => {
    console.log(
      " ========================================= [RequestRaler: START] =============================================="
    );
    // プロバイダーを作成
    const provider = new ethers.JsonRpcProvider(RPC_URL);

    // get relayer
    const relayer = new ethers.Wallet(RELAYER_PRIVATE_KEY!, provider);
    // create forwarder contract instance
    const forwarder: any = new Contract(
      SAMPLEFORWARDER_ADDRESS,
      SAMPLEFORWARDER_ABI,
      relayer
    ) as any;

    console.log("relayer:", relayer.address);

    let result;

    try {
      console.log("request:", request);
      // call verify method
      const verifyResult = await forwarder
        .connect(relayer)
        .verify(request.request);
      console.log("verify result: ", verifyResult);
      if (!verifyResult) throw "invalid request data!";

      // call execute method from relayer
      const tx = await forwarder.connect(relayer).execute(request.request, {
        value: request.request.value,
        gas: 90000000,
      });
      // await tx.wait();

      console.log("tx.hash:", tx.hash);
      result = tx.hash;
    } catch (error) {
      console.error("Error requestRelayer :", error);
    } finally {
      console.log(
        " ========================================= [RequestRaler: END] =============================================="
      );
      return result;
    }
  };
  ```

  思ったよりもシンプルに実装できました！！

  RELAYER_PRIVATE_KEY には秘密鍵が埋め込まれるので環境変数からとってくるようにしています。

  今回は **Sytems Manager Parameter Store** 上に保管してそこから取得してくるような実装としました！

  これで少しだけセキュアな作りになっているはず・・・。

---

Lambda 側の実装の解説はここまでです。

では次にスタックを定義しているファイルを確認していきたいと思います。

今回サーバーレス API の実装に使ったサービスは以下の 3 つです！！！

- **API Gateway**
- **Lambda**
- **Sytems Manager Parameter Store**

ブロックチェーンを使っているので **Aurora RDS** や **DynamoDB** は使っていません！！

必要なスタックの定義は次の通りです！！

```ts
import * as cdk from "aws-cdk-lib";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as lambda from "aws-cdk-lib/aws-lambda";
import { NodejsFunction } from "aws-cdk-lib/aws-lambda-nodejs";
import * as ssm from "aws-cdk-lib/aws-ssm";
import { Construct } from "constructs";
import path = require("path");

/**
 * Relayerに関するスタック
 */
export class RelayerStack extends cdk.Stack {
  // グローバル変数群
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Sytems Manager Parameter Storeから環境変数を取得する。
    const RELAYER_PRIVATE_KEY = ssm.StringParameter.valueFromLookup(
      this,
      "RELAYER_PRIVATE_KEY"
    );

    // Lambda関数を定義
    const lambdaFunction = new NodejsFunction(this, "RelayerLambdaFunction", {
      runtime: lambda.Runtime.NODEJS_18_X,
      entry: path.join(__dirname, "../resources/lambda/index.ts"),
      handler: "handler",
      bundling: {
        forceDockerBundling: true,
      },
      timeout: cdk.Duration.seconds(600),
      environment: {
        RELAYER_PRIVATE_KEY: RELAYER_PRIVATE_KEY, // 環境変数として渡す
      },
    });

    // API Gateway Rest APIを作成
    const api = new apigateway.RestApi(this, "RelayerPublicApi", {
      restApiName: "relayer",
      description: "This RelayerPublicApi serves my Lambda function.",
    });

    // Lambda Integration
    const postLambdaIntegration = new apigateway.LambdaIntegration(
      lambdaFunction,
      {
        requestTemplates: {
          "application/json": '{ "statusCode": "200" }',
        },
        integrationResponses: [
          {
            statusCode: "200",
            responseParameters: {
              "method.response.header.Access-Control-Allow-Origin": "'*'",
            },
          },
        ],
      }
    );

    // APIキーを作成
    const apiKey = api.addApiKey("ApiKey");

    // APIキーを使用するUsagePlanを作成
    const plan = api.addUsagePlan("UsagePlan", {
      name: "Easy",
      throttle: {
        rateLimit: 10,
        burstLimit: 2,
      },
    });

    // APIのリソースとメソッドを定義
    const items = api.root.addResource("relayer");
    // CORSの設定を追加
    items.addCorsPreflight({
      allowOrigins: apigateway.Cors.ALL_ORIGINS,
      allowMethods: ["POST", "OPTIONS"],
      allowHeaders: [
        "Content-Type",
        "X-Amz-Date",
        "Authorization",
        "X-Api-Key",
        "X-Amz-Security-Token",
      ],
    });

    const postMethod = items.addMethod("POST", postLambdaIntegration, {
      apiKeyRequired: true,
      methodResponses: [
        {
          statusCode: "200",
          responseParameters: {
            "method.response.header.Access-Control-Allow-Origin": true,
          },
        },
      ],
    });

    // UsagePlanにメソッドを追加
    plan.addApiStage({
      stage: api.deploymentStage,
      throttle: [
        {
          method: postMethod,
          throttle: {
            rateLimit: 10,
            burstLimit: 2,
          },
        },
      ],
    });
    // UsagePlanにAPIキーを追加
    plan.addApiKey(apiKey);

    // 成果物
    new cdk.CfnOutput(this, "RelayerApiUrl", {
      value: api.url,
      description: "The URL of the API Gateway",
      exportName: "RelayerApiUrl",
    });

    new cdk.CfnOutput(this, "RelayerLambdaFunctionArn", {
      value: lambdaFunction.functionArn,
      description: "The ARN of the Lambda function",
      exportName: "RelayerLambdaFunctionArn",
    });
  }
}
```

これだけです！！

サーバーレスなリレイヤー用のスタックを定義するだけだとこれだけで済みました！！

CDK を使っているのでスタックの展開・削除はともにコマンド一つで済みます！！

- **展開用のコマンド**

  ```bash
  yarn cdk deploy '*'
  ```

- **削除用のコマンド**

  ```bash
  yarn cdk destroy '*'
  ```

---

フロント側での呼び出しですが、通常の API を呼び出すのと同じように API エンドポイントと API キー、引数を渡してあげれば処理を呼び出せます！！

下記のコードは実際にこのサーバーレス API を呼び出している部分の実装です！！

```ts
/**
 * register
 */
const register = async () => {
  try {
    console.log("address:", address);
    console.log("deployedContractData.address:", deployedContractData.address);

    // create Contract object
    const domains: any = new Contract(
      deployedContractData.address,
      deployedContractData.abi,
      signer
    ) as any;
    const forwarder: any = new Contract(
      SampleForwarderContractData.address,
      SampleForwarderContractData.abi,
      signer
    ) as any;
    // generate encoded data
    const data = domains.interface.encodeFunctionData("register", [
      address,
      domain,
      years,
    ]);
    // get EIP712 domain
    const eip721Domain = await forwarder.eip712Domain();
    const provider = new ethers.JsonRpcProvider(RPC_URL);
    // get current block
    const currentBlock = await provider.getBlock("latest");
    const currentTime = currentBlock!.timestamp;
    // get deadline
    const uint48Time = await getUint48(currentTime);
    console.log("getUint48:", uint48Time);

    // creat metaTx request data
    const signature = await signer!.signTypedData(
      {
        name: eip721Domain.name,
        version: eip721Domain.version,
        chainId: eip721Domain.chainId,
        verifyingContract: eip721Domain.verifyingContract,
      },
      {
        ForwardRequest: ForwardRequest,
      },
      {
        from: address,
        to: domains.target,
        value: price.toString(),
        gas: 9000000,
        nonce: await forwarder.nonces(address),
        deadline: uint48Time,
        data: data,
      }
    );

    console.log("signature:", signature);

    // call execute method from relayer
    await POST({
      request: {
        from: address,
        to: domains.target,
        value: price.toString(),
        gas: 9000000,
        //nonce: await forwarder.nonces(address),
        deadline: uint48Time.toString(),
        data: data,
        signature: signature,
      },
    }).then(async (result) => {
      // APIリクエストのリザルトをJSONとして解析
      console.log("API response:", result);
      setTxHash(result.body.txHash);

      toast.success("🦄 Success!", {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
    });
  } catch (err: any) {
    console.error("err:", err);
    toast.error("Failed....", {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "colored",
    });
  }
};
```

`POST` メソッドを呼び出していますが、そこで実際に API へのリクエストを投げています。

`POST`メソッドの中身は次のとおりです。

```ts
import { BASE_API_URL } from "~~/utils/constants";

const API_KEY = process.env.NEXT_PUBLIC_API_KEY;

/**
 * requestRelayer API
 * @param requestData
 */
export async function POST(requestData: any) {
  console.log("request:", requestData?.request);

  if (requestData?.request === undefined) {
    return new Response("Request has no request", {
      status: 503,
    });
  }

  const response = await fetch(`${BASE_API_URL}/relayer`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": API_KEY!,
    },
    body: JSON.stringify({
      request: requestData.request,
    }),
  });

  console.log("response:", response);

  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }

  const data = await response.json();

  console.log("responseData:", data);

  return {
    status: 200,
    body: data,
  } as any;
}
```

コードの解説はここまでになります。

## まとめ

いかがでしたでしょうか。

本当は **SecretManager** や **KMS** なんかを使った方がよりセキュアにできますが、今回は **Systems Manager Parameter Store** を採用しました。

個人開発で作ったものなのでまだまだ甘いところがありますが、今後勉強していってもっとよいサーバーレス API を実装できるようになりたいと思います！！

ここまで読んでいただきありがとうございました！！

## 参考文献

1. [GitHub - CDN](https://github.com/mashharuki/CDN)
2. [Akindo - XeneaDomainNameService Product Page](https://app.akindo.io/communities/ENp28mgxOh61kQBZ/products/4eBLmzqVafMg3W6a)
3. [AWS CDK サイト](https://aws.amazon.com/jp/cdk/)
4. [Buidl Guidl 公式サイト](https://buidlguidl.com/)
5. [GitHub - scaffold-eth-2](https://github.com/scaffold-eth/scaffold-eth-2)
6. [OpenZeppelin Defender](https://defender.openzeppelin.com/#/auth/sign-in?returnTo=%2F)
7. [Note - WaveHack 1st season 総括記事](https://note.com/shinkinjo/n/n313d1e931ebf)
8. [Xenea 公式サイト](https://xenea.io/)
9. [ServerlessDays Tokyo 2024](https://serverless.connpass.com/event/325659/)
