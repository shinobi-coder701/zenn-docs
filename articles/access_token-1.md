---
title: "React + Honoで学ぶJWT認証: Access/Refresh分離と401自動リトライを実装してテストした話"
emoji: "🐑"
type: "tech"
topics: ["セキュリティ","OIDC","IDトークン","React","Hono"]
published: true
---

# はじめに

みなさん、こんにちは！

突然ですが、認証絡みのことを調べているとよく出てくる**アクセストークン**や**リフレッシュトークン**という言葉について何のために生成されているのかご存知でしょうか？

https://e-words.jp/w/%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3.html

https://qiita.com/toshi104tech/items/7930011c8a6290b97cb3

自分は全くわかっていなかったので理解するためにサンプルコードを実装しました。

本記事はそこで得られた学びをシェアするための記事になっています！

同じような疑問を持つ人にプラスになれば幸いです！

# この記事でわかること

- **Access Token** と **Refresh Token** をどう分離して扱うか
- `401 -> refresh -> 1回だけ再試行` をフロントでどう実装するか
- 「成功系」だけでなく「失敗系」までテストで担保する考え方

学習用の小さな構成でも、認証周りは設計の良し悪しが体験に直結します。  
本記事では、このリポジトリで実装した内容をベースに実装の意図とハマりどころをまとめます。

# サンプルコードのGitHub リポジトリ

https://github.com/mashharuki/accesstoken-sample

# 前提と構成

- **フロントエンド**:   
  - React
  - Vite
  - TypeScript
- **バックエンド**：
  - Hono 
  - Node.js
  - TypeScript
- **認証方式**
  - Access Token: レスポンスボディで返し、フロント状態で保持
  - Refresh Token: `HttpOnly` Cookie で保持

実装の入り口:

- `pkgs/frontend/src/contexts/auth-context.tsx`

https://github.com/mashharuki/accesstoken-sample/tree/main/pkgs/frontend/src/contexts/auth-context.tsx

- `pkgs/frontend/src/lib/api-client.ts`

https://github.com/mashharuki/accesstoken-sample/tree/main/pkgs/frontend/src/lib/api-client.ts


- `pkgs/backend/src/routes/auth.routes.ts`

https://github.com/mashharuki/accesstoken-sample/tree/main/pkgs/backend/src/routes/auth.routes.ts

- `pkgs/backend/src/services/auth.service.ts`

https://github.com/mashharuki/accesstoken-sample/tree/main/pkgs/backend/src/services/auth.service.ts

# サンプルアプリのイメージ

サンプルアプリは非常にシンプルなものです。

ログインしたらCookieの中にアクセストークンとリフレッシュトークンが埋め込まれ、有効期限内であれば再度アクセスした時に認証情報の入力が不要になるというものです！

![](/images/access_token-1/0.png)

![](/images/access_token-1/1.png)

![](/images/access_token-1/2.png)

> Cookieとは？
> 
> Webサイトがユーザーのブラウザ（ChromeやSafariなど）に、一時的に訪問データ（ID、閲覧履歴、カート内容、入力情報）を小さなファイルとして保存する仕組み

# なぜこの構成にしたか

JWT認証で理解が難しいのは「ログイン成功」より「期限切れ・不正・再試行」の挙動です。

そこで、次の方針で実装しました。

1. Tokenの責務を分離する
2. APIクライアントに自動再試行ロジックを集約する
3. 失敗時は認証状態を必ず破棄して一貫性を守る
4. テストで成功系/失敗系を明示する

# バックエンド実装の要点

## 1. ログイン時に2種類のトークンを発行

`AuthService` で **Access Token(15分)** と **Refresh Token(7日)** を発行しています。

- `pkgs/backend/src/services/auth.service.ts`

```ts
private readonly ACCESS_TOKEN_EXPIRY = 15 * 60;
private readonly REFRESH_TOKEN_EXPIRY = 7 * 24 * 60 * 60;
```

## 2. Refresh Token は HttpOnly Cookie に保存

`/auth/login` で Refresh Token を Cookie に設定します。

- `pkgs/backend/src/routes/auth.routes.ts`

```ts
// Cookieにセット
setCookie(c, "refreshToken", result.refreshToken, {
  httpOnly: true,
  secure: true,
  sameSite: "Strict",
  path: "/",
  maxAge: 604800,
});
```

## 3. 保護APIは Bearer 検証をミドルウェアで共通化

Authorization ヘッダがない/形式不正/期限切れを `401` で返す構成にしています。

https://github.com/mashharuki/accesstoken-sample/tree/main/pkgs/backend/src/middleware/auth.middleware.ts

# フロントエンド実装の要点

## 1. 認証状態は AuthContext に集約

ログイン成功時に `accessToken` と `user` を state に保存し、起動時に `refresh()` を試行します。

- `pkgs/frontend/src/contexts/auth-context.tsx`

```ts
useEffect(() => {
  refresh().catch(() => {
    // Refresh failure should leave the app unauthenticated.
  });
}, [refresh]);
```

## 2. APIクライアントで 401 の自動回復

`createApiClient` の中で `401` を検知したら `refresh()` を呼び、同じリクエストを1回だけ再実行します。

- `pkgs/frontend/src/lib/api-client.ts`

```ts
if (response.status === 401 && !hasRetried) {
  // リフレッシュ処理
  await config.refresh();
  return request<T>(method, path, body, true);
}
```

> この「1回だけ」が重要で、無限リトライを避けられます。

## 3. ルーティングガードを明示

未認証なら `/login` に飛ばし、認証済みなら `/protected` に入れる構成です。

- `pkgs/frontend/src/components/ProtectedRoute.tsx`

https://github.com/mashharuki/accesstoken-sample/tree/main/pkgs/frontend/src/components/ProtectedRoute.tsx

- `pkgs/frontend/src/App.tsx`

https://github.com/mashharuki/accesstoken-sample/tree/main/pkgs/frontend/src/App.tsx

# ハマりどころと対処

## 1. Cookieが送られない

`fetch` 側で `credentials: "include"` が必須です。  

この実装では `login`, `refresh`, `api-client` の全てで明示しています。

## 2. refresh多重実行

画面の同時リクエスト時に refresh が重複しやすいため、`refreshInProgress` でガードしています。

- `pkgs/frontend/src/contexts/auth-context.tsx`

https://github.com/mashharuki/accesstoken-sample/tree/main/pkgs/frontend/src/contexts/auth-context.tsx

## 3. 失敗時の状態不整合

refresh失敗時に token/user が残るとバグの温床になるため、`catch` で確実に `null` へ戻します。

## テストで担保していること

このリポジトリでは以下の観点をテストしています。

- バックエンド: 
  - `auth.routes`
  - `auth.service`
  - `auth.middleware`
  - `protected.routes`
  - `error-handler`
  - `env-config`
  - `cors`
- フロントエンド: 
  - `auth-context`
  - `api-client`
  - `protected-route`
  - `protected-page`
  - `login-form`
  - `routing`
  - `app-integration`

参考:

- `pkgs/backend/src/__tests__/auth.routes.test.ts`

https://github.com/mashharuki/accesstoken-sample/tree/main/pkgs/backend/src/__tests__/auth.routes.test.ts

- `pkgs/backend/src/__tests__/auth.service.test.ts`

https://github.com/mashharuki/accesstoken-sample/tree/main/pkgs/backend/src/__tests__/auth.service.test.ts

- `pkgs/frontend/src/__tests__/api-client.test.ts`

https://github.com/mashharuki/accesstoken-sample/tree/main/pkgs/frontend/src/__tests__/api-client.test.ts

- `pkgs/frontend/src/__tests__/auth-context.test.tsx`

https://github.com/mashharuki/accesstoken-sample/tree/main/pkgs/frontend/src/__tests__/auth-context.test.tsx

テストがあることで、認証フロー変更時の回帰を検知しやすくなります！

Spec駆動開発とテスト駆動開発で開発を進めればユニットテストコードもちゃんと生成してくれますよ！

# 実装してわかったトレードオフ

1. Cookie運用は実装コストが上がる  
2. ただし Token責務分離により、設計意図が明確になる  
3. 自動リトライはUXを改善するが、失敗時の終了条件が必須  
4. 学習用でも失敗系テストを先に考えると、実装が安定する

# まとめ

JWT認証は「ログイン成功」だけ作っても実運用に耐えません。  

このリポジトリでは、`Access/Refresh分離`, `401自動回復`, `失敗時の状態リセット`, `テスト担保` まで実装することで、認証の本質に近い学びを得られました！

同じテーマで学ぶ人はまず「アクセストークンやリフレッシュトークンをどこに格納するか」や「失敗系をどう扱うか」から設計すると、全体が崩れにくくなると思います！

## Xのフォローもよろしくお願いします！！

https://twitter.com/haruki_web3
