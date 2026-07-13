# Scoring Rubric — 10-Axis Evaluation (100 Points)

## Scoring Method

Raw score = sum of (axis score x weight). Normalize: `total = raw / 130 * 100`.

## Axis 1: Message Clarity (Weight x2)

Each slide should convey exactly ONE clear message.

| Score | Criteria |
|-------|----------|
| 10 | Every slide has a single, immediately obvious message. No ambiguity. |
| 8 | 90%+ slides have clear single messages. Minor cases of dual topics. |
| 6 | Most slides have a message, but 3–4 slides mix multiple ideas. |
| 4 | Half the slides lack focus. Multiple ideas compete for attention. |
| 2 | Most slides are unfocused. Audience cannot identify the point. |

**Check**: Read each slide for 3 seconds. Can you state its message in one sentence?

**Common deductions**:
- Slide contains 2+ unrelated ideas → -2
- No discernible core message → -3
- Placeholder text ("ここに説明") → -4

## Axis 2: Story Structure (Weight x2)

The deck should follow a coherent narrative arc.

| Score | Criteria |
|-------|----------|
| 10 | Clear arc: Opening hook → Problem → Solution → Evidence → CTA. Slide titles alone tell the story. |
| 8 | Good flow with minor gaps. One section feels disconnected. |
| 6 | Basic structure exists but transitions are weak. No clear climax. |
| 4 | Random slide order. No sense of progression. |
| 2 | Slides could be shuffled without losing coherence. No narrative. |

**Check**: Read only slide titles in order. Do they form a logical story?

**Frameworks to evaluate against** (see `story-evaluation.md` for details):
- PREP (Point-Reason-Example-Point): Best for proposals
- Problem-Solution: Best for improvement proposals
- SDS (Summary-Details-Summary): Best for reports
- AS-IS → TO-BE: Best for transformation plans
- Why → What → How: Best for vision/kickoff
- Comparative Analysis: Best for decision support

**Common deductions**:
- No clear opening hook → -2
- Missing CTA or next steps → -1
- Abrupt topic jumps without transitions → -2
- Conclusion doesn't connect back to opening → -1

## Axis 3: Visual Hierarchy (Weight x1.5)

The eye should be guided to the most important element first.

| Score | Criteria |
|-------|----------|
| 10 | Size, color, and position create unmistakable priority order. Bold key phrases work perfectly. |
| 8 | Hierarchy mostly clear. 1–2 slides have competing elements. |
| 6 | Some hierarchy exists but inconsistent across slides. |
| 4 | Flat design — everything has equal visual weight. |
| 2 | Hierarchy is inverted (less important elements are more prominent). |

**Check**: Squint at each slide. What do you see first? Is it the most important element?

**Common deductions**:
- Multiple bold phrases per bullet → -2
- No bold/emphasis anywhere → -2
- Title smaller than body text → -3
- Key message buried in body text → -2

## Axis 4: Information Density (Weight x1.5)

Less is more. Respect the audience's cognitive load.

| Score | Criteria |
|-------|----------|
| 10 | Every slide: ≤5 bullets, ≤12 words each, ≤150 chars total body. Breathing room. |
| 8 | Mostly within limits. 1–2 slides slightly exceed. |
| 6 | Several slides have 6–7 bullets or 15+ word items. Feels dense. |
| 4 | Most slides are text walls. 8+ bullets common. |
| 2 | Slides are paragraphs of text. No bullet structure. |

**Thresholds**:
- Bullets per slide: ≤5 (ideal), 6 (acceptable), 7+ (too many)
- Words per bullet: ≤12 (ideal), 15 (acceptable), 16+ (too long)
- Total characters per slide body: ≤150 (ideal), 200 (acceptable), 201+ (dense)
- Japanese: ≤20 characters per line at 24px

**Common deductions**:
- Slide with 7+ bullets → -2 per occurrence
- Bullet exceeding 15 words → -1 per occurrence
- Full paragraph instead of bullets → -3

## Axis 5: Layout & Whitespace (Weight x1)

Professional layouts use grids, alignment, and generous margins.

| Score | Criteria |
|-------|----------|
| 10 | Consistent grid usage. Columns, cards, and steps used appropriately. 30%+ whitespace. |
| 8 | Good layout variety. Minor alignment issues. |
| 6 | Basic layouts. Some slides feel cramped. |
| 4 | No layout components used. Text-only slides throughout. |
| 2 | Chaotic placement. No visual structure. |

**Check**:
- Are `.columns`, `.card`, `.steps`, etc. used where appropriate?
- Is whitespace consistent across slides?
- Do comparison slides use two-column layout?
- Do process slides use `.steps`?

## Axis 6: Typography (Weight x1)

Consistent, readable type treatment across the deck.

| Score | Criteria |
|-------|----------|
| 10 | Font hierarchy clear (H1 > H2 > body). Bold = accent only. Emphasis consistent. |
| 8 | Good typography. Minor inconsistencies in heading levels. |
| 6 | Readable but heading levels are misused (H3 for titles, etc.). |
| 4 | Inconsistent fonts/sizes. Hard to distinguish hierarchy. |
| 2 | Typography is chaotic. Multiple uncoordinated styles. |

**Rules**:
- `# H1` → Title / Lead / Ending slides ONLY
- `## H2` → Every content slide must have one
- `**bold**` → Exactly 1 key phrase per bullet
- `*italic*` → Warnings or caveats only
- `` `code` `` → Technical terms only
- Bullet items are parallel in grammar (all nouns, or all verbs)

## Axis 7: Color & Contrast (Weight x1)

Limited palette, meaningful color usage, sufficient contrast.

| Score | Criteria |
|-------|----------|
| 10 | ≤3 colors + neutral. Each color has consistent meaning. WCAG AA contrast. |
| 8 | Good color usage. Minor inconsistencies in color meaning. |
| 6 | Colors are used but without consistent semantic meaning. |
| 4 | Too many colors. No clear palette. Some low-contrast areas. |
| 2 | Rainbow slides. Colors distract rather than communicate. |

**70-25-5 Rule**:
- 70%: Base (white/dark background)
- 25%: Primary accent (e.g., `--accent: #3b82f6`)
- 5%: Secondary accent (e.g., `--accent-warm: #f59e0b`)

**Card color semantics**:
- `.accent` (blue) → Information, features
- `.warn` (amber) → Caution, attention
- `.success` (green) → Achievement, positive
- `.danger` (red) → Risk, critical

## Axis 8: Visual Variety (Weight x1)

Alternate slide types to maintain engagement.

| Score | Criteria |
|-------|----------|
| 10 | Every 2–3 slides changes visual type. Mix of bullets, cards, metrics, code, images. |
| 8 | Good variety. One stretch of 3 similar slides. |
| 6 | Some variety but 4+ consecutive bullet-only slides exist. |
| 4 | Monotonous. Same layout repeated throughout. |
| 2 | Every slide is identical bullet format. |

**Slide type catalog**:
- Bullet list (default)
- Two/three column (`.columns`)
- Card grid (`.card`)
- Metric/KPI (`.number`)
- Highlight (`.highlight`)
- Steps/process (`.steps`)
- Code block (`dark` class)
- Table
- Image + text
- Lead (big message)
- Section break

**Rule**: No 3 consecutive slides of the same type.

## Axis 9: Slide Titles (Weight x1)

Titles should be messages (assertions), not topic labels.

| Score | Criteria |
|-------|----------|
| 10 | Every title is an assertion. Reading titles only tells the full story. |
| 8 | 80%+ titles are message-driven. A few are still topic labels. |
| 6 | Mix of messages and labels. Story only partially readable from titles. |
| 4 | Most titles are labels ("Background", "Data", "Summary"). |
| 2 | Titles are generic or missing. |

**Examples**:
- NG: `## 売上実績` (topic label)
- OK: `## Q3売上は目標比120%を達成` (message/assertion)
- NG: `## 背景` (generic label)
- OK: `## 市場シェアの低下が3四半期連続で進行中` (concrete message)
- NG: `## まとめ` (generic)
- OK: `## 3つの施策で年間30%のコスト削減を実現` (specific conclusion)

## Axis 10: Technical Quality (Weight x1)

Valid Marp syntax, correct directives, no broken HTML.

| Score | Criteria |
|-------|----------|
| 10 | Perfect frontmatter. All classes valid. HTML components well-formed. Renderable. |
| 8 | Minor issues (missing `html: true` but no HTML used). |
| 6 | Some broken HTML or invalid class names. Still renders. |
| 4 | Missing frontmatter fields. Several broken components. |
| 2 | File doesn't render as Marp at all. |

**Checklist**:
- [ ] `marp: true` in frontmatter
- [ ] `theme:` specified
- [ ] `paginate: true` present
- [ ] `size: 16:9` present
- [ ] `html: true` if any `<div>` used
- [ ] All `<!-- _class: X -->` use valid class names
- [ ] No unclosed `<div>` tags
- [ ] Slide separators `---` are on their own line
- [ ] CSS is embedded in `style:` block (self-contained file)
