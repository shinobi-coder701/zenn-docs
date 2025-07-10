---
title: "MCP動かすときの環境変数どう読み込ませてる？"
emoji: "🔐"
type: "tech" 
topics: ["生成AI", "MCP", "VSCode", "環境変数", "AIエージェント"]
published: false
---

## はじめに

突然ですが、皆さんMCP動かす時に環境変数ってどうやって設定していますか？？

`mcp.json`とかの **設定ファイルにAPIキーとかベタ書きされて動かされている方も多いのではないでしょうか** ？！

僕もベタ書きして動かしてました！！！

今回は設定ファイルにベタ書きしなくても良い方法を見つけることができたのでそれをシェアしたいと思います！！

ぜひ最後まで読んでいってください！！

## 🚀結論 envfile プロパティを使おう！！

設定方法だけを手短に知りたい方は以下のGitHubリポジトリの `.vscode/mcp.example.json` をご覧ください！！

https://github.com/AO-protocol/overflow2025

全然知らなかったのですが、 VS Codeのドキュメントに以下のようなものを見つけました！

https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_configuration-format

そしてそこには知りたかった **環境変数の取り扱い** 方についてまとめられているではありませんか！

`envfile`プロパティなるものがあり、これを使えば良いとのこと！！

## envfileプロパティを使って環境変数を読み込んでみた！

`envfile`を使ったことでmcpの設定ファイルが以下のように変わりました！！

`${workspaceFolder}/pkgs/mcp/.env` と指定することでプロジェクトの任意のディレクトリ配下にある `.env` を読み込ませることができます！！

- **Before**

  ```json
  {
    "inputs": [],
    "servers": {
      "x402-walrus": {
        "command": "node",
        "args": [
          "${workspaceFolder}/pkgs/mcp/dist/index.js"
        ],
        "env": {
          "RESOURCE_SERVER_URL": "http://localhost:4021",
          "ENDPOINT_PATH": "/download",
          "PRIVATE_KEY": "<your private key>"
        }
      }
    }
  }
  ```

- **After**

  ```json
  {
    "inputs": [],
    "servers": {
      "x402-walrus": {
        "command": "node",
        "args": [
          "${workspaceFolder}/pkgs/mcp/dist/index.js"
        ],
        "envFile": "${workspaceFolder}/pkgs/mcp/.env"
      }
    }
  }
  ```

<br/>

これなら安心してチーム間でもmcpの設定ファイルが共有できますね！！

素晴らしい！！！

## まとめ

特にWeb3系のmcpだと秘密鍵を取り扱うことも多いため、流石にベタ書きするのはまずいよな〜って思っていました...笑。

なんとかいい方法ないか考えていたところこの設定ファイルを教えてもらい、これは良さそうだということで記事化しました！！

**皆さんもぜひお試しあれ** ！！

ここまで読んでいただきありがとうございました！！

## 余談

今回共有したGitHubリポジトリの詳しい実装については以下のブログ記事で紹介しています！

https://zenn.dev/mashharuki/articles/x402_walrus_mcp

よろしければそちらもご参照ください〜！