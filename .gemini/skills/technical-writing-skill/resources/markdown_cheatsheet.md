# Markdown Cheatsheet for Zenn & Qiita

## Zenn Specific Syntax

### Message Blocks (Info, Warning, Alert)
Use these to highlight important information.

```markdown
:::message
This allows you to verify your changes.
:::

:::message alert
This is a warning message. Use for critical info.
:::
```

### Details (Accordion)
Use these for long logs or optional code.

```markdown
:::details Click to see the code
Here is the hidden content.
```javascript
console.log("Hello");
```
:::
```

### Link Cards
To embed a nice link card:
```markdown
https://zenn.dev/
```
(Just paste the URL on its own line)

## Qiita Specific Syntax

### Note / Warning (New Style)
Qiita supports GitHub-style alerts.

```markdown
> [!NOTE]
> Useful information here.

> [!WARNING]
> Important warning here.
```

### Code Blocks with Filename
```markdown
```python:app.py
print("Hello Qiita")
```
```

### Task Lists
```markdown
- [x] Done task
- [ ] Todo task
```

## Universal Best Practices

### Embedding Images
- Zenn: Drag & drop to upload.
- Qiita: Drag & drop to upload.
- **Alt Text**: Always add alt text for accessibility. `![Alt Text](url)`

### Headers
- Use `#` for H1 (Title ONLY), start content with `##` (H2).
- Don't skip levels (e.g., H2 -> H4 is bad).

### Lists
- Use `-` or `*` for bullet points.
- Use `1.` for numbered lists.

### Tables
| Syntax | Description |
| ----------- | ----------- |
| Header | Title |
| Paragraph | Text |

```markdown
| Syntax | Description |
| :--- | :--- |
| Header | Title |
```
