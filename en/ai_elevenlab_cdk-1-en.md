---
title: "Build and Deploy a Voice AI Agent on AWS with the ElevenLabs SDK!"
emoji: "🎙️"
type: "tech" 
topics: ["ai","react","typescript","aws","cdk"]
published: false
---

# Introduction

Have you ever tried developing a Voice AI Agent?

"Voice AI? That sounds complicated..."

If you're thinking that, you're not alone. While there are advanced tools like Google's **ADK** (Agent Development Kit), there is actually a much simpler way to get started!

https://github.com/kazunori279/adk-streaming-guide

The answer is **ElevenLabs**.

In this article, I’ll show you how to build a Voice AI Agent using React + Vite and how to deploy it to AWS using the AWS CDK!

# Source Code

The complete source code for this project is available on GitHub:

https://github.com/mashharuki/Elevenlab-React-Sample

# What is ElevenLabs?

ElevenLabs is a world-class AI audio platform developed by **ElevenLabs, Inc.** based in New York. It is renowned for its ability to generate extremely natural and emotionally expressive speech.

https://elevenlabs.io

# Creating an AI Agent with ElevenLabs

You can find the developer documentation here:

https://elevenlabs.io/docs

To create an AI Agent, you first need to access the dashboard:

https://elevenlabs.io/app/

![](/images/ai_elevenlab_cdk-1/2.png)

Click on **Agents** on the left sidebar and select **Add Agent**.

![](/images/ai_elevenlab_cdk-1/3.png)

For this tutorial, select **Personal Agent**.

![](/images/ai_elevenlab_cdk-1/4.png)

Enter the name and purpose of your AI Agent.

![](/images/ai_elevenlab_cdk-1/5.png)

Next, specify the **System Prompt**, **Language**, and **Voice Type**.

> One of the best things about ElevenLabs is the sheer number of supported languages and high-quality voices!

![](/images/ai_elevenlab_cdk-1/6.png)

Once configured, click the **Deploy** button in the top right. An **Agent ID** will be generated—make sure to copy and save it!

![](/images/ai_elevenlab_cdk-1/7.png)

Although not covered in detail here, you can also connect your agent to **MCP (Model Context Protocol)** servers!

![](/images/ai_elevenlab_cdk-1/0.png)

![](/images/ai_elevenlab_cdk-1/1.png)

# Integrating into React with the SDK

ElevenLabs provides a dedicated React SDK that makes integration seamless.

https://elevenlabs.io/docs/eleven-agents/libraries/react

## Implementation Highlights

Here are the key parts of the implementation:

- **Loading the Agent ID**

  ```ts
  // Agent ID created in the ElevenLabs dashboard
  const agentIdFromEnv =
    typeof import.meta.env.VITE_ELEVENLABS_AGENT_ID === 'string'
      ? import.meta.env.VITE_ELEVENLABS_AGENT_ID
      : ''
  ```

- **Setting up useConversation**

  We use the `useConversation` hook from the React SDK to manage conversation states and event handlers.

  ```ts
  // Using the useConversation hook to manage state and events
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

- **Requesting Microphone Permission**

  ```ts
  const handleRequestMic = async (): Promise<void> => {
    setErrorText('')
    try {
      // Request mic permission and update state if granted
      await navigator.mediaDevices.getUserMedia({ audio: true })
      setMicReady(true)
    } catch (error: unknown) {
      setErrorText(buildErrorText(error))
    }
  }
  ```

- **Starting a Session**

  Use the `conversation.startSession` method to begin the interaction.

  ```ts
  const handleStartSession = async (): Promise<void> => {
    setErrorText('')
    if (!agentIdFromEnv) {
      setErrorText('Please set VITE_ELEVENLABS_AGENT_ID')
      return
    }
    try {
      if (!micReady) {
        // Activate mic if not already ready
        await navigator.mediaDevices.getUserMedia({ audio: true })
        setMicReady(true)
      }
      // Start session and save the conversation ID
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

- **Sending Voice Data**

  To send a message to the agent, use `conversation.sendUserMessage`.

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

- **Ending the Session**

  ```ts
  const handleEndSession = async (): Promise<void> => {
    setErrorText('')
    try {
      // End the session and clear the state
      await conversation.endSession()
    } catch (error: unknown) {
      setErrorText(buildErrorText(error))
    }
  }
  ```

# Deploying to AWS with CDK

Now, let's deploy our Voice AI Agent application to AWS! We’ll use the AWS CDK to set up an **S3 + CloudFront** architecture.

- **CDK Stack File**

  This is a simplified implementation optimized for testing.

  ```ts
  import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
  import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
  import * as s3 from 'aws-cdk-lib/aws-s3';
  import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
  import * as cdk from 'aws-cdk-lib/core';
  import { Construct } from 'constructs';
  import * as path from 'path';

  export class CdkStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
      super(scope, id, props);

      // S3 Bucket for static assets
      const websiteBucket = new s3.Bucket(this, 'WebsiteBucket', {
        blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
        encryption: s3.BucketEncryption.S3_MANAGED,
        enforceSSL: true,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        autoDeleteObjects: true,
      });

      // CloudFront Distribution
      const distribution = new cloudfront.Distribution(this, 'Distribution', {
        defaultBehavior: {
          origin: origins.S3BucketOrigin.withOriginAccessControl(websiteBucket),
          viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
          cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
        },
        defaultRootObject: 'index.html',
        // SPA routing: fallback to index.html
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

      // Deploy built assets to S3
      new s3deploy.BucketDeployment(this, 'DeployWebsite', {
        sources: [s3deploy.Source.asset(path.join(__dirname, '../../my-app/dist'))],
        destinationBucket: websiteBucket,
        distribution,
        distributionPaths: ['/*'],
      });

      // Outputs
      new cdk.CfnOutput(this, 'DistributionDomainName', {
        value: distribution.distributionDomainName,
      });
    }
  }
  ```

- **Installation**

  Run the following in both `cdk` and `my-app` directories:

  ```bash
  bun install
  ```

- **Environment Variables**

  Create a `.env` file in the `my-app` directory and set your Agent ID:

  ```bash
  VITE_ELEVENLABS_AGENT_ID=your_agent_id_here
  ```

- **Build and Deploy**

  Build the frontend assets:

  ```bash
  bun run build
  ```

  Then deploy the CDK stack:

  ```bash
  bun cdk deploy
  ```

Once the deployment is complete, click the CloudFront URL. You should see the following screen:

![](/images/ai_elevenlab_cdk-1/8.png)

Try turning on the mic and starting a session—you can now talk to your AI agent!

![](/images/ai_elevenlab_cdk-1/9.png)

- **Cleanup**

  Remember to destroy the resources when you're finished testing:

  ```bash
  bun cdk destroy
  ```

# Summary

Building a Voice AI Agent is surprisingly easy with the right tools! By combining ElevenLabs with React and AWS, you can create natural, interactive experiences in no time. 

Imagine connecting this to an MCP server (like the Draw.io MCP)—the possibilities are endless. We are moving towards a future where interacting via voice rather than keyboard will be the norm, so getting comfortable with SDKs like ElevenLabs is definitely a valuable skill.

Thank you for reading!
