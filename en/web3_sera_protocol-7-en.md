---
title: "Building an Agent SKILL for SeraProtocol: The Ultimate Guide to On-chain FX Automation"
emoji: "💪"
type: "tech"
topics: ["ethereum", "dex", "mcp", "typescript", "claude"]
published: true
---

# Introduction

I have been sharing the charm of **Sera Protocol** through this series.

1. [[Next-Gen On-Chain FX] Why Sera Protocol Replaced AMM with CLOB: A Technical Deep Dive](https://dev.to/mashharuki/next-gen-on-chain-fx-why-sera-protocol-replaced-amm-with-clob-a-technical-deep-dive-1aoj)
2. [Hands-on with Sera Protocol's GraphQL API!](https://dev.to/mashharuki/hands-on-with-sera-protocols-graphql-api-1i2p)
3. [Let's Build a Script to Retrieve Data from Sera Protocol!](https://dev.to/mashharuki/lets-build-a-script-to-retrieve-data-from-sera-protocol-533a)
4. [Hands-on with Sera Protocol Tutorial: Mastering On-Chain Trade Execution!](https://dev.to/mashharuki/hands-on-with-sera-protocol-tutorial-mastering-on-chain-trade-execution-1l3a)
5. [Full-Throttle Sera Protocol: Building a Professional DeFi Dashboard with React](https://dev.to/mashharuki/full-throttle-sera-protocol-building-a-professional-defi-dashboard-with-react-1mkf)
6. [Building an MCP Server for Sera Protocol: The Dawn of AI-Agent Driven On-Chain FX](https://dev.to/mashharuki/building-an-mcp-server-for-sera-protocol-the-dawn-of-ai-agent-driven-on-chain-fx-le8)

For this 7th installment, I'll wrap up the series by summarizing my experience building an **Agent SKILL** for **Sera Protocol**!

I hope you enjoy reading this to the end!

# About the SKILL

The skill I created can be found in the following GitHub repository!

https://github.com/mashharuki/SeraProtocol-Sample/tree/main/.claude/skills/sera-protocol

## Contents of the Agent SKILL

This skill includes features to comprehensively support app development using Sera Protocol from four perspectives:

- Development patterns using GraphQL
- Development patterns using Smart Contracts
- Integration with Frontend Applications
- Developing MCP Servers

# Implementation Method

I used **Anthropic's** **skill-creator** to implement the SKILL!
It has been recently updated, and the quality of the generated **Agent SKILLs** is becoming a hot topic!

https://github.com/anthropics/skills/tree/main/skills

When requesting the skill creation, I provided the content of my previous blog posts and the sample code I had implemented as context.

I will share the results of how that turned out!

:::message
The model used was **Claude 4.6 Opus**.
:::

# Three Evaluation Scenarios for the Created SKILL

The update to **skill-creator** included a feature to evaluate the created skills.

Specifically, it sets up three evaluation scenarios and measures how well the requirements are met when the skill is used versus when it is not!

For this project, the following scenarios were prepared.

## Scenario 1
 
- **Prompt**:  

  ```bash
  Write a TypeScript script to get the order book information (5 bids/asks each) for the TWETH/TUSDC market from the SeraProtocol subgraph. Do not use viem, use fetch only.
  ```

- **Expected Result**: 

  ```bash
  Fetch-based TypeScript code that uses GraphQL query to get bids/asks from the depths entity. Includes the correct subgraph URL, appropriate where/orderBy/orderDirection conditions, and rawAmount_gt:0 filter.
  ```

## Scenario 2

- **Prompt**:  

  ```bash
  Tell me the full procedure for placing a limitBid on Sera Protocol. From token approve to tx submission and waiting for confirmation. Please provide a specific code example using viem. priceIndex=12000, rawAmount=500.
  ```

- **Expected Result**:  

  ```bash
  A complete flow of 1) ERC20 approve → 2) simulateContract → 3) writeContract → 4) waitForTransactionReceipt. Viem code including the correct ROUTER_ADDRESS, LimitOrderParams struct, deadline setting, and postOnly=true safety setting.
  ```

## Scenario 3

- **Prompt**: 

  ```bash
  I want to add a new tool `sera_get_chart_data` to the SeraProtocol MCP server. It's a read-only tool that returns OHLCV (candlestick) data. Which files should I change and how?
  ```
  
- **Expected Result**:   

  ```bash
  1) Add Zod schema to schemas/index.ts 2) Add chartLogs GraphQL query function to services/subgraph.ts 3) Register tool in tools/read-tools.ts. Implementation policy following existing code structure and patterns, including intervalType (1m, 5m, 15m, 1h, 4h, 1d, 1w) parameters.
  ```

# Results of the Three Evaluation Scenarios

The results were as follows!

First, the overall summary:

| Item | With SKILL | Without SKILL | Difference (Based on "With") |
| :--- | :--- | :--- | :--- |
| Average Pass Rate | 1.00 (±0.00) | 0.83 (±0.14) | **+17%** |
| Average Execution Time | 88.07s (±31.2) | 69.47s (±22.4) | +27% |
| Average Token Count | 31,483 (±7,460) | 23,423 (±5,020) | +34% |

Next, the comparison by scenario:

| Scenario | With SKILL <br/>（Pass / Time / Tokens） | Without SKILL<br/>（Pass / Time / Tokens） | Comments |
| :--- | :--- | :--- | :--- |
| graphql-orderbook | 8/8 (100%)<br/> 66.4s<br/> 21,513 | 8/8 (100%)<br/> 51.1s<br/> 18,033 | Both achieved requirements |
| limit-bid-flow | 9/9 (100%)<br/> 131.7s<br/> 39,321 | 8/9 (89%)<br/> 101.0s<br/> 30,163 | Accuracy dropped without SKILL |
| mcp-chart-tool | 7/7 (100%)<br/> 66.1s<br/> 33,614 | 5/7 (71%)<br/> 57.3s<br/> 22,072 | Largest difference |

The analysis points are summarized below:

- **"With SKILL" achieved 100% in all 3 scenarios (24/24 assertions).**
- "Without SKILL" lost points in Scenarios 2 and 3 (missing market info acquisition, incorrect approve expression, lack of polling, lack of postOnly safety measure, confusing `candles`/`chartLogs`, missing `1w` interval).
- Scenario 1 had low discriminative power, as both achieved perfect scores.
- While "With SKILL" increased token consumption, it improved the accuracy and comprehensiveness of implementations based on domain-specific knowledge.

The accuracy is quite impressive!

## Comparison of Actually Generated Code

Next, let's look at the code actually generated for each scenario.

### Scenario ①

In this scenario, we tried implementing a simple script that gets SeraProtocol data using only GraphQL without `viem`. Both patterns seem to meet the requirements!

- **With SKILL**

  https://github.com/mashharuki/SeraProtocol-Sample/tree/main/sera-protocol-workspace/iteration-1/eval-1-graphql-orderbook/with_skill

- **Without SKILL**

  https://github.com/mashharuki/SeraProtocol-Sample/tree/main/sera-protocol-workspace/iteration-1/eval-1-graphql-orderbook/without_skill

### Scenario ②

Next is the result for the scenario including write-type processing using `viem`. You can see that the accuracy drops in the pattern where the SKILL is not used.

In the "With SKILL" case, the logic to simulate transaction processing is implemented very carefully.

- **With SKILL**

  https://github.com/mashharuki/SeraProtocol-Sample/tree/main/sera-protocol-workspace/iteration-1/eval-2-limit-bid-flow/with_skill

- **Without SKILL**

  https://github.com/mashharuki/SeraProtocol-Sample/tree/main/sera-protocol-workspace/iteration-1/eval-2-limit-bid-flow/without_skill

### Scenario ③

Finally, for the most difficult MCP server implementation, the results were even more clearly divided between "With SKILL" and "Without SKILL."

When the SKILL was present, it output not only build and test commands but also how to verify operations using the **MCP Inspector**.

- **With SKILL**

  https://github.com/mashharuki/SeraProtocol-Sample/tree/main/sera-protocol-workspace/iteration-1/eval-3-mcp-chart-tool/with_skill

- **Without SKILL**

  https://github.com/mashharuki/SeraProtocol-Sample/tree/main/sera-protocol-workspace/iteration-1/eval-3-mcp-chart-tool/without_skill

# Summary

I tried turning everything I've researched and all the sample code I've built into a SKILL!

It was confirmed that the more complex the implementation method, the more the SKILL demonstrates its power.

Sera Protocol currently only supports testnets, so why not master development on Sera Protocol using SKILLs before the mainnet launch?

https://sera.cx/

Thank you for reading this far!
