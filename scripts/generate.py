# -*- coding: utf-8 -*-
"""
Generate the markdown-based project index for guneysus.github.io-projects.

Produces:
  README.md                     - main navigation / index
  projects/<name>.md            - one page per project
  projects.json                 - machine-readable project data

Usage:
  python scripts/generate.py
"""
import json
import os
import re
import unicodedata

from projects_data import (
    ARCHIVES,
    CATEGORIES,
    PROJECT_CATEGORIES,
    TIERS,
    TIER_ORDER,
    TIER_THRESHOLDS,
    ARCHIVE_PROJECTS,
    GITLAB_ARCHIVE_PROJECTS,
    GITHUB_ARCHIVE_PROJECTS,
    GITHUB_ARCHIVE_EXTRA_PROJECTS,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_DIR = os.path.join(ROOT, "projects")
FORKS_DIR = os.path.join(ROOT, "forks")
OTHER_DIR = os.path.join(ROOT, "other")
DATA_FILE = os.path.join(ROOT, "projects.json")

# The archive repo that is the single source of truth. Projects present in this
# archive are canonical; the same project in another archive is a duplicate copy.
CANONICAL_ARCHIVE = "archive"


def page_rel_path(project):
    """Relative path from README to a project's page (forks live in forks/)."""
    if project.get("fork"):
        return f"forks/{slugify(project['name'])}.md"
    cat = category_of(project)
    return f"projects/{cat}/{slugify(project['name'])}.md"


def category_of(project):
    """Return the category key for a project (defaults to 'misc')."""
    return PROJECT_CATEGORIES.get(project["name"], "misc")


def _num(value):
    """Parse a numeric score, returning None for non-numeric values like 'Multi'."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def tier_of(project):
    """Classify a project into a PARA-style tier.

    Uses idea_score / impl_score / size when available; falls back to sensible
    defaults for projects without classification data.
    """
    # Explicit override wins (set manually in projects_data.py if needed).
    if project.get("tier"):
        return project["tier"]

    idea = _num(project.get("idea_score"))
    impl = _num(project.get("impl_score"))
    size = project.get("size")

    # Flagship: strong idea AND strong implementation
    if idea is not None and impl is not None:
        if idea >= TIER_THRESHOLDS["flagship"]["idea"] and impl >= TIER_THRESHOLDS["flagship"]["impl"]:
            return "flagship"

    # Showcase: strong implementation (idea below flagship threshold)
    if impl is not None and impl >= TIER_THRESHOLDS["showcase"]["impl"]:
        return "showcase"

    # Learning: small size, not already flagship/showcase
    if size == TIER_THRESHOLDS["learning"]["size"]:
        return "learning"

    # Projects with no classification data: default to archive.
    return "archive"


def slugify(name):
    """Create a filesystem-safe slug from a project name."""
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    name = re.sub(r"[^a-zA-Z0-9._-]", "-", name)
    return name.strip("-")


def original_url(project):
    """Build a link to the original repository."""
    owner = project["owner"]
    name = project["name"]
    if project["source"] == "github":
        return f"https://github.com/{owner}/{name}"
    return f"https://gitlab.com/{owner}/{name}"


def archive_label(project):
    return ARCHIVES[project["archive_repo"]]["label"]


def archive_url(project):
    """Build a clickable link to the project's current location in the archive monorepo."""
    arch = ARCHIVES[project["archive_repo"]]
    # GitLab uses /-/tree/<branch>/<path>; GitHub uses /tree/<branch>/<path>
    if "gitlab.com" in arch["web_url"]:
        return f"{arch['web_url']}/-/tree/{arch['branch']}/{project['archive_path']}"
    return f"{arch['web_url']}/tree/{arch['branch']}/{project['archive_path']}"


def build_project_page(project, duplicates):
    """Render a single project markdown page."""
    name = project["name"]
    desc = project.get("description") or "*No description available.*"
    vis = "🔓 Public" if project["visibility"] == "public" else "🔒 Private"
    fork = "Yes" if project.get("fork") else "No"
    archived = "✅ Archived" if project.get("archived") else "❌ Not archived"
    if project.get("canonical") and name in duplicates:
        status = "⭐ **Canonical** — this is the single source of truth for this project."
    elif project.get("duplicate_of"):
        status = f"⚠️ **Duplicate copy** — the canonical source is `{project['duplicate_of']}` in the {ARCHIVES[CANONICAL_ARCHIVE]['label']}."
    else:
        status = ""

    lines = [
        f"# {name}",
        "",
        f"> {desc}",
        "",
        status,
        "",
        "## Overview",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| **Name** | `{name}` |",
        f"| **Tier** | {TIERS[tier_of(project)]['emoji']} {TIERS[tier_of(project)]['label']} |",
        f"| **Description** | {desc} |",
        f"| **Visibility** | {vis} |",
        f"| **Fork** | {fork} |",
        f"| **Last activity** | {project.get('last_activity', '—')} |",
        f"| **Status** | {archived} |",
        f"| **Original source** | {project['source'].capitalize()} |",
        f"| **Original owner** | `{project['owner']}` |",
    ]
    if project.get("language"):
        lines.append(f"| **Language** | {project['language']} |")
    if project.get("project_type"):
        lines.append(f"| **Type** | {project['project_type']} |")
    if project.get("size"):
        lines.append(f"| **Size** | {project['size']} |")
    if project.get("idea"):
        lines.append(f"| **Idea** | {project['idea']} |")
    if project.get("idea_score"):
        lines.append(f"| **Idea score** | {project['idea_score']} |")
    if project.get("impl_score"):
        lines.append(f"| **Impl score** | {project['impl_score']} |")
    if project.get("rating"):
        lines.append(f"| **Rating** | {project['rating']} |")
    if project.get("score"):
        lines.append(f"| **Score** | {project['score']} |")
    lines += [
        "",
        "## Links",
        "",
        f"- **Original repository:** [{original_url(project)}]({original_url(project)})",
        f"- **Current location:** [{archive_url(project)}]({archive_url(project)})",
        f"- **Archive monorepo:** {archive_label(project)}",
        f"- **Archive path:** `{project['archive_path']}`",
        "",
        "## Archive Origins",
        "",
    ]
    for origin in ARCHIVES[project["archive_repo"]]["origins"]:
        lines.append(f"- `{origin}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    back = "../../README.md" if not project.get("fork") else "../README.md"
    lines.append(f"*Generated by `scripts/generate.py` · [Back to index]({back})*")
    return "\n".join(lines)


def build_summary(projects, duplicates):
    """Render other/summary.md — archive monorepos, summary, and duplicates."""
    by_source = {"github": [], "gitlab": []}
    for p in projects:
        by_source[p["source"]].append(p)

    originals = [p for p in projects if not p.get("fork")]
    forks = [p for p in projects if p.get("fork")]

    lines = [
        "# 📦 Archive Monorepos & Summary",
        "",
        "> Consolidated metadata for the archived projects. The **Projects** index lives in "
        "[`README.md`](../README.md); forks are in [`forks.md`](forks.md).",
        "",
        "## 📦 Archive Monorepos",
        "",
        "| Archive | Local path | Origins |",
        "| --- | --- | --- |",
    ]
    for key, arch in ARCHIVES.items():
        origins = "<br>".join(f"`{o}`" for o in arch["origins"])
        lines.append(f"| **{arch['label']}** | `{arch['local_path']}` | {origins} |")

    lines += [
        "",
        "## 📊 Summary",
        "",
        f"- **Total projects:** {len(projects)}",
        f"- **GitHub projects:** {len(by_source['github'])}",
        f"- **GitLab projects:** {len(by_source['gitlab'])}",
        f"- **Forks:** {len(forks)}",
        f"- **Duplicates (in multiple archives):** {len(duplicates)}",
        "",
    ]

    # Tier summary (canonical originals only)
    tier_counts = {}
    for p in originals:
        if p.get("duplicate_of"):
            continue
        tier_counts[tier_of(p)] = tier_counts.get(tier_of(p), 0) + 1
    if tier_counts:
        lines.append("**By tier (canonical originals):**")
        lines.append("")
        for tier_key in TIER_ORDER:
            if tier_key in tier_counts:
                t = TIERS[tier_key]
                lines.append(f"- {t['emoji']} **{t['label']}:** {tier_counts[tier_key]}")
        lines.append("")

    lines += [
        "## ⚠️ Duplicates",
        "",
        "Some projects exist in **more than one** archive monorepo. The **Archive** repo "
        f"({ARCHIVES[CANONICAL_ARCHIVE]['label']}) is the single source of truth; copies in "
        "other archives are marked as duplicates.",
        "",
    ]
    if duplicates:
        lines.append("| Project | Canonical | Other archives |")
        lines.append("| --- | --- | --- |")
        for name in sorted(duplicates):
            canonical = ARCHIVES[CANONICAL_ARCHIVE]["label"] if CANONICAL_ARCHIVE in duplicates[name] else "—"
            others = ", ".join(ARCHIVES[a]["label"] for a in duplicates[name] if a != CANONICAL_ARCHIVE)
            lines.append(f"| `{name}` | {canonical} | {others} |")
    else:
        lines.append("_No duplicates detected._")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated by `scripts/generate.py` · [Back to index](../README.md)*")
    return "\n".join(lines)


def build_forks(forks, duplicates):
    """Render other/forks.md — the forks section."""
    lines = [
        "# 🍴 Forks",
        "",
        "> Forked repositories — kept for reference, not original projects.",
        "",
        "| # | Project | Source | Language | Visibility | Archived | Last activity | Description |",
        "| :-: | --- | :-: | :-: | :-: | :-: | :-: | --- |",
    ]
    for i, p in enumerate(sorted(forks, key=lambda x: x["name"].lower()), start=1):
        if p.get("duplicate_of"):
            continue  # hide duplicate copies
        marker = " ⭐" if p.get("canonical") and p["name"] in duplicates else ""
        lang = p.get("language") or "—"
        src = "🐙 GitHub" if p["source"] == "github" else "🦊 GitLab"
        lines.append(
            f"| {i} | [{p['name']}]({page_rel_path(p)}){marker} | "
            f"{src} | "
            f"{lang} | "
            f"{'🔓' if p['visibility']=='public' else '🔒'} | "
            f"{'✅' if p.get('archived') else '❌'} | "
            f"{p.get('last_activity','—')} | {p.get('description') or ''} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated by `scripts/generate.py` · [Back to index](../README.md)*")
    return "\n".join(lines)


def build_readme(projects, duplicates):
    """Render the main README index — the tier-based Projects section.

    Archive monorepos/summary/duplicates live in other/summary.md; forks live
    in other/forks.md. This file links to both.
    """
    originals = [p for p in projects if not p.get("fork")]

    lines = [
        "# 🗂️ Project Archive Index",
        "",
        "> **Metadata & navigation index** for my archived projects, consolidated from multiple "
        "GitHub and GitLab monorepo archives. This repository does **not** contain source code — "
        "it links to the original repositories and the archive monorepos that preserve them.",
        "",
        "## 🧭 Navigation",
        "",
        "- [📦 Archive Monorepos & Summary](other/summary.md) — archive repos, totals, duplicates",
        "- [🍴 Forks](other/forks.md) — forked repositories kept for reference",
        "",
        "## 🗂️ Projects",
        "",
        "Projects are organized by **tier** (PARA-style), reflecting each project's "
        "maturity and value. Within each tier, projects are grouped by technology/domain. "
        "Only canonical entries are shown (duplicate copies are hidden).",
        "",
    ]

    # Group original projects by tier (canonical only; duplicate copies hidden)
    by_tier = {}
    for p in originals:
        if p.get("duplicate_of"):
            continue  # hide duplicate copies, show only canonical
        by_tier.setdefault(tier_of(p), []).append(p)

    for tier_key in TIER_ORDER:
        if tier_key not in by_tier:
            continue
        tier = TIERS[tier_key]
        lines += [
            f"### {tier['emoji']} {tier['label']}",
            "",
            f"> {tier['description']}",
            "",
        ]
        # Within a tier, group by technology category
        by_cat = {}
        for p in by_tier[tier_key]:
            by_cat.setdefault(category_of(p), []).append(p)
        for cat_key in sorted(by_cat, key=lambda c: CATEGORIES[c]["label"].lower()):
            cat = CATEGORIES[cat_key]
            lines += [
                f"#### {cat['emoji']} {cat['label']}",
                "",
                "| # | Project | Source | Language | Type | Size | Idea | Impl | Rating | Visibility | Archived | Last activity | Description |",
                "| :-: | --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | --- |",
            ]
            for i, p in enumerate(sorted(by_cat[cat_key], key=lambda x: x["name"].lower()), start=1):
                marker = " ⭐" if p.get("canonical") and p["name"] in duplicates else ""
                lang = p.get("language") or "—"
                ptype = p.get("project_type") or "—"
                size = p.get("size") or "—"
                idea = p.get("idea") or "—"
                impl = p.get("impl_score") or "—"
                rating = p.get("rating") or "—"
                src = "🐙 GitHub" if p["source"] == "github" else "🦊 GitLab"
                lines.append(
                    f"| {i} | [{p['name']}]({page_rel_path(p)}){marker} | "
                    f"{src} | "
                    f"{lang} | "
                    f"{ptype} | "
                    f"{size} | "
                    f"{idea} | "
                    f"{impl} | "
                    f"{rating} | "
                    f"{'🔓' if p['visibility']=='public' else '🔒'} | "
                    f"{'✅' if p.get('archived') else '❌'} | "
                    f"{p.get('last_activity','—')} | {p.get('description') or ''} |"
                )
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Generated by `scripts/generate.py` · Data in `scripts/projects_data.py`*")
    return "\n".join(lines)


def discover_archive_projects():
    """Discover projects in the canonical archive repo (source of truth).

    Reads the repo's repos/ structure from the configured branch (via
    `git ls-tree`) and merges with the curated ARCHIVE_PROJECTS list.
    Curated entries (with descriptions) take precedence; any additional
    projects found in the branch are added with placeholder metadata.
    """
    import subprocess

    curated = {p["name"]: dict(p) for p in ARCHIVE_PROJECTS}
    arch = ARCHIVES[CANONICAL_ARCHIVE]
    repo_root = arch["local_path"]
    branch = arch["branch"]
    discovered = dict(curated)

    # Map archive subfolder -> (source, owner)
    sections = {
        "repos/github.com/guneysus": ("github", "guneysus"),
        "repos/gitlab.com/guneysu": ("gitlab", "guneysu"),
        "repos/gitlab.com/guneysu.dev": ("gitlab", "guneysu.dev"),
    }
    for sub, (source, owner) in sections.items():
        try:
            out = subprocess.run(
                ["git", "-C", repo_root, "ls-tree", "-d", "--name-only", f"origin/{branch}", sub + "/"],
                capture_output=True, text=True, check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
        for line in out.stdout.splitlines():
            name = line.rstrip("/").split("/")[-1]
            if not name or name in discovered:
                continue
            discovered[name] = {
                "name": name,
                "description": "",
                "visibility": "private",
                "fork": False,
                "last_activity": "",
                "archived": True,
                "source": source,
                "owner": owner,
                "archive_path": f"{sub}/{name}",
            }

    # Discover forks from the archive repo's forks/ section
    fork_sections = {
        "forks/github.com/guneysus": ("github", "guneysus"),
        "forks/github.com/guneysus-archieve": ("github", "guneysus-archieve"),
    }
    for sub, (source, owner) in fork_sections.items():
        try:
            out = subprocess.run(
                ["git", "-C", repo_root, "ls-tree", "-d", "--name-only", f"origin/{branch}", sub + "/"],
                capture_output=True, text=True, check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
        for line in out.stdout.splitlines():
            name = line.rstrip("/").split("/")[-1]
            if not name or name in discovered:
                continue
            discovered[name] = {
                "name": name,
                "description": "",
                "visibility": "private",
                "fork": True,
                "last_activity": "",
                "archived": True,
                "source": source,
                "owner": owner,
                "archive_path": f"{sub}/{name}",
            }
    return list(discovered.values())


def main():
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    os.makedirs(FORKS_DIR, exist_ok=True)

    # Auto-discover projects in the canonical archive repo (source of truth) that
    # aren't already curated in ARCHIVE_PROJECTS. This keeps the canonical archive
    # complete even as new projects are added to the repo.
    archive_projects = discover_archive_projects()

    # Tag each project with its archive repo
    projects = []
    for p in archive_projects:
        p = dict(p)
        p["archive_repo"] = "archive"
        projects.append(p)
    for p in GITLAB_ARCHIVE_PROJECTS:
        p = dict(p)
        p["archive_repo"] = "gitlab-archive"
        projects.append(p)
    for p in GITHUB_ARCHIVE_PROJECTS:
        p = dict(p)
        p["archive_repo"] = "github-guneysus-archive"
        p["archive_path"] = f"repos/github.com/guneysus-archieve/{p['name']}"
        projects.append(p)
    for p in GITHUB_ARCHIVE_EXTRA_PROJECTS:
        p = dict(p)
        p["archive_repo"] = "github-guneysus-archive"
        p["archive_path"] = f"repos/github.com/guneysus-archieve/{p['name']}"
        projects.append(p)

    # Detect duplicates by name across archives
    by_name = {}
    for p in projects:
        by_name.setdefault(p["name"], []).append(p)
    duplicates = {}
    for name, copies in by_name.items():
        archs = sorted({p["archive_repo"] for p in copies})
        if len(archs) > 1:
            duplicates[name] = archs
            # Mark the copy in the canonical archive as canonical; others as duplicates
            for p in copies:
                if p["archive_repo"] == CANONICAL_ARCHIVE:
                    p["canonical"] = True
                    p["duplicate_of"] = None
                else:
                    p["canonical"] = False
                    p["duplicate_of"] = name
        else:
            p = copies[0]
            p["canonical"] = True
            p["duplicate_of"] = None

    # Enrich metadata from the canonical archive repo's data files
    from enrich import enrich_projects
    n_enriched = enrich_projects(projects, ARCHIVES[CANONICAL_ARCHIVE]["local_path"], ARCHIVES[CANONICAL_ARCHIVE]["branch"])
    print(f"Enriched {n_enriched} projects with metadata")

    # Write per-project pages.
    # When multiple projects share the same slugified filename (duplicates across
    # archives), only the canonical entry gets a page; duplicate copies are skipped
    # to avoid overwriting the canonical page.
    written = set()
    for p in sorted(projects, key=lambda x: (not x.get("canonical", True), x["name"].lower())):
        slug = slugify(p["name"])
        if p.get("fork"):
            folder = FORKS_DIR
        else:
            folder = os.path.join(PROJECTS_DIR, category_of(p))
        path = os.path.join(folder, f"{slug}.md")
        if path in written:
            continue  # a canonical entry already wrote this page
        os.makedirs(folder, exist_ok=True)
        page = build_project_page(p, duplicates)
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        written.add(path)

    # Write README (tier-based Projects index)
    readme = build_readme(projects, duplicates)
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)

    # Write other/summary.md (archive monorepos, summary, duplicates)
    os.makedirs(OTHER_DIR, exist_ok=True)
    summary = build_summary(projects, duplicates)
    with open(os.path.join(OTHER_DIR, "summary.md"), "w", encoding="utf-8") as f:
        f.write(summary)

    # Write other/forks.md (forks section)
    forks = [p for p in projects if p.get("fork")]
    forks_md = build_forks(forks, duplicates)
    with open(os.path.join(OTHER_DIR, "forks.md"), "w", encoding="utf-8") as f:
        f.write(forks_md)

    # Write JSON data
    data = {
        "archives": ARCHIVES,
        "duplicates": duplicates,
        "projects": projects,
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(projects)} project pages, README.md, other/summary.md, other/forks.md, and projects.json")
    print(f"Duplicates detected: {len(duplicates)}")


if __name__ == "__main__":
    main()