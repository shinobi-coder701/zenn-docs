---
title: "Motia × Strands Agent SDK: A Guide to AI Agent Development 3"
emoji: "🐳"
type: "tech"
topics: ["aws", "cdk", "AI", "StrandsAgent", "motia"]
published: false
---

## Introduction

Hello everyone!

This is the third installment in our series on AI agent development using **Motia** and the **Strands Agent SDK**!

https://zenn.dev/mashharuki/articles/aws_strands_agent_motia-1

https://zenn.dev/mashharuki/articles/aws_strands_agent_motia-2

In the previous post, we explored how to call the **Motia** backend API from a frontend application.

In this article, we'll focus on containerizing the backend with Docker and deploying it to AWS using the AWS Cloud Development Kit (CDK)!

> Note: I won't be diving into the specific frontend or backend logic implementation details here. If you're interested in those, please check out the previous posts!

I hope you enjoy reading this to the end!

# Source Code Used in This Post

The complete source code is available in the following GitHub repository:

https://github.com/mashharuki/Motia-Strands-Agent-Sample

# Dockerizing Motia for ECS/App Runner

The most challenging part of this project was creating the Dockerfile.

Since Motia requires both Node.js and Python runtimes to be active simultaneously, setting up the environment (like PATH configurations) was a bit tricky at first.

The following Dockerfile configuration successfully runs the Motia backend:

```yaml
FROM node:20-slim

# Install Python + uv
RUN apt-get update && apt-get install -y python3 python3-venv curl && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install iii CLI
RUN curl -fsSL https://install.iii.dev/iii/main/install.sh | sh
ENV PATH="/root/.iii/bin:/root/.local/bin:${PATH}"

WORKDIR /app

# Node.js Dependencies
COPY nodejs/package*.json nodejs/
RUN cd nodejs && npm install

# Python Dependencies
COPY python/pyproject.toml python/
RUN cd python && /root/.local/bin/uv venv && /root/.local/bin/uv pip install -r pyproject.toml

# Source Code & Config
COPY nodejs/ nodejs/
COPY python/ python/
COPY iii-config.yaml .

# Data Directory
RUN mkdir -p data

EXPOSE 3111 3112

CMD ["iii", "-c", "iii-config.yaml"]
```

While supporting two runtimes makes the Dockerfile more complex, it ensures that both the Node.js agent logic and Python tools can run in a single container.

After building this, I realized there's an official Docker setup guide in the documentation as well! Check it out if you're interested:

https://www.motia.dev/docs/deployment-guide/self-hosted#docker-setup

# Explaining the CDK Stack

Next, let's break down the **CDK Stack**.

For the backend container runtime, I decided to use **AWS App Runner** for the first time!

https://aws.amazon.com/apprunner/

Since the agent needs to call **Amazon Bedrock**, I've added the necessary IAM permissions to the instance role. The frontend follows a standard **S3 + CloudFront** architecture.

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
 * CDK Stack for Motia Strands Agent
 * - S3 Bucket for frontend static files
 * - App Runner Service for backend (Docker image from local directory)
 * - CloudFront Distribution with S3 OAC and App Runner custom origin
 * - IAM roles for App Runner to access ECR and Bedrock
 */
export class CdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // ========================================
    // 1. S3 Bucket - Frontend Static Files
    // ========================================
    const siteBucket = new s3.Bucket(this, 'FrontendBucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
    });

    // ========================================
    // 2. Docker Image Asset - Motia Backend
    // ========================================
    const imageAsset = new ecr_assets.DockerImageAsset(this, 'MotiaBackendImage', {
      directory: path.join(__dirname, '../../my-project'),
      platform: ecr_assets.Platform.LINUX_AMD64,
    });

    // ========================================
    // 3. IAM Roles for App Runner
    // ========================================

    // Access Role for ECR
    const accessRole = new iam.Role(this, 'AppRunnerAccessRole', {
      assumedBy: new iam.ServicePrincipal('build.apprunner.amazonaws.com'),
    });
    imageAsset.repository.grantPull(accessRole);

    // Instance Role for Bedrock Access
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
    });

    // App Runner AutoScaling (min:1, max:1 for cost efficiency in this sample)
    const autoScalingConfig = new apprunner.CfnAutoScalingConfiguration(this, 'AppRunnerAutoScaling', {
      autoScalingConfigurationName: 'motia-single-instance',
      maxConcurrency: 100,
      maxSize: 1,
      minSize: 1,
    });
    appRunnerService.autoScalingConfigurationArn = autoScalingConfig.attrAutoScalingConfigurationArn;

    const appRunnerServiceUrl = appRunnerService.attrServiceUrl;

    // ========================================
    // 5. CloudFront Distribution
    // ========================================

    const oac = new cloudfront.S3OriginAccessControl(this, 'OAC', {
      signing: cloudfront.Signing.SIGV4_ALWAYS,
    });

    const s3Origin = origins.S3BucketOrigin.withOriginAccessControl(siteBucket, {
      originAccessControl: oac,
    });

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
    // 6. S3 Deployment - Uploading Frontend
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

    cdk.Tags.of(this).add('Project', 'motia-strands-agent');
  }
}
```

# Time to Deploy!

- **Install Dependencies**

  First, install the necessary packages. Run this command inside the `cdk` directory:

  ```bash
  bun install
  ```

- **Deploy to AWS**

  ```bash
  bun cdk deploy
  ```  

  After a few minutes, the CloudFront URL will be displayed in the terminal. Clicking it should reveal the following screen (this screenshot is from the local environment, but the deployed version looks identical!):

  ![](/images/aws_strands_agent_motia-2/1.png)

  You can use the AI assistant feature by entering prompts in the chat box!

  ![](/images/aws_strands_agent_motia-2/5.png)

- **Cleanup**

  Once you're done testing, don't forget to delete the resources to avoid unnecessary costs!

  ```bash
  bun cdk destroy
  ```

# Summary

In this post, we successfully containerized the Motia backend and deployed it to AWS using App Runner and CDK.

Through this sample project, we've covered everything from basic implementation to full-scale cloud deployment. I plan to use this architecture to develop and share more original applications in the future!

Thank you so much for reading!
