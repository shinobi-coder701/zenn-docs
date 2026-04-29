---
title: "Unleashing IronClaw: The Secure, Rust-Based AI Agent Framework by NearAI"
published: true
tags: ai, near, rust, security
canonical_url: https://zenn.dev/harukikondo/articles/nearai_ironclaw-1
cover_image: https://raw.githubusercontent.com/harukikondo/zenn-docs/main/images/nearai_ironclaw-1/0.png
---

## Introduction: The Rise of Secure AI Agents

By now, most of you in the AI space have probably heard of **OpenClaw**. It’s the AI Agent framework that took the community by storm in early 2026.

But have you heard of **IronClaw**?

While OpenClaw focused on accessibility and rapid prototyping, **IronClaw** is its security-hardened sibling, built from the ground up in **Rust**. Developed by the team at **Near AI**, it’s designed for developers who need autonomous agents that can handle sensitive data—like passwords and API keys—without exposing them to the LLM.

In this post, we’ll dive deep into what makes IronClaw the "Iron Man suit" for your AI agents.

## What is IronClaw?

![IronClaw Overview](https://raw.githubusercontent.com/harukikondo/zenn-docs/main/images/nearai_ironclaw-1/0.png)

**IronClaw** is an open-source AI Agent framework developed by **Near AI**. It is designed to run in secure environments like **NEAR AI Cloud**, allowing agents to autonomously operate tools (Google Workspace, GitHub, etc.) while keeping user credentials strictly confidential.

### About Near AI
[Near AI Official Website](https://www.near.org/ai)

Near AI started as a prominent Layer 1 blockchain project (once considered a potential "Ethereum killer"). Today, it has evolved into an AI-native public blockchain. 

Fun fact: One of its founders, Illia Polosukhin, is a co-author of the seminal **"Attention Is All You Need"** paper—the research that introduced the **Transformer** architecture to the world.

## Key Features of IronClaw

Running IronClaw on the NEAR AI Cloud provides several hardware-level security benefits that standard frameworks lack:

- **TEE (Trusted Execution Environment)**: Agents run in encrypted, isolated enclaves.
- **Data Confidentiality**: Memory data is always encrypted. Not even the cloud provider (NEAR AI) can peek into your conversations or memory.
- **Verifiability**: Hardware-level isolation (like GPU attestation) ensures private and verifiable computing.
- **Secrets Protection**: An "Encrypted Vault" integrates with the infrastructure to inject credentials into tools without the LLM ever seeing the raw API keys.

### Capabilities at a Glance

| Category | Feature | Benefit |
| --- | --- | --- |
| **Security** | Encrypted Vault / WASM Isolation | Secrets are stored safely; tools run in sandboxes. |
| **Connectivity** | Multi-channel Support | Operate via Terminal, Telegram, Discord, or Webhooks. |
| **Memory** | Persistent Memory | Agents remember past conversations and documents for RAG. |
| **Automation** | Scheduled Jobs | Automate tasks like "Generate a report every morning at 9 AM." |
| **Extensibility** | Tool Ecosystem | Easily add tools for Google Docs, Calendar, GitHub, and Web Search. |

## The 4-Layer Security Architecture

IronClaw employs a "Defense in Depth" strategy, ensuring data passes through four independent protection layers before reaching any external service.

1.  **Safety Layer**: Prevents prompt injection, sanitizes content, and scans for over 15 types of secret patterns.
2.  **WASM Sandbox**: A lightweight execution environment for tools with strict memory limits (default 16MB) and "Fuel Metering" to prevent infinite loops.
3.  **Docker Sandbox**: Container-level isolation for complex jobs and untrusted script execution.
4.  **Secret Management**: A "Zero-Exposure" model using AES-256-GCM encryption where credentials are only injected at the host boundary.

### WASM vs. Docker Sandbox: Which is which?

| Feature | WASM Sandbox | Docker Sandbox |
| --- | --- | --- |
| **Runtime** | `wasmtime` | Container Virtualization |
| **Primary Use** | Secure Tool Execution | Code Execution, Builds, Scripts |
| **Footprint** | Extremely Lightweight | Moderate Resource Usage |
| **Limits** | Fuel Metering (Instructions) | CPU / Memory (Standard) |
| **Secret Access** | Injected via Proxy | Environment Variables / Volumes |

## Getting Started with IronClaw

### 1. Access the Agent Dashboard
Head over to the [Near AI Agent Dashboard](https://agent.near.ai/).

### 2. Choose Your Plan
![Plan Selection](https://raw.githubusercontent.com/harukikondo/zenn-docs/main/images/nearai_ironclaw-1/6.png)
The **Starter** plan is free and perfect for getting your feet wet.

### 3. One-Click Deployment
Click the **Deploy** button to spin up your IronClaw instance on NEAR AI Cloud.
![Deployment](https://raw.githubusercontent.com/harukikondo/zenn-docs/main/images/nearai_ironclaw-1/1.png)
The default LLM is typically set to **Qwen**, but you can customize this.

### 4. Experiment!
![Dashboard](https://raw.githubusercontent.com/harukikondo/zenn-docs/main/images/nearai_ironclaw-1/2.png)
Try chatting with your agent, adding new Skills, or connecting MCP (Model Context Protocol) servers.

## Conclusion

With a team led by a Transformer co-author, it’s no surprise that IronClaw is a masterclass in combining AI utility with rigorous security. Its deployment process is arguably one of the smoothest in the ecosystem.

If you’re looking to build an agent that does more than just chat—an agent you can actually trust with your digital life—IronClaw is the way to go.

Thanks for reading!

## Join the Hackathon!
Near AI is proud to sponsor the **OpenClaw Hackathon** on May 2nd! 

[Register Here](https://luma.com/zw01ink4?tk=VucpiH)

Using IronClaw in your project will definitely put you on the radar for the security-focused tracks. We can't wait to see what you build!

## References
- [IronClaw Official Site](https://docs.ironclaw.com)
- [Developer Documentation](https://docs.ironclaw.com)
- {% github nearai/ironclaw %}
- [Near AI Agent Dashboard](https://agent.near.ai/)
