# Marp Slides — Design Principles

## Narrative Architecture

### The Golden Arc (12–15 slides)
```
1. Title
2. Agenda / Table of Contents
3–4. Problem / Background / Why this matters
5–7. Core content (solution / findings / proposal)
8–9. Evidence / data / demo / case study
10.  Summary — 3 key takeaways
11.  Next steps / Call to action
12.  Ending (thank you / contact)
```

### Adjust arc by purpose
| Purpose | Opening | Body emphasis | Close |
|---|---|---|---|
| Pitch | Hook + problem | Value + evidence | Strong CTA |
| Technical talk | Context | Architecture + demo | Next steps |
| Status report | Goal recap | Progress + issues | Decisions needed |
| Education | Why it matters | Concepts + examples | Practice / summary |

---

## Slide Design Rules

### 1 idea per slide
- If a slide has two separate topics, split it.
- Title = the one idea, body = the evidence/explanation.

### Content density
| Bad | Good |
|---|---|
| 8+ bullet points | Max 5 bullets |
| Full sentences | ≤12 words per bullet |
| Everything equally styled | **Bold** the single key phrase per bullet |
| Dense code blocks | Only essential lines, use `# ...` for omissions |

### Visual variety — alternate every 2–3 slides
- Text-heavy → visual/sparse
- Bullets → `.columns` comparison
- Prose → `.card` cards
- Claim → `.highlight` box

### Color discipline
- **1 accent color per slide** maximum (beyond the theme accent)
- Use `strong` (blue) for positive/important, `em` (amber) for warnings/caution
- Section breaks are the only slides with fully colored backgrounds in a run

---

## Slide Type Archetypes

### Title slide (`<!-- _class: title -->`)
- H1: Short, punchy title (≤8 words)
- H2: Subtitle or event/context
- P: Date, presenter, organization

### Section break (`<!-- _class: section -->`)
- H2: Section name
- P: One-line preview (optional)
- Use between major topic groups

### Content slide (default)
- H2: Slide topic (not a vague label like "Overview")
- Body: Bullets, columns, or cards
- One clear takeaway per slide

### Lead/Key message (`<!-- _class: lead -->`)
- H1: Single bold claim (≤6 words)
- Use for: "3x faster", "The key insight is...", major transitions
- No bullet points

### Data/metric slide
- Use `.number` + label pairs for KPIs
- Combine with `.columns.col-3` for 3 metrics side by side
- Always add context: what's the target? vs. when?

### Comparison slide
- `.columns` with two sides: "Before / After", "Option A / Option B"
- Left = current/problem, Right = new/solution

### Code showcase (`<!-- _class: dark -->`)
- Dark background suits code blocks visually
- Keep ≤20 lines visible; annotate with `# comments`
- Precede with a slide explaining WHAT to look for

### Ending slide (`<!-- _class: ending -->`)
- H1: "Thank you" / "ありがとうございました"
- H2: Name + contact info
- P: URL, QR code note, etc.

---

## Typography Usage

| Element | Use case |
|---|---|
| `**text**` | Most important phrase (1 per bullet) |
| `*text*` | Warning, caution, secondary note |
| `# H1` | Only on title/lead/ending slides |
| `## H2` | Slide heading — every content slide |
| `### H3` | Sub-section within a slide (use sparingly) |
| `` `code` `` | Technical terms, commands, file names |
| `> blockquote` | External quotes, pull quotes |

---

## Slide Count Guidelines

| Presentation length | Recommended slides |
|---|---|
| Lightning talk (5 min) | 8–10 |
| Standard (15–20 min) | 12–18 |
| Workshop (30–45 min) | 20–30 |
| Report / document | Unlimited, add ToC |

**Rule of thumb:** 1 minute per slide for talks. For documents meant to be read, 2–3× denser is fine.

---

## Japanese-Specific Tips

- Use `。` to end sentences in bullet points for formal register
- Use `・` for informal sub-bullets (more readable than `·`)
- Katakana technical terms (AI、クラウド) are fine; avoid romaji mixing
- Heading font weight 700–800 is especially important for Japanese legibility at small sizes
- Keep lines ≤20 characters for readability in body text at 24px
