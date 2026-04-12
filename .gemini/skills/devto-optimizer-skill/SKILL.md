---
name: devto-optimizer-skill
description: |
  Optimize and convert Zenn Flavored Markdown (ZFM) articles to Dev.to (Forem) compatible Markdown.
  Use this skill whenever the user wants to post a Zenn article to Dev.to, needs to convert markdown for cross-posting, or asks to "optimize for dev.to".
  It handles front matter conversion, Liquid tag embeds, KaTeX math blocks, callout transformations, and general formatting adjustments required by Dev.to.
---

# Dev.to Optimizer Skill

This skill transforms Zenn-specific Markdown into a polished, high-quality Dev.to post. It ensures that all technical components (embeds, math, code blocks) are correctly rendered and that the post follows Dev.to's Jekyll-style front matter and heading hierarchy conventions.

## 🚀 When to Use This Skill
- When a user wants to cross-post a Zenn article to Dev.to.
- When you see Zenn-specific notation like `@[youtube](id)` or `:::message`.
- When the user explicitly asks to "convert to dev.to" or "optimize for dev.to".

## 🛠 Preparation
Before converting, refer to the detailed conversion rules in:
`references/conversion_rules.md`

## 📝 Workflow

### Step 1: Jekyll Front Matter Construction
Dev.to requires a specific YAML header. If the source article has Zenn front matter, convert it as follows:
- `title` -> `title` (Keep it catchy! Dev.to titles often perform better with a "How to" or "Ultimate Guide" feel).
- `emoji` -> (Remove, Dev.to doesn't use these in front matter).
- `type` -> (Remove).
- `topics` -> `tags` (Max 4 tags, lowercase, no spaces).
- `published` -> `published: true` (or `false` for drafts).
- **Add** `canonical_url`: The original Zenn article URL to avoid SEO penalties.
- **Add** `cover_image`: If available.

### Step 2: Content Transformation
Apply the following surgical changes to the markdown body:

1.  **Heading Shift**:
    - **CRITICAL**: Dev.to uses the `title` as the H1. The first heading in the body MUST be **H2 (##)**.
    - If the Zenn article uses `# Header` inside the body, demote all headers by one level (# -> ##, ## -> ###, etc.).

2.  **Liquid Tag Embeds**:
    - Convert `@[youtube](id)` -> `{% youtube id %}`
    - Convert `@[twitter](id)` -> `{% twitter id %}`
    - Convert `@[gist](id)` -> `{% gist id %}`
    - Convert `@[card](url)` -> `{% link url %}`
    - For general URLs that Zenn automatically turns into cards, use `{% embed URL %}`.

3.  **Math Blocks (KaTeX)**:
    - Block: `$$ ... $$` -> `{% katex %} ... {% endkatex %}`
    - Inline: `$ ... $` -> `{% katex inline %} ... {% endkatex %}`

4.  **Callout (Message) Blocks**:
    - Convert `:::message` -> `> **Note**` + `> content`
    - Convert `:::message alert` -> `> **Warning**` + `> content`

5.  **Details/Accordions**:
    - Convert `:::details Title` -> `<details><summary>Title</summary>`
    - Convert `:::` -> `</details>`

6.  **Code Blocks**:
    - Remove filenames from language identifiers (e.g., `js:index.js` -> `javascript`).
    - Add the filename as a comment on the first line of the code block.

7.  **Mermaid Diagrams**:
    - Since Dev.to doesn't support Mermaid, wrap the Mermaid code in a `<details>` block or provide a link to the Mermaid Live Editor via `{% embed %}`.

### Step 3: Polish for Global Audience
Dev.to is a global platform. While the user may post in Japanese, consider:
- Suggesting an English translation of the title and tags.
- Ensuring links use descriptive text (avoid "Click here").
- Placing emojis at the end of sentences for better screen reader compatibility.

## 🏁 Final Output
The skill should output the complete, converted Markdown code block, ready to be pasted into the Dev.to editor.
