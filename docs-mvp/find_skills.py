"""
Công cụ tìm skill liên quan đến keyword trong docs-mvp/key-work.md.

Cách chạy:
    python docs-mvp/find_skills.py

Kết quả ghi vào: docs-mvp/define_all_skill.md
"""

import re
import sys
from pathlib import Path

# Windows terminal thường dùng cp1252, cần reconfigure sang UTF-8 để in tiếng Việt
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / ".claude" / "skills"
KEYWORDS_FILE = Path(__file__).parent / "key-work.md"
OUTPUT_FILE = Path(__file__).parent / "define_all_skill.md"

# Độ dài tối đa của tóm tắt (ký tự)
MAX_SUMMARY_LEN = 120

# ──────────────────────────────────────────────
# Mapping keyword → domain (có thể nhiều domain)
# Thêm keyword mới vào đây khi cần
# ──────────────────────────────────────────────
KEYWORD_DOMAIN: dict[str, list[str]] = {
    # Frontend
    "react":          ["FE"],
    "reactjs":        ["FE"],
    "react-native":   ["FE", "Mobile"],
    "typescript":     ["FE", "BE"],
    "javascript":     ["FE", "BE"],
    "css":            ["FE"],
    "html":           ["FE"],
    "tailwind":       ["FE"],
    "front":          ["FE"],
    "front-end":      ["FE"],
    "responsive":     ["FE"],
    "accessibility":  ["FE"],
    "seo":            ["FE"],
    "i18n":           ["FE"],
    "mobile":         ["FE", "Mobile"],
    "flutter":        ["Mobile"],
    "web":            ["FE"],

    # Backend
    "backend":        ["BE"],
    "back-end":       ["BE"],
    "django":         ["BE"],
    "django-rest-framework": ["BE"],
    "python":         ["BE"],
    "postgres":       ["BE"],
    "database":       ["BE", "Data"],
    "rest":           ["BE", "FE"],
    "graphql":        ["BE", "FE"],
    "socket":         ["BE", "FE"],
    "serverless":     ["BE", "DevOps"],
    # API — dùng chung FE lẫn BE
    "api":            ["FE", "BE"],
    "query":          ["FE", "BE"],

    # Testing
    "tdd":            ["Testing"],
    "testing":        ["Testing"],
    "debugger":       ["Testing"],
    "debugging":      ["Testing"],
    "jest":           ["Testing"],
    "mocha":          ["Testing"],
    "cypress":        ["Testing"],
    "playwright":     ["Testing"],
    "error":          ["Testing"],

    # DevOps / CI-CD
    "devops":         ["DevOps"],
    "ci":             ["DevOps"],
    "cd":             ["DevOps"],
    "deployment":     ["DevOps"],
    "containerization": ["DevOps"],
    "cloud":          ["DevOps"],
    "monitoring":     ["DevOps"],
    "scaling":        ["DevOps"],
    "caching":        ["DevOps", "BE"],
    "git":            ["DevOps"],

    # Architecture / Design
    "architecture":   ["Architecture"],
    "design":         ["Architecture"],
    "patterns":       ["Architecture"],
    "frameworks":     ["Architecture"],
    "software":       ["Architecture"],
    "standards":      ["Architecture"],
    "microservices":  ["Architecture", "BE"],
    "full":           ["Architecture"],
    "stack":          ["Architecture"],

    # Code Quality
    "review":         ["Quality"],
    "refactor":       ["Quality"],
    "document":       ["Quality"],
    "documentation":  ["Quality"],
    "code":           ["Quality"],
    "claude":         ["Quality"],
    "coding":         ["Quality"],
    "quality":        ["Quality"],
    "best":           ["Quality"],
    "practices":      ["Quality"],
    "handling":       ["Quality"],
    "senior":         ["Quality"],
    "engineer":       ["Quality"],

    # Data / Analytics
    "data":           ["Data"],
    "analytics":      ["Data"],
    "algorithms":     ["Data"],
    "structures":     ["Data"],
    "computing":      ["Data", "DevOps"],
    "performance":    ["FE", "BE"],
    "optimization":   ["FE", "BE"],

    # Claude / AI Tools
    "claude":         ["Claude"],
    "claude-code":    ["Claude"],
    "anthropic":      ["Claude"],
    "prompt":         ["Claude"],
    "mcp":            ["Claude"],
    "llm":            ["Claude"],

    # Codex (OpenAI Codex / GitHub Copilot ecosystem)
    "codex":          ["Codex"],
    "copilot":        ["Codex"],
    "openai":         ["Codex"],
    "gpt":            ["Codex"],
    "completion":     ["Codex"],

    # Cursor (AI-powered editor)
    "cursor":         ["Cursor"],
    "editor":         ["Cursor"],
    "ide":            ["Cursor", "VSCode"],
    "extension":      ["Cursor", "VSCode"],

    # VSCode
    "vscode":         ["VSCode"],
    "workspace":      ["VSCode"],
    "snippet":        ["VSCode"],
    "keybinding":     ["VSCode"],
    "debugger":       ["VSCode", "Testing"],
    "launch":         ["VSCode"],
    "task":           ["VSCode"],
    "devcontainer":   ["VSCode"],

    # Antigravity (skill platform)
    "antigravity":    ["Antigravity"],
    "skill":          ["Antigravity", "Tools"],
    "skills":         ["Antigravity", "Tools"],
    "plugin":         ["Antigravity"],
    "superpowers":    ["Antigravity"],

    # BA (Business Analysis)
    "bussiness-analysis": ["BA"],
    "project-management": ["BA"],
    "business":       ["BA"],
    "analysis":       ["BA"],
    "analyst":        ["BA"],
    "requirements":   ["BA"],
    "stakeholder":    ["BA"],
    "workflow":       ["BA"],
    "process":        ["BA"],
    "strategy":       ["BA"],
    "planning":       ["BA"],
    "reporting":      ["BA"],
    "kpi":            ["BA"],
    "metrics":        ["BA"],

    # Design (UI/UX)
    "design":         ["Design"],
    "ui":             ["Design"],
    "ux":             ["Design"],
    "figma":          ["Design"],
    "wireframe":      ["Design"],
    "prototype":      ["Design"],
    "typography":     ["Design"],
    "color":          ["Design"],
    "layout":         ["Design"],
    "animation":      ["Design"],
    "visual":         ["Design"],
    "branding":       ["Design"],
    "icon":           ["Design"],
    "responsive":     ["FE", "Design"],

    # AI / Agent
    "agent":          ["AI"],
    "chatbot":        ["AI"],
    "automation":     ["AI", "DevOps"],

    # General
    "tools":          ["Tools"],
    "libraries":      ["Tools"],
    "security":       ["Security"],
    "base":           ["Architecture"],
    "docs":           ["Quality"],
    "architect":      ["Architecture"],
    "skill":          ["Tools"],
    "io":             ["BE"],
    "project-management": ["Management"],
    "bussiness-analysis": ["Management"],
}


def get_domains(keywords: set[str]) -> str:
    """Trả về danh sách domain không trùng từ tập keyword đã khớp."""
    seen: list[str] = []
    for kw in sorted(keywords):
        for d in KEYWORD_DOMAIN.get(kw, ["Other"]):
            if d not in seen:
                seen.append(d)
    return ", ".join(seen) if seen else "Other"


# ──────────────────────────────────────────────
# Đọc keyword từ file
# ──────────────────────────────────────────────

def read_keywords(path: Path) -> list[str]:
    """
    Đọc từng dòng trong key-work.md, bỏ qua dòng comment (#)
    và dòng trống. Trả về danh sách keyword viết thường, không trùng lặp.
    """
    keywords: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        # Bỏ dấu gạch đầu dòng kiểu Markdown (- item, * item)
        line = line.strip().lstrip("-*").strip()
        # Xóa định dạng Markdown: backtick, bold, link
        line = re.sub(r"[`*_\[\]]", "", line)
        line = re.sub(r"\([^)]*\)", "", line).strip()
        if line and not line.startswith("#"):
            keywords.append(line.lower())
    # Giữ thứ tự, loại bỏ trùng lặp
    return list(dict.fromkeys(keywords))


# ──────────────────────────────────────────────
# Logic so khớp keyword ↔ tên skill
# ──────────────────────────────────────────────

# Cặp token bị coi là khác nhau dù một bên chứa bên kia
# VD: "java" ≠ "javascript"
_AMBIGUOUS: frozenset[tuple[str, str]] = frozenset({
    ("java", "javascript"),
    ("javascript", "java"),
})


def tokenize(text: str) -> list[str]:
    """Tách tên skill thành các token theo dấu - _ khoảng trắng."""
    return re.split(r"[-_\s/]+", text.lower())


def match_skill(keyword: str, skill_name: str) -> str | None:
    """
    So khớp keyword với tên skill theo 4 mức ưu tiên:

    1. exact   — giống hoàn toàn:  "tdd"  ==  "tdd"
    2. contains— chuỗi con:        "tools" có trong "web-tools"
    3. token   — token bằng nhau:  "code" khớp token trong "code-review"
    4. partial — token chứa nhau:  "tools" chứa "tool" → khớp "tool-builder"

    Trả về None nếu không khớp.
    """
    kw = keyword.lower()
    sn = skill_name.lower()

    if kw == sn:
        return "exact"

    if (kw in sn or sn in kw) and (kw, sn) not in _AMBIGUOUS and (sn, kw) not in _AMBIGUOUS:
        return "contains"

    kw_tokens = tokenize(kw)
    sn_tokens = tokenize(sn)

    # Token bằng nhau (exact token intersection)
    if set(kw_tokens) & set(sn_tokens):
        return "token"

    # Partial: token này là chuỗi con của token kia
    # Ngoại lệ: "java" ≠ "javascript" — tránh match nhầm
    if _partial_token_match(kw_tokens, sn_tokens):
        return "partial"

    return None


def _partial_token_match(kw_tokens: list[str], sn_tokens: list[str]) -> bool:
    long_kw = [t for t in kw_tokens if len(t) >= 3]
    long_sn = [t for t in sn_tokens if len(t) >= 3]
    return any(
        (kt in st or st in kt)
        for kt in long_kw
        for st in long_sn
        if (kt, st) not in _AMBIGUOUS and (st, kt) not in _AMBIGUOUS
    )


# ──────────────────────────────────────────────
# Đọc tóm tắt từ SKILL.md
# ──────────────────────────────────────────────

def _parse_description(text: str) -> str | None:
    """Lấy giá trị field description trong YAML frontmatter."""
    m = re.search(r'^description:\s*"?([^"\n]+)"?\s*$', text, re.MULTILINE)
    if m:
        desc = m.group(1).strip()
        return (desc[:MAX_SUMMARY_LEN] + "…") if len(desc) > MAX_SUMMARY_LEN else desc
    return None


def _first_body_line(text: str) -> str | None:
    """Lấy dòng nội dung đầu tiên ngoài frontmatter và heading."""
    in_front = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "---":
            in_front = not in_front
            continue
        if not in_front and stripped and not stripped.startswith("#"):
            return stripped[:MAX_SUMMARY_LEN]
    return None


def get_summary(skill_dir: Path, lang: str = "vi") -> str:
    """
    Đọc tối đa 50 dòng đầu của SKILL.md để lấy mô tả ngắn.
    Ưu tiên field description trong frontmatter YAML.
    """
    no_desc = "No description" if lang == "en" else "Chưa có mô tả"
    for name in ("SKILL.md", "skill.md"):
        md = skill_dir / name
        if md.exists():
            lines: list[str] = []
            with md.open(encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f):
                    if i >= 50:
                        break
                    lines.append(line)
            text = "".join(lines)
            return _parse_description(text) or _first_body_line(text) or no_desc
    return no_desc


# ──────────────────────────────────────────────
# Xuất Markdown table
# ──────────────────────────────────────────────

def escape_cell(text: str) -> str:
    """Thoát ký tự đặc biệt trong ô Markdown table."""
    return text.replace("|", "\\|").replace("\n", " ")


def build_link(skill_name: str, skill_dir: Path) -> str:
    """Tạo link Markdown đến file SKILL.md của skill."""
    for name in ("SKILL.md", "skill.md"):
        if (skill_dir / name).exists():
            return f"[{skill_name}](.claude/skills/{skill_name}/{name})"
    return skill_name


LABELS = {
    "vi": {
        "title":    "Danh sách Skill theo Domain",
        "total":    "Tổng cộng **{rows}** skill khớp từ **{kws}** keyword trong `key-work.md`.",
        "keyword":  "Keyword",
        "skill":    "Tên skill",
        "domain":   "Domain",
        "summary":  "Tóm tắt",
    },
    "en": {
        "title":    "Skill List by Domain",
        "total":    "Total **{rows}** skills matched from **{kws}** keywords in `key-work.md`.",
        "keyword":  "Keyword",
        "skill":    "Skill name",
        "domain":   "Domain",
        "summary":  "Summary",
    },
}


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Find skills matching keywords.")
    parser.add_argument("--lang", choices=["vi", "en"], default="vi", help="Output language (default: vi)")
    args = parser.parse_args()
    lang: str = args.lang
    lbl = LABELS[lang]

    keywords = read_keywords(KEYWORDS_FILE)
    print(f"Keywords: {len(keywords)} — {keywords[:8]}...")

    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith("."))
    print(f"Skills found: {len(skill_dirs)}")

    skill_map: dict[str, dict] = {}
    priority = ["exact", "contains", "token", "partial"]

    for kw in keywords:
        for sd in skill_dirs:
            match_type = match_skill(kw, sd.name)
            if match_type:
                entry = skill_map.setdefault(sd.name, {"keywords": set(), "match_type": match_type, "path": sd})
                entry["keywords"].add(kw)
                if priority.index(match_type) < priority.index(entry["match_type"]):
                    entry["match_type"] = match_type

    print(f"Matched: {len(skill_map)}")

    # Build rows: (domain_primary, keywords_str, link, domains_str, summary)
    rows = []
    for sn, info in skill_map.items():
        keywords_str = ", ".join(sorted(info["keywords"]))
        link = build_link(sn, info["path"])
        domains = get_domains(info["keywords"])
        summary = get_summary(info["path"], lang)
        # domain_primary = first domain để group & sort
        domain_primary = domains.split(",")[0].strip()
        rows.append((domain_primary, keywords_str, link, domains, summary))

    # Sắp xếp: Domain → Keyword → Tên skill
    rows.sort(key=lambda r: (r[0].lower(), r[1].lower(), r[2].lower()))

    # Gom nhóm theo domain, mỗi nhóm có section header
    out: list[str] = [
        f"# {lbl['title']}\n\n",
        lbl["total"].format(rows=len(rows), kws=len(keywords)) + "\n\n",
    ]

    current_domain = ""
    for domain_primary, keywords_str, link, domains, summary in rows:
        if domain_primary != current_domain:
            current_domain = domain_primary
            out.append(f"\n## {current_domain}\n\n")
            out.append(f"| {lbl['keyword']} | {lbl['skill']} | {lbl['domain']} | {lbl['summary']} |\n")
            out.append("|---|---|---|---|\n")
        cells = " | ".join(escape_cell(c) for c in (keywords_str, link, domains, summary))
        out.append(f"| {cells} |\n")

    OUTPUT_FILE.write_text("".join(out), encoding="utf-8")
    print(f"Written: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
