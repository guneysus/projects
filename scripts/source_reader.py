# -*- coding: utf-8 -*-
"""
Read project source from the gitlab-archive repo to extract:
  - core idea (from README or description)
  - a representative code snippet (for small projects)

The gitlab-archive (X:\\git\\gitlab.com\\guneysu\\gitlab-archive) is the source
of truth for project content. Each project lives under repos/<host>/<owner>/<name>/.
"""
import os
import re
import subprocess

# The gitlab-archive repo that holds the project sources.
SOURCE_ARCHIVE = r"X:\git\gitlab.com\guneysu\gitlab-archive"
SOURCE_BRANCH = "HEAD"

# File extensions we consider "source code" (for snippet extraction).
SOURCE_EXTS = {
    ".cs", ".py", ".js", ".ts", ".go", ".rs", ".sh", ".ps1", ".sql",
    ".lua", ".java", ".c", ".cpp", ".h", ".html", ".css", ".jsx", ".tsx",
    ".rb", ".php", ".kt", ".swift", ".m", ".r", ".pl", ".vim", ".tf",
}

# Files to skip when looking for a representative snippet.
SKIP_FILES = {
    ".gitignore", ".gitattributes", "LICENSE", "LICENSE.md", "LICENSE.txt",
    "package-lock.json", "poetry.lock", "Pipfile.lock", "yarn.lock",
    "Gemfile.lock", "Cargo.lock", "composer.lock", "go.sum",
}

# Files that are good snippet candidates (prefer these).
PREFERRED_FILES = {
    "main.py", "app.py", "index.js", "index.ts", "main.js", "main.ts",
    "Main.cs", "main.cs", "App.cs", "app.cs", "index.html", "main.go",
    "main.rs", "script.py", "cli.py", "server.py", "server.js",
}


def _git_show(repo_root, ref, path):
    """Return file content from a git ref via `git show`, or None."""
    try:
        out = subprocess.run(
            ["git", "-C", repo_root, "show", f"{ref}:{path}"],
            capture_output=True, check=True,
        )
        # Decode as UTF-8 with fallback; skip binary files
        try:
            return out.stdout.decode("utf-8", errors="replace")
        except Exception:
            return None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _git_ls(repo_root, ref, path):
    """List files under a path in a git ref."""
    try:
        out = subprocess.run(
            ["git", "-C", repo_root, "ls-tree", "-r", "--name-only", ref, path],
            capture_output=True, text=True, check=True,
        )
        return [l for l in out.stdout.splitlines() if l]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def _clean(content):
    """Strip BOM and normalize whitespace."""
    if content is None:
        return ""
    content = content.lstrip("\ufeff")
    return content


def _first_paragraph(md):
    """Extract the first meaningful paragraph from a README."""
    lines = [l.strip() for l in md.splitlines()]
    in_code = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("!["):  # image
            continue
        if not line:
            continue
        if line.startswith("|") or line.startswith("---"):
            continue
        # Skip badge/shield lines (contain img.shields.io or badges)
        if "shields.io" in line or "badge" in line.lower():
            continue
        # Collect consecutive non-empty, non-code lines
        para = []
        for l in lines[i:]:
            if not l:
                break
            if l.startswith("```"):
                break
            para.append(l)
        text = " ".join(para).strip()
        # Remove markdown links -> keep text
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        text = re.sub(r"[*_`>#]", "", text).strip()
        if len(text) > 20:
            return text
    return ""


def _extract_code_blocks(md):
    """Extract fenced code blocks from a README."""
    blocks = re.findall(r"```(\w*)\n(.*?)```", md, re.DOTALL)
    return [(lang, b.strip()) for lang, b in blocks if b.strip()]


def _pick_snippet_file(files):
    """Pick the best source file for a snippet from a list of file paths."""
    if not files:
        return None
    # Prefer files in preferred list
    for f in files:
        base = os.path.basename(f)
        if base in PREFERRED_FILES:
            return f
    # Prefer files with source extensions, shortest path first
    candidates = [f for f in files if os.path.splitext(f)[1] in SOURCE_EXTS]
    if not candidates:
        return None
    # Prefer files not in test/spec folders
    non_test = [f for f in candidates if not re.search(r"(test|spec|tests?|__pycache__)", f, re.I)]
    pool = non_test or candidates
    return min(pool, key=lambda f: (f.count("/"), len(f)))


def _extract_snippet(content, max_lines=25):
    """Extract a representative snippet from source code."""
    content = _clean(content)
    lines = content.splitlines()
    if not lines:
        return ""
    # Strip leading blank lines
    while lines and not lines[0].strip():
        lines.pop(0)
    # Skip license/header comment blocks
    start = 0
    if lines and lines[0].strip().startswith(("/*", "//", "#", "<!--", "/*!")):
        # find first non-comment line
        for i, l in enumerate(lines):
            if l.strip() and not l.strip().startswith(("/*", "//", "#", "<!--", "*", "*/")):
                start = i
                break
    snippet = lines[start:start + max_lines]
    return "\n".join(snippet).strip()


def read_project_source(project):
    """Read source info for a project from the gitlab-archive.

    Returns a dict with:
      core_idea : str  (short explanation of the project's core idea)
      snippet   : str  (representative code snippet, or "")
      snippet_lang : str (language hint for the snippet fence)
    """
    name = project["name"]
    # Build the path in the gitlab-archive. The archive_path already encodes
    # repos/<host>/<owner>/<name>; use it directly.
    path = project.get("archive_path", "")
    if not path:
        return {"core_idea": "", "snippet": "", "snippet_lang": ""}

    files = _git_ls(SOURCE_ARCHIVE, SOURCE_BRANCH, path)
    if not files:
        return {"core_idea": "", "snippet": "", "snippet_lang": ""}

    # 1. Core idea from README
    core_idea = ""
    readme = next((f for f in files if os.path.basename(f).lower() == "readme.md"), None)
    if readme:
        md = _git_show(SOURCE_ARCHIVE, SOURCE_BRANCH, readme)
        if md:
            core_idea = _first_paragraph(md)

    # Fall back to the project description if README has no meaningful paragraph
    if not core_idea:
        core_idea = (project.get("description") or "").strip()

    # 2. Code snippet: prefer README code block, else a source file
    snippet = ""
    snippet_lang = ""
    if readme:
        md = _git_show(SOURCE_ARCHIVE, SOURCE_BRANCH, readme)
        if md:
            blocks = _extract_code_blocks(md)
            if blocks:
                lang, code = blocks[0]
                snippet = code
                snippet_lang = lang or ""

    if not snippet:
        # Pick a source file
        src_files = [f for f in files if os.path.splitext(f)[1] in SOURCE_EXTS]
        src_files = [f for f in src_files if os.path.basename(f) not in SKIP_FILES]
        pick = _pick_snippet_file(src_files)
        if pick:
            content = _git_show(SOURCE_ARCHIVE, SOURCE_BRANCH, pick)
            if content:
                snippet = _extract_snippet(content)
                snippet_lang = os.path.splitext(pick)[1].lstrip(".")

    return {
        "core_idea": core_idea,
        "snippet": snippet,
        "snippet_lang": snippet_lang,
    }