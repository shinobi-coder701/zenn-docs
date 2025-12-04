---
title: "TypeScript開発者待望？！ Strands Agents TypeScript SDKを試してみた！"
emoji: "🧬"
type: "tech" 
topics: ["AWS", "生成AI", "TypeScript", "Claude", "AIエージェント"]
published: true
---

:::message
この記事はStrands Agents TypeScripts SDK発表直後の記事となります。

SDKの仕様については今後変更される可能性がありますのでご了承ください。
:::

## はじめに

皆さん、こんにちは！

今ラスベガスで何が行われているかご存知ですか？？

そう、 **AWS re:Invent** の真っ最中です！！  

https://reinvent.awsevents.com/

:::message
めちゃくちゃ行きたい....
:::

毎年めちゃくちゃ多くのアップデートが発表されるのですが、その中で**Strands Agents**のTypeScript SDKが発表されましたー！！！

**TypeScript** 愛用者でAI Agentを開発している人には朗報ですね！！

これまで **TypeScript**を使って AI Agentを開発するとなると **Mastra** か **LangGraph**、**LangChain** とかを使っている方が多かったはずです。

でも**Strands Agents** のTypeScript SDKが登場したことで新たな選択肢として加わってきそうです！！

今回はそのTypeScript SDKを早速試してみましたので記事にしてみました！

ぜひ最後まで読んで行ってください！

## Strands Agentsとは

Strands Agentsとは**AWS**発のAI Agent開発用フレームワークです！！

https://strandsagents.com/latest/

モデル設定がデフォルトで設定されているので**たった数行でAI Agentを実装することができるようになっています！！**

本当に10行ぐらいとかで作れます！！

みのるんさんやmoritalousさんの記事でも簡単に実装できることが特徴として紹介されていました。

https://qiita.com/minorun365/items/dd05a3e4938482ac6055

https://qiita.com/moritalous/items/6a9ed8db3efb00cca28e

登場した当時、**自分も触ってみたい！** と思っていたのですが、

**「Python しかSDKが無いのか....」**

ということであまり積極的には触れてきませんでした...。

そんなこんなで **Mastra** と出会ってしまっていたのでそっちを調べることばかりしてしまってなかなか触れませんでした..


でも**とうとうTypeScriptのSDKが出ました！**

これは触るしかない！！

## Strands Agents TypeScript 版の特徴

ざっと触ってみて自分が感じた特徴というかできることは以下の通りです！

- **めちゃくちゃ簡単にAI Agentが構築できる**
  - デフォルトのモデルは**Claude Sonnet4.5**
- **外部ツールやMCPの統合はもちろん可能！**
- **実装の流れはMastraにかなり似ている**
  - よってMastraを使っていた人はほぼ同じ感覚で実装できる
- **現在対応しているプロバイダーは ClaudeとOpenAI**だけっぽい
  - ここは今後拡充される可能性大！

## いざ実践！！

今回試したソースコードは以下に格納されています。

https://github.com/mashharuki/StrandsAgent-TypeScriptSDK-Sample

### このサンプルコードを試すときの事前準備

AI Agent自体は簡単にセットアップが可能ですが、いくつか事前準備が済んでいること前提です！

今回は以下の6点が済んでいることを確認してください！

- AWSアカウントを作成済みであること
- `aws login`や`Identity Center`などを使ってAWSにログイン済みであること
- ログインしたAWSアカウントで`Claude Sonnet 4.5`のモデルが使用可能であること
  - エラーが出る場合はIAM周りを確認してみてください。
- `bun`をインストール済みであること
- `uv`をインストール済みであること
  - MCP利用時に使います。
- (オプション) Open AIのモデルを使う場合は、Open AIのAPIキーを発行しておくこと

以降はこの4点ができているものとして進めます！！

### GitHubリポジトリのクローンとセットアップ

以下のコマンドを順番に実行して、依存関係のインストールを行います！

```bash
git clone https://github.com/mashharuki/StrandsAgent-TypeScriptSDK-Sample
cd sample-agent 

bun install
```

これで一旦は準備完了です！

### 一番シンプルな呼び出し方を試してみる

ではまずは一番シンプルな呼び出し方を試してみましょう！

コードで言うと以下のような実装になります！

```ts
import { Agent } from '@strands-agents/sdk'

const main = async() => {
    const agent = new Agent({})

    // Invoke
    const result = await agent.invoke('What is the square root of 1764?')
    console.log(result);
};

main();
```

めちゃめちゃシンプルですね！

以下のコマンドで実行します！

```bash
bun run dev
```

すると以下のように返ってきました！！

```bash
√1764 = 42

This is because 42 × 42 = 1764.AgentResult {
  type: "agentResult",
  stopReason: "endTurn",
  lastMessage: Message {
    type: "message",
    role: "assistant",
    content: [
      [Object ...]
    ],
  },
  toString: [Function: toString],
}
```

とても簡単に動かせました！！

### システムプロンプトを設定して試してみる

では続いてシステムプロンプトを設定して試してみます！

**Agent**インスタンスを初期化する際に引数にシステムプロンプトを設定することができます。

コードで言うと以下のようになります。

```ts
import { Agent } from '@strands-agents/sdk'

const main = async() => {
    const agent = new Agent({
        systemPrompt: 'You are a helpful assistant.'
    })

    // Invoke
    const result = await agent.invoke('What is the square root of 1764?')
    console.log(result);
};

main();
```

では動かしてみます！

```bash
bun run dev
```

すると以下のように返ってきました！

```bash
The square root of 1764 is 42.

To verify: 42 × 42 = 1764 ✓AgentResult {
  type: "agentResult",
  stopReason: "endTurn",
  lastMessage: Message {
    type: "message",
    role: "assistant",
    content: [
      [Object ...]
    ],
  },
  toString: [Function: toString],
}
```

さっきより若干丁寧になりました！

### レスポンスストリーミングも試してみる

続いて**レスポンスストリーミング**も試してみます！

呼び出すメソッドが変わるだけなので本当に**Mastra**に似ていますね！

コードは以下のようになります！

```ts
import { Agent } from '@strands-agents/sdk'

const main = async() => {
    const agent = new Agent({
        systemPrompt: 'You are a helpful assistant.',
    })

    console.log('Agent response stream:');
    // invokeではなくstreamメソッドを使う
    for await (const event of agent.stream('Tell me a story about a brave toaster.')) {
      console.log('[Event]', event.type)
    };
};

main();
```

こちらも動かしてみると....

以下のような結果が返ってきました！！

```bash
Agent response stream:
[Event] beforeInvocationEvent
[Event] messageAddedEvent
[Event] beforeModelCallEvent
[Event] modelStreamEventHook
[Event] modelMessageStartEvent
[Event] modelStreamEventHook
#[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 The Brave Little[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 Toaster of[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 Maple[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 Street

Once[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 upon a time, in a co[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
zy kitchen on Maple Street, there[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 lived a chrome[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 toaster named Spark[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
. While[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 other appl[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
iances bo[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
asted about their digital[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 displays[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 and fancy[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 settings[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
, Spark ha[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
d just[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 two[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 slots[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 an[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
d a simple dial.[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 But[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 what[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 Spark lacked in features, he[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 made up for in heart[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
.

One[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 winter[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 morning, a[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 small[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 fire[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 started when[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 a[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 dish[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 tow[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
el fell[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 onto[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 the st[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
ove's[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 gas[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 burner. The flames began[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 to sprea[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
d while[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 the[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 family[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 sl[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
ept up[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
stairs.[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook


Spark knew he had to act[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 fast.[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 Summ[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
oning all[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 his courage, he po[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
pped his[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 lever[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 up[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 and down repeatedly[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
—[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
*[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
click[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
-[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
click-click-click*—making[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 as[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 much noise as possible. When[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 that[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 didn't work, he pushe[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
d his heating[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 elements[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 to[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 maximum[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
,[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 trigg[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
ering the[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 smoke[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 detector[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 above[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 him[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
.

The alarm[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 bl[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
ared.[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 The family w[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
oke an[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
d escape[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
d safely[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
, calling[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 911.[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook


Firef[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
ighters arrived and put[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 out the bl[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
aze before[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 it consume[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
d the house[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
. Though[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 Spark's[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 chrome[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 was[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 scor[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
ched an[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
d his lever[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 bent[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 from[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 the heat, he ha[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
d saved the day[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
.

The[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 family[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 kept[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 him[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 on[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 the[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 counter[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 forever[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 after[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
—[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
even[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 when[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 they bought[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 a new four[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
-slice toaster.[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 Because[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 Spark had proven[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 that b[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
ravery isn't about how[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 fancy[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 you[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 are.[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook


It[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
's about what[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 you do when the heat[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 is on.

**[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
The[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 End**[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
 [Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
🍞[Event] modelContentBlockDeltaEvent
[Event] modelStreamEventHook
[Event] modelContentBlockStopEvent
[Event] modelStreamEventHook
[Event] textBlock
[Event] modelStreamEventHook
[Event] modelMessageStopEvent
[Event] modelStreamEventHook
[Event] modelMetadataEvent
[Event] afterModelCallEvent
[Event] messageAddedEvent
[Event] afterInvocationEvent
[Event] agentResult
```

めちゃくちゃ簡単！！

### 外部ツールを呼び出してみる

続いて外部ツールを呼び出してみます！

チュートリアルに従って以下のようなコードを実装しました！

まずは外部ツールを定義したファイルを用意します。

```ts
import { Agent, tool } from '@strands-agents/sdk'
import { z } from 'zod'
/**
 * 天気予報を取得する外部ツール
 */
const weatherTool = tool({
  name: 'get_weather',
  description: 'Get the current weather for a specific location.',
  inputSchema: z.object({
    location: z.string().describe('The city and state, e.g., San Francisco, CA'),
  }),
  callback: (input) => {
    // input is fully typed based on the Zod schema
    return `The weather in ${input.location} is 72°F and sunny.`
  },
})

export {
    weatherTool,
}
```

これで準備OKです！

あとは`Agent`インスタンスを初期化する際の引数の`tools`に設定すればOKです！

```ts
import { Agent } from '@strands-agents/sdk'
import { 
    weatherTool,
} from "./tools";

/**
 * メイン関数
 */
const main = async() => {
    // Create agent (uses default Amazon Bedrock provider)
    const agent = new Agent({
        systemPrompt: 'You are a helpful assistant.',
        tools: [
            weatherTool,
        ]
    })

    // Invoke 
    const result2 = await agent.invoke('What is the weather in San Francisco?')
    console.log(result2);
};

main();
```

こちらも同様に実行してみます。

```bash
bun run dev
```

すると以下のような結果が返ってきました！！

```bash
🔧 Tool #1: get_weather
✓ Tool completed
The weather in San Francisco is currently 72°F and sunny.AgentResult {
  type: "agentResult",
  stopReason: "endTurn",
  lastMessage: Message {
    type: "message",
    role: "assistant",
    content: [
      [Object ...]
    ],
  },
  toString: [Function: toString],
```

うまく外部ツールを呼び出せています！

### MCPを呼び出してみる

では続いてMCPの設定方法についてです！

こちらもまずMCP用のファイルを用意して準備します。

今回は**AWS MCP Servers**の**AWS Document MCP**を使っています。

```ts
import { Agent, McpClient  } from '@strands-agents/sdk'
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

/**
 * AWS Document MCPサーバーを利用するためのMCPクライアントの設定
 */
const documentationTools = new McpClient({
  transport: new StdioClientTransport({
    command: "uvx",
    args: ["awslabs.aws-documentation-mcp-server@latest"],
  }),
});

export {
    documentationTools
}
```

これで準備OKです！

あとは外部ツールを設定したときと同じ流れでコードは以下のようになります！

```ts
import { Agent } from '@strands-agents/sdk'
import { 
    documentationTools
} from "./tools";

/**
 * メイン関数
 */
const main = async() => {
    // Create agent (uses default Amazon Bedrock provider)
    const agent = new Agent({
        systemPrompt: 'You are a helpful assistant.',
        tools: [
            documentationTools
        ]
    })

    // invoke
    const result3 = await agent.invoke("Use a random tool from the MCP server.");
    console.log(result3);

    await documentationTools.disconnect();
};

main();
```

こちらも同様に実行してみます。

```bash
bun run dev
```

すると....

```bash
[12/04/25 16:02:24] INFO     Processing request of type ListToolsRequest                                                                                                           server.py:709
I'll use the search_documentation tool to search for information about AWS Lambda.
🔧 Tool #1: search_documentation
[12/04/25 16:02:28] INFO     Processing request of type CallToolRequest                                                                                                            server.py:709
[12/04/25 16:02:30] INFO     HTTP Request: POST https://proxy.search.docs.aws.amazon.com/search?session=dccc8958-e7f7-44ee-97de-c6bacda4457f "HTTP/1.1 200 OK"                   _client.py:1740
✓ Tool completed
Great! I used the `search_documentation` tool to search for "AWS Lambda" and found 5 relevant results:

1. **AWS Lambda Documentation** - The main documentation hub for Lambda
2. **AWS Lambda API Reference** - Details about all Lambda API operations
3. **AWS Lambda CLI** - Command-line interface documentation
4. **AWS Lambda Developer Guide** - Comprehensive guide for developers
5. **What is AWS Lambda?** - An introductory page explaining Lambda's capabilities

The search results show that AWS Lambda is used for building scalable web apps, mobile backends, processing data streams, responding to database changes, running scheduled tasks, and more. Would you like me to read any of these documentation pages in detail?AgentResult {
  type: "agentResult",
  stopReason: "endTurn",
  lastMessage: Message {
    type: "message",
    role: "assistant",
    content: [
      [Object ...]
    ],
  },
  toString: [Function: toString],
}
```

ちゃんとDocument MCPを呼び出せていますね！！

やったー🙌！！！

## まとめ

とても簡単な紹介にはなりますが、以上で TypeScript SDKを試してみた記録の紹介は以上になります！

**触ってみた感じ、コードの実装はMastraと大体同じなのでMastra触ってみた人はすぐに慣れると思います！**

AgentCoreとか他のAWSサービスとの連携も踏まえるとAI AgentをAWS上で動かす場合には強力な選択肢になりそうです！！

今回はここまでになります！！

読んでいただきありがとうございました！！