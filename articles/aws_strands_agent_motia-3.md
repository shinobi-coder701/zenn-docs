---
title: "Motia × Strands Agent SDKで作るAIエージェント開発入門3"
emoji: "🐳"
type: "tech"
topics: ["aws", "cdk", "AI", "StrandsAgent", "motia"]
published: false
---

## はじめに

こんにちは！

今回の記事は**Motia**と**Strands Agent SDK**を使ったAIエージェント開発をテーマに記事の第3回目の記事となります！

https://zenn.dev/mashharuki/articles/aws_strands_agent_motia-1

https://zenn.dev/mashharuki/articles/aws_strands_agent_motia-1

前回の記事でフロントエンドから**Motia**のバックエンドAPIサーバーを呼び出すところまでを試しました。

今回はバックエンドをDockerコンテナ化し、CDKでAWS上にデプロイするところまで試してみたいと思います！

> フロントエンドやバックエンドの実装についての解説はこの記事の中ではしないので気になる方は前回の記事をご覧ください！

ぜひ最後まで読んでいってください！

# 今回試したソースコード

以下のGitHubリポジトリに格納してあります！

https://github.com/mashharuki/Motia-Strands-Agent-Sample

# ECSで動かすために用意したMotia向けのDockerファイル

今回一番ハマったのがこのDockerファイルの作成です。

`iii`入れたり、NodejsとPythonの2つのランタイムが動くような設定にしなければならないので最初PATHとかが通らないエラーが出たりして苦戦しました。

現時点では以下のようなファイルを用意してあげれば動きます！

```yaml
FROM node:20-slim

# Python + uv インストール
RUN apt-get update && apt-get install -y python3 python3-venv curl && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# iii CLI インストール
RUN curl -fsSL https://install.iii.dev/iii/main/install.sh | sh
ENV PATH="/root/.iii/bin:/root/.local/bin:${PATH}"

WORKDIR /app

# Node.js 依存関係
COPY nodejs/package*.json nodejs/
RUN cd nodejs && npm install

# Python 依存関係
COPY python/pyproject.toml python/
RUN cd python && /root/.local/bin/uv venv && /root/.local/bin/uv pip install -r pyproject.toml

# ソースコード & 設定
COPY nodejs/ nodejs/
COPY python/ python/
COPY iii-config.yaml .

# データディレクトリ
RUN mkdir -p data

EXPOSE 3111 3112

CMD ["iii", "-c", "iii-config.yaml"]
```

2つのランタイムを動かせる代わりにDockerfileが複雑になってしまうという欠点がありますね。

頑張って作った後に公式ドキュメントでDockerfileが紹介されているのを見つけました...笑

公式ドキュメントの方も気になるという方は以下のページを参照してください！

https://www.motia.dev/docs/deployment-guide/self-hosted#docker-setup

# CDKスタックについて

次に**CDKスタック**の中身について解説していきます！

Dockerコンテナの起動環境として今回は**AppRunner**を初めて使ってみました！

https://aws.amazon.com/jp/apprunner/

**Amazon Bedrock**を呼び出す必要があるのでECSには必要な権限を追加しています！

フロントエンドは **S3 + CloudFront** のよくある構成です！

```ts
import * as apprunner from 'aws-cdk-lib/aws-apprunner';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as ecr_assets from 'aws-cdk-lib/aws-ecr-assets';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import * as cdk from 'aws-cdk-lib/core';
import { Construct } from 'constructs';
import * as path from 'path';

/**
/**
 * Motia Strands Agent用CDKスタック
 * - フロントエンド静的ファイル用S3バケット
 * - バックエンド用App Runnerサービス（ローカルディレクトリのDockerイメージ）
 * - S3用OACとApp Runner用カスタムオリジンを備えたCloudFront ディストリビューション
 * - ECRおよびBedrockにアクセスするためのApp Runner用IAMロール
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

    // ========================================
    // 1. S3 Bucket - フロントエンド静的ファイル
    // ========================================
    const siteBucket = new s3.Bucket(this, 'FrontendBucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
    });

    // ========================================
    // 2. Docker Image Asset - Motia バックエンド
    // ========================================
    const imageAsset = new ecr_assets.DockerImageAsset(this, 'MotiaBackendImage', {
      directory: path.join(__dirname, '../../my-project'),
      platform: ecr_assets.Platform.LINUX_AMD64,
    });

    // ========================================
    // 3. IAM Roles for App Runner
    // ========================================

    // ECR アクセスロール
    const accessRole = new iam.Role(this, 'AppRunnerAccessRole', {
      assumedBy: new iam.ServicePrincipal('build.apprunner.amazonaws.com'),
    });
    imageAsset.repository.grantPull(accessRole);

    // インスタンスロール (Bedrock アクセス用)
    const instanceRole = new iam.Role(this, 'AppRunnerInstanceRole', {
      assumedBy: new iam.ServicePrincipal('tasks.apprunner.amazonaws.com'),
    });
    instanceRole.addToPolicy(new iam.PolicyStatement({
      actions: [
        'bedrock:InvokeModel',
        'bedrock:InvokeModelWithResponseStream',
      ],
      resources: ['*'],
    }));

    // ========================================
    // 4. App Runner Service (L1 - CfnService)
    // ========================================
    const appRunnerService = new apprunner.CfnService(this, 'MotiaBackendService', {
      serviceName: 'motia-backend',
      sourceConfiguration: {
        authenticationConfiguration: {
          accessRoleArn: accessRole.roleArn,
        },
        imageRepository: {
          imageIdentifier: imageAsset.imageUri,
          imageRepositoryType: 'ECR',
          imageConfiguration: {
            port: '3111',
            runtimeEnvironmentVariables: [
              { name: 'AWS_REGION', value: 'us-east-1' },
            ],
          },
        },
        autoDeploymentsEnabled: false,
      },
      instanceConfiguration: {
        cpu: '1 vCPU',
        memory: '2 GB',
        instanceRoleArn: instanceRole.roleArn,
      },
      autoScalingConfigurationArn: undefined, // デフォルト (min:1, max:25)
    });

    // App Runner の AutoScaling (min:1, max:1)
    const autoScalingConfig = new apprunner.CfnAutoScalingConfiguration(this, 'AppRunnerAutoScaling', {
      autoScalingConfigurationName: 'motia-single-instance',
      maxConcurrency: 100,
      maxSize: 1,
      minSize: 1,
    });
    appRunnerService.autoScalingConfigurationArn = autoScalingConfig.attrAutoScalingConfigurationArn;

    // App Runner サービスURL
    const appRunnerServiceUrl = appRunnerService.attrServiceUrl;

    // ========================================
    // 5. CloudFront Distribution
    // ========================================

    // OAC for S3
    const oac = new cloudfront.S3OriginAccessControl(this, 'OAC', {
      signing: cloudfront.Signing.SIGV4_ALWAYS,
    });

    // S3 Origin
    const s3Origin = origins.S3BucketOrigin.withOriginAccessControl(siteBucket, {
      originAccessControl: oac,
    });

    // App Runner Origin
    const appRunnerOrigin = new origins.HttpOrigin(appRunnerServiceUrl, {
      protocolPolicy: cloudfront.OriginProtocolPolicy.HTTPS_ONLY,
    });

    const distribution = new cloudfront.Distribution(this, 'Distribution', {
      defaultBehavior: {
        origin: s3Origin,
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
      },
      additionalBehaviors: {
        '/tickets*': {
          origin: appRunnerOrigin,
          viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
          allowedMethods: cloudfront.AllowedMethods.ALLOW_ALL,
          cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED,
          originRequestPolicy: cloudfront.OriginRequestPolicy.ALL_VIEWER,
        },
      },
      defaultRootObject: 'index.html',
      errorResponses: [
        {
          httpStatus: 403,
          responseHttpStatus: 200,
          responsePagePath: '/index.html',
          ttl: cdk.Duration.minutes(0),
        },
        {
          httpStatus: 404,
          responseHttpStatus: 200,
          responsePagePath: '/index.html',
          ttl: cdk.Duration.minutes(0),
        },
      ],
    });

    // ========================================
    // 6. S3 Deployment - フロントエンドをアップロード
    // ========================================
    new s3deploy.BucketDeployment(this, 'DeployFrontend', {
      sources: [s3deploy.Source.asset(path.join(__dirname, '../../frontend/dist'))],
      destinationBucket: siteBucket,
      distribution,
      distributionPaths: ['/*'],
    });

    // ========================================
    // Outputs
    // ========================================
    new cdk.CfnOutput(this, 'CloudFrontUrl', {
      value: `https://${distribution.distributionDomainName}`,
      description: 'CloudFront Distribution URL',
    });

    new cdk.CfnOutput(this, 'AppRunnerServiceUrl', {
      value: `https://${appRunnerServiceUrl}`,
      description: 'App Runner Service URL',
    });

    // タグ
    cdk.Tags.of(this).add('Project', 'motia-strands-agent');
  }
}
```

# いざ、デプロイ！

- **依存関係のインストール**

  まず以下のコマンドで依存関係をインストールします！

  このコマンドは`cdk`ディレクトリ配下で実行してください。

  ```bash
  bun install
  ```

- **デプロイ**

  ```bash
  bun cdk deploy
  ```  

  しばらくするとCloudFrontのURLが出力されるのでそれをクリックすると以下のような画面が出てくるはずです(画像はローカルで立ち上げた時のものですが同じものが描画されます)！

  ![](/images/aws_strands_agent_motia-2/1.png)

  AIアシスタント機能もチャット欄にプロンプトを入力すれば使えます！

  ![](/images/aws_strands_agent_motia-2/5.png)

- **クリーンアップ**

  検証が終わったら忘れずにリソースを削除しましょう！

  ```bash
  bun cdk destroy
  ```

# まとめ

Dockerコンテナ化してAppRunnerで動かすところまでを試してみました！  

今回作成したサンプルコードで基本的な実装方法やAWSへのデプロイ方法は学んだので今後もこの構成を使ってオリジナルアプリの開発・情報発信を積極的にやっていこうと思います！

ここまで読んでいただきありがとうございました！