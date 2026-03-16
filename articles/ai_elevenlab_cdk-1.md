---
title: "11ElevenLabs SDKを使って音声AI AgentをAWS上にデプロイしてみよう！"
emoji: "🎙️"
type: "tech" 
topics: ["ai","react","typescript","aws","cdk"]
published: false
---

# はじめに

皆さんは、音声AIエージェントを開発したことがありますか？

「音声AIエージェントなんか難しそう...」

そう思われている方もいるのではないでしょうか？

最近だとGoogleが提供している**ADK**を使ったサンプルコード等も発表されていますが、実はもっと簡単に実装する方法があります！

https://github.com/kazunori279/adk-streaming-guide

それは**ElevenLabs**を利用することです！

今回はReact+Viteで動く音声AIエージェントの開発方法とAWS CDKへのデプロイ方法をまとめて紹介します！

# 今回試したソースコード

以下のGitHubリポジトリに格納してあります。

https://github.com/mashharuki/Elevenlab-React-Sample

# 11ElevenLabsとは

ElevenLabs（イレブンラボ）はニューヨークに拠点を置く**ElevenLabs, Inc.**が提供する、極めて自然で感情豊かな音声を生成できる世界最高峰の音声AIプラットフォームです！

https://elevenlabs.io

# 11ElevenLabsでAI Agentを作ってみよう！

開発者向けドキュメントは以下から確認ができます！

https://elevenlabs.io/docs

AI Agentを作成するためにはダッシュボードにアクセスする必要があります！

https://elevenlabs.io/app/

![](/images/ai_elevenlab_cdk-1/2.png)

画面左側のAgentsをクリックしてAgentを追加します！

![](/images/ai_elevenlab_cdk-1/3.png)

今回はPersonal Agentを選択します！

![](/images/ai_elevenlab_cdk-1/4.png)

AI Agentの名前と目的を入力します。

![](/images/ai_elevenlab_cdk-1/5.png)

次にシステムプロンプト、言語、そして音声のタイプを指定します。

> 11ElevenLabsのすごいところは対応言語と音声のタイプの多さです！

![](/images/ai_elevenlab_cdk-1/6.png)

設定が完了したら右上のdeployボタンを押してAI Agentをデプロイします！

この時**Agent ID**が出力されるのでそれを控えておきます！

![](/images/ai_elevenlab_cdk-1/7.png)

今回は紹介しませんが、MCPサーバーとも接続させることが可能です！

![](/images/ai_elevenlab_cdk-1/0.png)

![](/images/ai_elevenlab_cdk-1/1.png)

# SDKを使ってReactに組み込んでみよう！

11ElevenLabsから提供されているReact SDKを使えばすぐにアプリに導入することができます！

https://elevenlabs.io/docs/eleven-agents/libraries/react

## 実装のポイント

いくつか重要なポイントだけピックアップして紹介していきます！

- **Agent IDの読み込み**

  ```ts
  // Eleven Labsのダッシュボードで作成したAgent ID
  const agentIdFromEnv =
    typeof import.meta.env.VITE_ELEVENLABS_AGENT_ID === 'string'
      ? import.meta.env.VITE_ELEVENLABS_AGENT_ID
      : ''
  ```

- **useConversationの設定**

  **11ElevenLabs** React SDKの機能である`useConversation`を使って会話の状態やイベントハンドラーを管理していくことになります！

  ```ts
  // useConversation フックを使用して会話の状態とイベントハンドラーを管理
  const conversation = useConversation({
    micMuted,
    volume: volumeRate,
    onMessage: (message: unknown) => {
      setMessages((prevMessages) => [...prevMessages, buildMessageItem(message)])
    },
    onError: (error: unknown) => {
      setErrorText(buildErrorText(error))
    },
    onStatusChange: (payload: { status: string }) => {
      setStatusText(payload.status)
    },
    onModeChange: (payload: { mode: string }) => {
      setModeText(payload.mode)
    },
    onConnect: () => {
      setErrorText('')
    },
    onDisconnect: () => {
      setConversationId('')
    },
  })
  ```

- **マイクの要求**

  マイクを使えるようにします！

  ```ts
  const handleRequestMic = async (): Promise<void> => {
    setErrorText('')
    try {
      // マイクの使用許可をリクエストし、許可された場合は状態を更新
      await navigator.mediaDevices.getUserMedia({ audio: true })
      setMicReady(true)
    } catch (error: unknown) {
      setErrorText(buildErrorText(error))
    }
  }
  ```

- **セッション開始**

  セッションを開始するには`conversation.startSession`メソッドを使います！

  ```ts
  const handleStartSession = async (): Promise<void> => {
    setErrorText('')
    if (!agentIdFromEnv) {
      setErrorText('VITE_ELEVENLABS_AGENT_ID を設定してください')
      return
    }
    try {
      if (!micReady) {
        // マイクがオンになっていない場合は有効化
        await navigator.mediaDevices.getUserMedia({ audio: true })
        setMicReady(true)
      }
      // セッションを開始し、会話IDを取得して状態に保存
      const newConversationId = await conversation.startSession({
        agentId: agentIdFromEnv,
        connectionType,
        userId: userId ? userId : undefined,
      })
      setConversationId(newConversationId)
    } catch (error: unknown) {
      setErrorText(buildErrorText(error))
    }
  }
  ```

- **音声データの送信**

  音声データを**11ElevenLabs**のAI Agentに送るには`conversation.sendUserMessage`メソッドを利用します！

  ```ts
  const handleSendMessage = (): void => {
    const trimmedText = inputText.trim()
    if (!trimmedText) {
      return
    }
    conversation.sendUserMessage(trimmedText)
    setInputText('')
  }
  ```

- **セッション終了**

  ```ts
  const handleEndSession = async (): Promise<void> => {
    setErrorText('')
    try {
      // セッションを終了し、会話IDを状態からクリアする
      await conversation.endSession()
    } catch (error: unknown) {
      setErrorText(buildErrorText(error))
    }
  }
  ```

ポイントなる実装の解説は以上です！

# CDKを使ってAWSにデプロイ！

では実装した音声AI AgentアプリをAWS上にデプロイしてみましょう！

今回はCDKを使って**S3**+**CloudFront**の構成を用意し、そこにReactアプリをデプロイしていきます！

- **CDKスタックファイル**

  検証目的の環境なので非常に簡易的な実装にしています！

  ```ts
  import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
  import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
  import * as s3 from 'aws-cdk-lib/aws-s3';
  import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
  import * as cdk from 'aws-cdk-lib/core';
  import { Construct } from 'constructs';
  import * as path from 'path';

  /**
  * CDK スタックファイル
  */
  export class CdkStack extends cdk.Stack {
    /**
    * コンストラクター
    * @param scope 
    * @param id 
    * @param props 
    */
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
      super(scope, id, props);

      // 静的アセット用のS３バケット
      const websiteBucket = new s3.Bucket(this, 'WebsiteBucket', {
        blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
        encryption: s3.BucketEncryption.S3_MANAGED,
        enforceSSL: true,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        autoDeleteObjects: true,
      });

      // CloudFront ディストビューションの設定
      const distribution = new cloudfront.Distribution(this, 'Distribution', {
        defaultBehavior: {
          origin: origins.S3BucketOrigin.withOriginAccessControl(websiteBucket),
          viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
          cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
        },
        defaultRootObject: 'index.html',
        // SPA routing: fallback to index.html for client-side routing
        errorResponses: [
          {
            httpStatus: 403,
            responseHttpStatus: 200,
            responsePagePath: '/index.html',
            ttl: cdk.Duration.minutes(5),
          },
          {
            httpStatus: 404,
            responseHttpStatus: 200,
            responsePagePath: '/index.html',
            ttl: cdk.Duration.minutes(5),
          },
        ],
      });

      // ビルド済みのアセットをS3バケットをデプロイする
      new s3deploy.BucketDeployment(this, 'DeployWebsite', {
        sources: [s3deploy.Source.asset(path.join(__dirname, '../../my-app/dist'))],
        destinationBucket: websiteBucket,
        distribution,
        distributionPaths: ['/*'],
      });

      // ============================================================
      // Outputs
      // ============================================================

      new cdk.CfnOutput(this, 'DistributionDomainName', {
        value: distribution.distributionDomainName,
        description: 'CloudFront distribution domain name',
      });

      new cdk.CfnOutput(this, 'DistributionId', {
        value: distribution.distributionId,
        description: 'CloudFront distribution ID',
      });

      new cdk.CfnOutput(this, 'BucketName', {
        value: websiteBucket.bucketName,
        description: 'S3 bucket name',
      });
    }
  }
  ```

- **依存関係のインストール**

  `cdk`と`my-app`でそれぞれ以下のコマンドを実行します。

  ```bash
  bun install
  ```

- **環境変数のセットアップ**

  `my-app`のみ環境変数ファイル`.env`を作成し以下の値をセットします。  
  Agent IDは先ほど11Elevenlabsのダッシュボードで作成したAgentのIDを指定します。

  ```bash
  VITE_ELEVENLABS_AGENT_ID=your_agent_id_here
  ```

- **フロントエンドのビルド**

  デプロイする静的アセットを用意します！

  `my-app`ディレクトリ配下でビルドコマンドを実施します！

  ```bash
  bun run build
  ```

  これで準備OKです！

- **CDKスタックをデプロイ**

  ```bash
  bun cdk deploy
  ```

  問題なくデプロイが完了したらCloudFrontのURLが出力されるはずなのでそれをクリックすればアプリにアクセスができます！

  以下のような画面が描画されればOKです！

  ![](/images/ai_elevenlab_cdk-1/8.png)

  試しにマイクをONにしてセッション開始してみると以下のように音声で色々と聞けちゃいます！！

  ![](/images/ai_elevenlab_cdk-1/9.png)

- **クリーンアップ**

  動作確認したら忘れずにリソースを削除しましょう！

  ```bash
  bun cdk destroy
  ```

# まとめ

今回の記事は以上になります！

どうでしたでしょうか？！

意外と簡単に音声AIエージェントが作れてしまうことが分かっていただけたかと思います！

今回はMCPサーバーを繋いでいませんが、これでdrawio MCPとか繋いだらすごいことができそうです！

今後はキーボードではなく音声で操作していくことが増えていくかと思いますので、**11ElevenLabs**のSDKの使い方を知っておくことは良いと思います！

今回はここまでになります！

読んでいただきありがとうございました！