---
title: "Motia × Strands Agent SDKで作るAIエージェント開発入門2"
emoji: "🚀"
type: "tech"
topics: ["aws", "typescript", "AI", "StrandsAgent", "motia"]
published: true
---

## はじめに

こんにちは！

今回の記事は**Motia**と**Strands Agent SDK**を使ったAIエージェント開発をテーマに記事の第2回目の記事となります！

https://zenn.dev/mashharuki/articles/aws_strands_agent_motia-1

前回の記事でAPIサーバーとして動かすところまでは試したので今回はフロントエンドから呼び出してみる部分についてまとめている記事になります！

> バックエンドの実装についての解説はこの記事の中ではしないので気になる方は前回の記事をご覧ください！

ぜひ最後まで読んでいってください！

# 今回試したソースコード

以下のGitHubリポジトリに格納してあります！

https://github.com/mashharuki/Motia-Strands-Agent-Sample

# APIで実装した機能とエンドポイント一覧

| メソッド | エンドポイント | 機能 | 実装 |
| :--- | :--- | :--- | :--- |
| GET | /tickets | チケット一覧取得 | Node.js |
| POST | /tickets | チケット新規作成 | Node.js |
| POST | /tickets/triage | チケットトリアージ | Python |
| POST | /tickets/escalate | チケットエスカレーション | Python |
| POST | /tickets/ai-assistant | AIアシスタント呼び出し | Node.js |

# フロントエンドの解説

フロントエンドは**React.js**+**Vite**で実装しています！

基本的にはAPIを呼び出しているだけなので通常のバックエンドとのインテグレーションに近いイメージです。

## UIのイメージ

UI構成はサイドバー + トップバー + メインコンテンツ + AIパネルという感じです！

![](/images/aws_strands_agent_motia-2/0.png)

ダッシュボード的な感じで今開いているチケットの一覧と状況を把握できるような見た目になっています！

![](/images/aws_strands_agent_motia-2/1.png)

![](/images/aws_strands_agent_motia-2/2.png)

![](/images/aws_strands_agent_motia-2/3.png)

![](/images/aws_strands_agent_motia-2/4.png)

AIアシスタント機能は右側のチャット欄にテキストを入力することで利用することが可能です！

ツールとしてチケットの一覧を取得する機能が実装してあるので今開いているチケットの状況を聞くことが可能です！

![](/images/aws_strands_agent_motia-2/5.png)

## ポイントとなる実装部分

`src/lib/api.ts` で共通 `request<T>()` を定義し各APIをラップしています！

- `Content-Type: application/json` を標準付与
- 非2xxはレスポンス本文を `Error` として投げる
- 返却JSONを型付きで扱う

```ts
/**
 * 共通のリクエスト処理
 * @param path
 * @param options
 * @returns
 */
async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body || `Request failed: ${res.status}`);
  }
  return res.json();
}
```

そして呼び出し可能なAPIは以下のメソッドでラップして呼び出せるようにしています！

```ts
/**
 * APIクライアント
 */
export const api = {
  // チケット一覧の取得
  getTickets: async () => {
    const data = await request<Ticket[] | { tickets: unknown[] }>("/tickets");
    const rawTickets = Array.isArray(data)
      ? data
      : Array.isArray(data?.tickets)
        ? data.tickets
        : [];
    return rawTickets.map(normalizeTicket).filter((t): t is Ticket => t !== null);
  },
  // チケットの作成
  createTicket: (payload: CreateTicketPayload) =>
    request<CreateTicketResponse>("/tickets", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  // チケットのトリアージ
  triageTicket: (payload: TriagePayload) =>
    request<Ticket>("/tickets/triage", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // チケットのエスカレーション
  escalateTicket: (payload: EscalatePayload) =>
    request<Ticket>("/tickets/escalate", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  // AIアシスタントへの問い合わせ
  aiAssistant: (payload: AIAssistantPayload) =>
    request<AIAssistantResponse>("/tickets/ai-assistant", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};
```

## 実際にAPIを呼び出している箇所

- **チケットを取得するAPI**

  ```ts
  /**
   * Fetch tickets from the API and update state
   */
  const fetchTickets = useCallback(async () => {
    try {
      // APIを呼び出して取得
      const data = await api.getTickets();
      setTickets(Array.isArray(data) ? data : []);
    } catch {
      // API may not be running yet
    }
  }, []);
  ```

- **AIアシスタントAPI**

  ```ts
  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim() || loading) return;
      setShowSuggestions(false);
      const userMsg: Message = {
        id: ++msgId,
        role: "user",
        content: text.trim(),
      };
      setMessages((prev) => [...prev, userMsg]);
      setInput("");
      setLoading(true);

      try {
        // ペイロードを用意
        const payload = contextTicketId
          ? { prompt: text.trim(), ticketId: contextTicketId }
          : { prompt: text.trim() };
        // AIアシスタントAPI(Strands Agent越しにAmazon Bedrockを呼び出す)
        const res = await api.aiAssistant(payload);
        const aiMsg: Message = {
          id: ++msgId,
          role: "ai",
          content: typeof res.answer === "string" ? res.answer : "",
        };
        setMessages((prev) => [...prev, aiMsg]);
      } catch (err) {
        const errMsg: Message = {
          id: ++msgId,
          role: "ai",
          content: `Error: ${err instanceof Error ? err.message : "Failed to get response"}`,
        };
        setMessages((prev) => [...prev, errMsg]);
      } finally {
        setLoading(false);
      }
    },
    [loading, contextTicketId],
  );
  ```

- **チケットをトリアージするAPI**

  ```ts
  const handleTriage = async () => {
    setTriageLoading(true);
    try {
      // トリアージするAPIを呼び出す！
      await api.triageTicket({
        ticketId: ticket.ticketId,
        assignee: triageAssignee,
        priority: triagePriority,
      });
      showToast(`Ticket ${ticket.ticketId} triaged successfully`, "success");
      onRefresh();
    } catch (err) {
      showToast(
        `Triage failed: ${err instanceof Error ? err.message : "Unknown error"}`,
        "error",
      );
    } finally {
      setTriageLoading(false);
    }
  };
  ```

- **チケットをエスカレーションするAPI**

  ```ts
  const handleEscalate = async () => {
    if (!escalateReason.trim()) return;
    setEscalateLoading(true);
    try {
      await api.escalateTicket({
        ticketId: ticket.ticketId,
        reason: escalateReason.trim(),
      });
      showToast(`Ticket ${ticket.ticketId} escalated`, "success");
      setEscalateReason("");
      onRefresh();
    } catch (err) {
      showToast(
        `Escalation failed: ${err instanceof Error ? err.message : "Unknown error"}`,
        "error",
      );
    } finally {
      setEscalateLoading(false);
    }
  };
  ```

# まとめ

今回はここまでになります！

バックエンドまで実装してしまえばフロントエンドからも呼び出しは普通のAPIとほぼ同じ感じですね！

次回はバックエンドを**Dockerコンテナ**化して**CDK**を使ってAWS上にデプロイするところまでを試してみたいと思います！

ここまで読んでいただきありがとうございました！