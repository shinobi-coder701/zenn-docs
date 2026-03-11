---
title: "vinextを試してみた！"
emoji: "⚡️"
type: "tech"
topics: ["cloudflare", "workers", "serverless", "javascript", "nextjs"]
published: true
---

# はじめに

先日**CloudFlare**から**vinext**なるものが発表されました！

https://blog.cloudflare.com/ja-jp/vinext/

**Next.js**と比較して最大57%バンドルサイズが小さくなるとのことで話題になってしました。

**vinext**は**Next.js**を**vite**ベースで再構築したものになります！

# サンプルコード

今回試したコードは以下に格納してあります！

https://github.com/mashharuki/cloudflare-workers-sample/tree/main/vinext-sample

# vinextのはじめ方

まずNext.jsのアプリを作ります。

```bash
bun create next-app@latest
```

デフォルトのプロジェクトを作ったら**vinext**プロジェクトにマイグレーションさせます！

```bash
bunx vinext init
```

これで準備OKです！！

正常に終了したらアプリを起動させることができます！

```bash
bunx run dev:vinext 
```

![](/images/cloudflare_worker-1/0.png)

# Cloudflare Workersにデプロイしてみよう！

では次にCloudflare Workersにデプロイしてみたいと思います！

ここでハマりまして、設定ファイル`vite.config.ts`を以下のように修正する必要があります。

```ts
import { cloudflare } from "@cloudflare/vite-plugin";
import vinext from "vinext";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [
    vinext(),
    cloudflare({
      viteEnvironment: { 
        name: "rsc", 
        childEnvironments: ["ssr"] 
      },
    })
  ],
});
```

これで準備OKです！

以下のコマンドでデプロイできます！

```bash
bunx vinext deploy
```

問題なければ**Cloudflare Workers**にデプロイされてローカルと同じような画面が描画されるはずです！

簡単ですね！

今回はここまでになります！

## 参考文献

- [Cloudflare Developers](https://developers.cloudflare.com/) - 公式ドキュメントが何よりの教科書。
- [Hono Documentation](https://hono.dev/) - エッジ開発の最高の相棒。
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Wrangler CLI Reference](https://developers.cloudflare.com/workers/wrangler/commands/)
- [GitHub - vinext](https://github.com/cloudflare/vinext)