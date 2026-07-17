#!/usr/bin/env python3
"""AI臭 lint — Markdown 日本語文書から機械検出できるAI臭パターンを洗い出す。

使い方:
    python3 ai_smell_lint.py 記事.md [記事2.md ...]

出力はすべて「疑いの提示」であり、エラーではない。
検出→文脈で判断→修正→再lint のループで使うこと（SKILL.md 参照）。
標準ライブラリのみで動く。終了コードは常に 0。
"""

import re
import statistics
import sys
import unicodedata
from pathlib import Path

# 文の述語的な末尾（これらで終わらなければ体言止め候補とみなす簡易判定）
PREDICATE_ENDINGS = (
    "です", "ます", "でした", "ました", "ません", "ですね", "ますね",
    "だ", "である", "だった", "する", "した", "なる", "なった", "いる", "いた",
    "ある", "あった", "れる", "れた", "られる", "ない", "たい", "しまう", "ください",
    "だろう", "でしょう", "みよう", "しよう", "ほしい", "よい", "いい",
)

VERBOSE_PATTERNS = [
    (r"することができま", "「〜することができます」→「〜できます」で十分"),
    (r"についてご紹介しま", "定型オープニング。いきなり本題に入る"),
    (r"を活用(?:し|す)", "「活用」の乱用の疑い。「使う」で足りないか確認"),
    (r"することが可能で", "翻訳調。「〜できます」に直す"),
    (r"という点において", "翻訳調。「〜では」に直す"),
]

CONNECTIVES = ["さらに", "加えて", "また", "一方で", "そして", "これにより", "このように"]

DASH_CHARS = "—―─–"


def is_japanese_prose(line):
    return bool(re.search(r"[ぁ-んァ-ヶ一-龠]", line))


def strip_document(text):
    """frontmatter とコードブロックを除いた行リスト (行番号, 内容) と、
    言語指定なしコードフェンスの行番号を返す。"""
    lines = text.splitlines()
    prose = []
    naked_fences = []
    in_code = False
    i = 0
    # frontmatter をスキップ
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                i = j + 1
                break
    while i < len(lines):
        line = lines[i]
        fence = re.match(r"^\s*(```|~~~)(.*)$", line)
        if fence:
            if not in_code:
                if not fence.group(2).strip():
                    naked_fences.append(i + 1)
                in_code = True
            else:
                in_code = False
            i += 1
            continue
        if not in_code:
            prose.append((i + 1, line))
        i += 1
    return prose, naked_fences


def split_sentences(prose_lines):
    """散文行から (行番号, 文) のリストを作る。見出し・箇条書き・表・画像は除外。"""
    sentences = []
    for lineno, line in prose_lines:
        s = line.strip()
        if not s or s.startswith(("#", "- ", "* ", "+ ", ">", "|", "![", ":::")):
            continue
        if re.match(r"^\d+\.\s", s):
            continue
        if not is_japanese_prose(s):
            continue
        # インラインコードとリンクの URL 部分をリズム計測から外す
        s = re.sub(r"`[^`]*`", "コード", s)
        s = re.sub(r"\]\([^)]*\)", "]", s)
        for sent in re.split(r"(?<=[。！？])", s):
            sent = sent.strip()
            if len(sent) >= 2:
                sentences.append((lineno, sent))
    return sentences


def sentence_core(sent):
    return sent.rstrip("。！？」）)』.").strip()


def is_taigendome(sent):
    """体言止めの簡易判定。末尾が述語で終わらず、名詞相当で止まる文。

    漢字・カタカナ・英数字終わりに加え、「仕組み」「強み」「高さ」のような
    漢字+み/さ で終わる転成名詞も体言止めとして拾う。"""
    core = sentence_core(sent)
    if not core:
        return False
    if any(core.endswith(e) for e in PREDICATE_ENDINGS):
        return False
    if re.search(r"[一-龠][みさ]$", core):
        return True
    last = core[-1]
    cat = unicodedata.name(last, "")
    return ("CJK UNIFIED" in cat) or ("KATAKANA" in cat) or last.isascii() and last.isalnum()


class Report:
    def __init__(self):
        self.findings = []  # (severity, rule, message, examples)

    def add(self, rule, message, examples=None):
        self.findings.append((rule, message, examples or []))

    def dump(self, path):
        print(f"\n{'=' * 60}")
        print(f"AI臭 lint: {path}")
        print("=" * 60)
        if not self.findings:
            print("疑い箇所は検出されなかった。リズム層は目視でも確認すること。")
            return
        for rule, message, examples in self.findings:
            print(f"\n[{rule}] {message}")
            for ex in examples[:5]:
                print(f"    {ex}")
            if len(examples) > 5:
                print(f"    ... 他 {len(examples) - 5} 件")
        print("\n※ これはエラーではなく「疑いの提示」。文脈で判断し、意図的な表現は残すこと。")


def lint_vocabulary(prose_lines, report):
    dash_hits, excl_lines, colon_heads, pair_bullets = [], [], [], []
    excl_count = bold_count = 0
    total_chars = 0

    for lineno, line in prose_lines:
        total_chars += len(line)
        for ch in DASH_CHARS:
            if ch in line:
                dash_hits.append(f"L{lineno}: {line.strip()[:60]}")
                break
        n = line.count("！") + line.count("!") - line.count("![")
        if n > 0 and is_japanese_prose(line):
            excl_count += n
            excl_lines.append(f"L{lineno}: {line.strip()[:60]}")
        bold_count += len(re.findall(r"\*\*[^*]+\*\*", line))
        if re.match(r"^\s*#{1,6}\s.*[：:]", line):
            colon_heads.append(f"L{lineno}: {line.strip()[:60]}")
        if re.match(r"^\s*[-*+]\s+[^:：]{1,25}[：:]\s*\S", line):
            pair_bullets.append(f"L{lineno}: {line.strip()[:60]}")

    if dash_hits:
        report.add("dash", f"ダッシュ区切りを{len(dash_hits)}箇所検出。読点か文分割に", dash_hits)
    if excl_count >= 4:
        report.add("exclamation", f"「！」が{excl_count}回。本当に強調したい箇所だけに", excl_lines)
    if total_chars and bold_count / max(total_chars, 1) * 1000 > 3:
        report.add("bold-overuse", f"太字が{bold_count}箇所と多め。基本はベタ書きに")
    if len(colon_heads) >= 2:
        report.add("colon-heading", f"コロン構造の見出しが{len(colon_heads)}件", colon_heads)
    if len(pair_bullets) >= 4:
        report.add("label-colon-list", f"「項目名: 説明」形式の箇条書きが{len(pair_bullets)}件。ベタ書きか見出し化を検討", pair_bullets)

    for pat, msg in VERBOSE_PATTERNS:
        hits = [f"L{ln}: {l.strip()[:60]}" for ln, l in prose_lines if re.search(pat, l)]
        if hits:
            report.add("verbose-phrase", f"{msg}（{len(hits)}件）", hits)


def lint_rhythm(sentences, report):
    if len(sentences) < 8:
        return
    lengths = [len(sentence_core(s)) for _, s in sentences]
    mean = statistics.mean(lengths)
    stdev = statistics.pstdev(lengths)
    cv = stdev / mean if mean else 0
    if cv < 0.38:
        report.add(
            "low-burstiness",
            f"文長が均質（平均{mean:.0f}字、変動係数{cv:.2f}）。最も普遍的なAI臭。"
            "短文を打ち込む・2文を結合するなどで揺れを作る",
        )

    taigen = [(ln, s) for ln, s in sentences if is_taigendome(s)]
    rate = len(taigen) / len(sentences)
    if rate == 0:
        report.add(
            "no-taigendome",
            "体言止めがゼロ。実測ではゼロこそAI臭（人間の約60%は使う）。効く場所に数回だけ置く",
        )
    elif rate > 0.25:
        report.add(
            "taigendome-overuse",
            f"体言止めが{len(taigen)}/{len(sentences)}文と多い。連続すると標語化する",
            [f"L{ln}: {s[:40]}" for ln, s in taigen],
        )

    dewanaku = [f"L{ln}: {s[:50]}" for ln, s in sentences if "ではなく" in s]
    if len(dewanaku) >= 3:
        report.add("dewanaku-repeat", f"「〜ではなく」の対比構文が{len(dewanaku)}回。素直に肯定形で言えないか", dewanaku)

    for conn in CONNECTIVES:
        heads = [f"L{ln}: {s[:40]}" for ln, s in sentences if s.startswith(conn)]
        if len(heads) >= 3:
            report.add("connective-repeat", f"文頭の「{conn}」が{len(heads)}回。流れでつなげないか", heads)


def lint_paragraph_uniformity(prose_lines, report):
    paras, current = [], []
    for _, line in prose_lines:
        s = line.strip()
        if not s:
            if current:
                paras.append(current)
                current = []
            continue
        if s.startswith(("#", "- ", "* ", "+ ", ">", "|", "![")):
            continue
        if is_japanese_prose(s):
            current.append(s)
    if current:
        paras.append(current)

    counts = [sum(len(re.findall(r"[。！？]", l)) for l in p) for p in paras]
    counts = [c for c in counts if c >= 2]
    if len(counts) >= 4:
        mode = statistics.mode(counts)
        share = counts.count(mode) / len(counts)
        if share >= 0.6 and mode >= 3:
            report.add(
                "uniform-paragraphs",
                f"段落の多く（{counts.count(mode)}/{len(counts)}）がきっかり{mode}文。"
                "内容の重さに段落の長さを従わせる",
            )


def lint_file(path):
    text = Path(path).read_text(encoding="utf-8")
    prose_lines, naked_fences = strip_document(text)
    sentences = split_sentences(prose_lines)
    report = Report()
    lint_vocabulary(prose_lines, report)
    lint_rhythm(sentences, report)
    lint_paragraph_uniformity(prose_lines, report)
    if naked_fences:
        report.add(
            "code-fence-no-lang",
            f"言語指定のないコードブロックが{len(naked_fences)}件",
            [f"L{n}" for n in naked_fences],
        )
    report.dump(path)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    for path in sys.argv[1:]:
        lint_file(path)


if __name__ == "__main__":
    main()
