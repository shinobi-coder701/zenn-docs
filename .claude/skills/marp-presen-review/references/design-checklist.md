# Visual Design Verification Checklist

Use this checklist to systematically audit each slide's visual quality.

## Per-Slide Checklist

### Layout
- [ ] Single clear focal point exists
- [ ] Elements aligned to implicit grid
- [ ] Whitespace ≥ 30% of slide area
- [ ] No content touching slide edges (respect 48px+ padding)
- [ ] Comparison content uses `.columns` layout
- [ ] Process/steps content uses `.steps` layout
- [ ] KPI/metrics use `.number` component

### Typography
- [ ] `## H2` title present on every content slide
- [ ] `# H1` used ONLY on title/lead/ending slides
- [ ] Exactly 1 `**bold**` key phrase per bullet
- [ ] No more than 5–6 bullets
- [ ] Each bullet ≤ 12 words (JP: ≤ 20 characters)
- [ ] Bullet items are grammatically parallel
- [ ] No orphan headings (heading without content below)

### Color
- [ ] Max 1 accent color per slide (beyond base palette)
- [ ] Card colors match semantics (accent=info, warn=caution, success=good, danger=risk)
- [ ] Text has sufficient contrast against background
- [ ] Dark slides (`dark`/`title`/`ending`) use light text only
- [ ] No color used purely for decoration

### Content
- [ ] No placeholder text ("ここに説明を入れる", "TBD", "TODO")
- [ ] Numbers are specific, not vague ("30%削減" not "大幅に削減")
- [ ] Sources cited for data/statistics
- [ ] Technical terms use inline code formatting

## Deck-Level Checklist

### Structure
- [ ] Title slide present with H1, subtitle, date/presenter
- [ ] Agenda/ToC slide follows title (for 10+ slide decks)
- [ ] Section break slides separate major topics
- [ ] Summary slide with ≤ 3 key takeaways
- [ ] CTA or Next Steps slide before ending
- [ ] Ending slide with contact/URL info

### Flow
- [ ] No 3+ consecutive slides with same layout type
- [ ] Visual type changes every 2–3 slides
- [ ] Slide count matches time allocation (~1 min/slide)
- [ ] Total slides: 8–10 (5min), 12–18 (15–20min), 20–30 (30–45min)

### Consistency
- [ ] Same heading level for same-tier content throughout
- [ ] Bold usage pattern consistent across all slides
- [ ] Card style consistent (don't mix `.accent` meanings)
- [ ] Slide class usage appropriate (title/section/lead/dark/ending)

### Technical
- [ ] Frontmatter complete: marp, theme, paginate, size, html, style
- [ ] CSS embedded in style block (self-contained)
- [ ] All `<div>` tags properly closed
- [ ] `<!-- _class: X -->` directives use valid class names
- [ ] Slide separators `---` on own line with blank lines around them

## Quick Severity Classification

| Finding | Severity |
|---------|----------|
| No Marp frontmatter | CRITICAL |
| Placeholder text in final output | HIGH |
| 7+ bullets on a slide | HIGH |
| No bold key phrases | HIGH |
| 4+ consecutive same-layout slides | HIGH |
| Missing title or ending slide | MEDIUM |
| Topic-label titles (not message-driven) | MEDIUM |
| Unclosed HTML div | MEDIUM |
| Minor alignment issue | LOW |
| Could benefit from layout component | LOW |
| Slight word count excess (13–15 words) | LOW |
