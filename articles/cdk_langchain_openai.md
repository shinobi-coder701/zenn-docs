---
title: "CDKとLangChainとOpenAI APIで簡易RAGを実装してみた！"
emoji: "🚀"
type: "tech" 
topics: ["OpenAI","RAG","CDK","生成AI","LangChain"]
published: true
---

![](/images/cdk_langchain_openai/0.png)

## はじめに

皆さん、こんにちは！

9月中旬〜10月初旬まで開催されていた **Solana** の大型ハッカソン **Radar Hackathon** に参加しました。

その時に **CDK** と **LangChain** と **Open AI API** を使って **MagicBlock** というプロトコルに関する4択の問題と回答を自動で生成してくれる簡易 RAG を実装してみましたのでその内容を共有したいと思います！

https://www.colosseum.org/radar

僕は、 [Yukiさん](https://twitter.com/stand_english)にお声がけいただいて AW系のゲームである **Q-drop Adventure** というプロダクトの開発をご一緒させていただきました！！

![](/images/36322bab97af38/1.png)

Live demoは以下で公開されています！！
ぜひ触ってみてください！！

https://qdropadventure.vercel.app/

---

## LangChainとは

LangChain は、複数のLLM（大規模言語モデル）やツールを組み合わせて、より複雑で高度なLLMアプリケーションを作成するためのフレームワークです。

https://www.langchain.com/

LangChainを使えばコード量も大幅に減りますし複雑な処理も実装しやすくなります！

例えば以下のようなことができるようになります！！

- **ツールの連携:**     
  LangChainは外部APIやデータベースと連携し、質問に対して動的にデータを取得して回答できるようにします。

- **メモリ:**     
  会話の履歴を保持し、文脈に基づいた応答が可能です。

- **プロンプト管理:**     
  複数のプロンプトを効果的に扱い、複雑なタスクをこなせるようにします。


AIエージェントやRAGを実装する時にお世話になる確率が非常に高いです！！

今回はOpenAI APIと組み合わせて使いましたが、 AWS の **Amazon Bedrock** 用の機能も用意されたりしていてクラウドサービスとの相性も非常に良いです！！

## RAG(検索拡張生成) とは

RAGは、LLMが外部データを使用して、より正確で信頼性のある情報を生成するためのアプローチです。

もっと簡単にいうと、 外部データを利用してLLMの生成能力を強化する技術ですね。

https://aws.amazon.com/jp/what-is/retrieval-augmented-generation/

通常、LLMは学習時に取り込んだデータのみを基に回答しますが、そのデータが古かったり限定的だったりする場合、正確な答えを出すことが難しくなります。

RAGは以下の2つのステップで動作します。

- **Retrieval (情報の取得):**   
  質問に関連する外部データ（例えばドキュメントやデータベース）を検索して取得します。

- **Generation (生成):**   
  取得したデータをもとに、LLMが回答を生成します。

この方法により、最新かつ正確な情報をもとにした回答が生成できるため、特定のドメインや最新情報が重要なアプリケーションで使われます。

---

## 今回の実装

今回実装したソースコードは以下のGitHubリポジトリの`cdk`ディレクトリに含まれています。

https://github.com/ytakahashi2020/airdrop_quest/tree/main

今回解説する部分のアーキテクチャですが、以下のようになっています！  

![](/images/cdk_langchain_openai/1.png)

RAGで使うマークダウンファイルはS3バケットに保管しています。

Lambda関数からOpen AI APIを呼び出し、S3バケット内のマークダウンを使ってRAGを実装しています！

Lambda関数の実装は以下の通りです。

マークダウンファイルの内容を追加で読み込ませて **MagicBlock** に関する問題を出力させるようにしています！！

```ts
import { HNSWLib } from "@langchain/community/vectorstores/hnswlib";
import { Document } from "@langchain/core/documents";
import { StringOutputParser } from "@langchain/core/output_parsers";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import {
  RunnableLambda,
  RunnableMap,
  RunnablePassthrough,
} from "@langchain/core/runnables";
import { ChatOpenAI, OpenAIEmbeddings } from "@langchain/openai";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";
import { getS3Object } from "./helper/s3";

// 環境変数を取得する。
const {OPENAI_API_KEY} = process.env;

/**
 * ハンドラー
 * @param event
 * @returns
 */
export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  
  console.log(`
    ================================ [Generate Quiz API START] ================================
  `);

  // S3バケット名を指定
  const bucketName = 'solana-radar-hackathon2024'; 
  // ファイル名を指定
  const objectKey = 'MagicBlock.md'; 
  // S3バケットからオブジェクトを取得する。
  const content = await getS3Object(bucketName, objectKey);
  // ベクトルデータストアを作成
  const vectorStore = await HNSWLib.fromDocuments(
    [new Document({pageContent: content})],
    new OpenAIEmbeddings()
  );

  const retriever = vectorStore.asRetriever(1);
  // テンプレートプロンプト
  const prompt = ChatPromptTemplate.fromMessages([
    [
      "ai",
      `Please create simple question based on only the following context:
        
      {context}`,
    ],
    ["human", "{question}"],
  ]);

  // ChatOpenAIインスタンスを生成
  const model = new ChatOpenAI({
    apiKey: OPENAI_API_KEY!,
  });
  const outputParser = new StringOutputParser();
  // セットアップ
  const setupAndRetrieval = RunnableMap.from({
    context: new RunnableLambda({
      func: (input: string) =>
        retriever.invoke(input).then((response) => response[0].pageContent),
    }).withConfig({runName: "contextRetriever"}),
    question: new RunnablePassthrough(),
  });

  let response;

  try {
    // プロンプトチェーンを作成
    const chain = setupAndRetrieval.pipe(prompt).pipe(model).pipe(outputParser);
    // プロンプトを実行
    const aiResponse = await chain.invoke(`
      MagicBookについて簡単なクイズを英語で作成してください。

      その際、回答は4択で、正しい答えが1つだけになるようにしてください。  
      問題文に答えが含まれないように注意してください。

      問題と回答は1ペアだけ作成してください。  
      なお、correct_answerは回答のキーではなく、answersオブジェクト内の4つの選択肢のいずれかの値と文字列一致させてください。  
      正解は選択肢A〜Dの中でランダムに設定してください。

      問題と回答は次の形式でJSONとして出力してください：

      {
        "question": "問題文",
        "answers": {
          "A": "選択肢A",
          "B": "選択肢B",
          "C": "選択肢C",
          "D": "選択肢D"
        },
        "correct_answer": "正しい回答（選択肢A〜Dのいずれかと一致する値）"
      }

      よろしくお願いします。
    `);
    console.log("aiResponse:::", aiResponse);

    response = {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-API-KEY",
      },
      body: JSON.stringify({
        content: aiResponse,
      }),
    };
  } catch (e: any) {
    console.error("error: ", e);

    response = {
      statusCode: 500,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-API-KEY",
      },
      body: JSON.stringify({
        message: "send meta tx failed.",
      }),
    };
  } finally {
    console.log(`
      ================================ [Generate Quiz API END] ================================
    `);
  }

  return response;
}
```

**LangChain**　を使っているのでとても簡単に実装できました！

S3バケットからマークダウンファイルのデータを取得してくるメソッドはヘルパー関数として別ファイルに実装しています！

こっちはシンプルです。

```ts
import { S3 } from 'aws-sdk';

// S3クライアントを作成
const s3 = new S3();

/**
 * S3バケットから任意のオブジェクトを取得するメソッド
 * @param bucketName バケット名
 * @param objectKey  オブジェクトキー
 * @returns 
 */
export const getS3Object = async (
  bucketName: string, 
  objectKey: string
): Promise<string> => {
  try {
    // S3からオブジェクトを取得
    const data = await s3.getObject({
      Bucket: bucketName,
      Key: objectKey
    }).promise();

    // ファイル内容をUTF-8でデコード
    const fileContent = data.Body?.toString('utf-8');

    if (fileContent) {
      console.log('Markdown file content:', fileContent);
    } else {
      console.error('File content is empty');
    }
    return fileContent || "";
  } catch (error) {
    console.error('Error fetching file from S3:', error);
    return "";
  }
}
```

CDKのテンプレートファイルは以下の通りとなっています！

**OpenAI API** の API キーは事前に Systems Managers Parameter Storeに保管しておく必要があります！

```ts
import * as cdk from 'aws-cdk-lib';
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from "aws-cdk-lib/aws-lambda";
import { NodejsFunction } from "aws-cdk-lib/aws-lambda-nodejs";
import * as ssm from "aws-cdk-lib/aws-ssm";
import { Construct } from 'constructs';
import path = require("path");

/**
 * SolanaRadarAPIServerStack
 */
export class SolanaRadarAPIServerStack extends cdk.Stack {
  /**
   * コンストラクター
   * @param scope 
   * @param id 
   * @param props 
   */
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // SSMから環境変数を取得する。
    const OPENAI_API_KEY = ssm.StringParameter.valueFromLookup(
      this,
      "OPENAI_API_KEY"
    );

    // Lambda関数を定義
    const lambdaFunction = new NodejsFunction(this, "SolanaRadarAPILambdaFunction", {
      runtime: lambda.Runtime.NODEJS_18_X,
      entry: path.join(__dirname, "../resources/lambda/index.ts"),
      handler: "handler",
      bundling: {
        forceDockerBundling: true,
        nodeModules: ["hnswlib-node"],
      },
      timeout: cdk.Duration.seconds(600),
      environment: {
        OPENAI_API_KEY: OPENAI_API_KEY
      },
    });

    // S3からファイルを取得するためのポリシー
    const s3ReadPolicy = new iam.PolicyStatement({
      actions: ['s3:GetObject'],
      resources: ['arn:aws:s3:::solana-radar-hackathon2024/*'], 
    });

    // Lambda関数にS3アクセス権限を追加
    lambdaFunction.addToRolePolicy(s3ReadPolicy);

    // API Gateway Rest APIを作成
    const api = new apigateway.RestApi(this, "SolanaRadarAPI", {
      restApiName: "generateQuiz",
      description: "SolanaRadarAPILambdaFunction servers my Lambda function.",
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
    const items = api.root.addResource("generateQuiz");
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
    new cdk.CfnOutput(this, "SolanaRadarAPIUrl", {
      value: api.url,
      description: "The URL of the API Gateway",
      exportName: "SolanaRadarAPIUrl",
    });

    new cdk.CfnOutput(this, "SolanaRadarAPILambdaFunctionArn", {
      value: lambdaFunction.functionArn,
      description: "The ARN of the Lambda function",
      exportName: "SolanaRadarAPILambdaFunctionArn",
    });
  }
}
```

CDKは本当に便利ですね。

実装の紹介はここまでになります。

---

## 動かしてみた！

では次にこのRAGがどのように動くのか見ていきたいと思います！

まずCDKをデプロイします！！

```bash
yarn cdk deploy '*'
```

しばらく待つと API エンドポイントのURLが出力されるので以下のようにして呼び出します！

```bash
curl -X POST "https://[固有値].execute-api.ap-northeast-1.amazonaws.com/prod/generateQuiz" -H "Content-Type: application/json" -H "x-api-key: [固有値]"
```

しばらく待つと以下のように4択の問題と回答を返してくれます！

```json
{
  "question": "What is the purpose of Session Keys in the MagicBlock framework?",
  "answers": {
    "A": "Enhancing asset security",
    "B": "Improving scalability",
    "C": "Solving cryptographic challenges",
    "D": "Managing user profiles"
  },
  "correct_answer": "A"
}
```

いい感じですね！！

このAPIをフロントエンドから呼び出すようにしており、実際の画面では以下のように出力されます！！

![](/images/cdk_langchain_openai/2.jpg)

これで人が問題を考える必要がなくなるので非常に楽ですね！

バリエーションを増やしたい時はマークダウンファイルを増やせば良さそうです。

CDKで展開したリソースを削除したい時は以下のコマンドを実行します！

```bash
yarn cdk destroy '*'
```

---

## まとめ

いかがでしたでしょうか？？

結構簡単に **RAG** が実装できたので今後もチャンスがあったら実装してみたいなと思いました！

サイトの内容をマークダウンにおとすのだけがめんどくさいですが、以下のサイトを使えば簡単にマークダウンにしてくれるので非常に楽です！

https://huggingface.co/spaces/moritalous/url-to-markdown-v2

また、最後になりますが僕たちのチームのプロダクトである **Q Drop Adventure** を応援していただけると大変嬉しいです！！

プロダクトページは以下です！

https://arena.colosseum.org/refresh-session?redirectBack=/projects/hackathon/q-drop-adventure

プロダクトのピッチ資料やビデオは以下で確認ができます！！  
良かったら見てみてください！！

https://www.loom.com/share/b1b8d8710510400cacf7ecfeca59c4f1

https://www.canva.com/design/DAGSeD3VV-8/7NY0PWR8QbAc5Cje4XG94g/watch?embed

今回は以上となります！！

ここまで読んでいただきありがとうございました！！

---

### 参考文献
1. [GitHub - Q-drop Adventure](https://github.com/ytakahashi2020/airdrop_quest/tree/main)
2. [LangChain公式サイト](https://www.langchain.com/)
3. [RAG (検索拡張生成) とは何ですか?](https://aws.amazon.com/jp/what-is/retrieval-augmented-generation/)
