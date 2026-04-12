# Zenn to Dev.to Markdown Conversion Reference

This document outlines the specific conversion rules from Zenn Flavored Markdown (ZFM) to Dev.to (Forem) Markdown.

## 1. Front Matter (Jekyll style)
Dev.to requires a YAML front matter block at the top of the post.

**Dev.to Template:**
```yaml
---
title: "Article Title"
published: true
tags: tag1, tag2, tag3
cover_image: https://example.com/image.png
canonical_url: https://zenn.dev/username/articles/slug
series: Series Name (Optional)
---
```

## 2. Heading Hierarchy
- **H1 (# Header)**: The `title` in the front matter is automatically rendered as H1.
- **Article Body**: Start with **H2 (## Header)**. Do not use H1 (#) inside the body.

## 3. Embeds (Liquid Tags)
Zenn uses `@[service](id)`, while Dev.to uses `{% service id %}` or `{% embed URL %}`.

| Element | Zenn Syntax | Dev.to Syntax |
| :--- | :--- | :--- |
| **YouTube** | `@[youtube](ID)` | `{% youtube ID %}` |
| **Twitter** | `@[twitter](ID)` | `{% twitter ID %}` |
| **GitHub Gist** | `@[gist](ID)` | `{% gist ID %}` |
| **Link Card** | `@[card](URL)` | `{% link URL %}` |
| **Universal** | (Just URL) | `{% embed URL %}` |

**Recommendation**: Use `{% embed URL %}` for most external links on Dev.to.

## 4. Mathematical Formulas (KaTeX)
| Type | Zenn Syntax | Dev.to Syntax |
| :--- | :--- | :--- |
| **Block** | `$$ ... $$` | `{% katex %} ... {% endkatex %}` |
| **Inline** | `$ ... $` | `{% katex inline %} ... {% endkatex %}` |

## 5. Callouts (Messages)
Zenn's `:::message` does not exist in Dev.to. Use blockquotes with bold labels.

**Zenn:**
```markdown
:::message
Note content
:::
```

**Dev.to Alternative:**
```markdown
> **Note**
> Note content
```

**Zenn (Alert):**
```markdown
:::message alert
Warning content
:::
```

**Dev.to Alternative:**
```markdown
> **Warning**
> Warning content
```

## 6. Details / Accordions
Zenn uses `:::details`, Dev.to uses standard HTML `<details>` tags.

**Zenn:**
```markdown
:::details Title
Content
:::
```

**Dev.to:**
```html
<details>
<summary>Title</summary>
Content
</details>
```

## 7. Code Blocks
Zenn supports filenames in the language identifier. Dev.to does not.

**Zenn:**
```markdown
```js:main.js
console.log("Hello");
```
```

**Dev.to:**
```markdown
```javascript
// main.js
console.log("Hello");
```
```

## 8. Mermaid Diagrams
Zenn supports Mermaid natively. Dev.to **does not**.
- **Action**: Convert Mermaid code blocks into images or link to Mermaid Live Editor using `{% embed URL %}`.

## 9. Image Sizing
Zenn allows sizing in the markdown URL. Dev.to requires HTML.

**Zenn**: `![](url =250x)`
**Dev.to**: `<img src="url" width="250">`
