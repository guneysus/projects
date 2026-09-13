# -*- coding: utf-8 -*-
"""
Metadata enrichment for the project index.

Reads metadata from the canonical archive repo's data/ folder and README
analysis table, and merges it into the project entries. This replaces
placeholder metadata (empty descriptions, generic flags) with real data.

Sources:
  - <archive>/README.md                    : detailed analysis table
                                              (description, language, type, size, rating)
  - <archive>/data/repos-archive-guneysus.json : fork flags, archived status, dates
  - <archive>/data/archive-scores.csv      : scores, last commit, hasArchived
"""
import csv
import json
import os
import re


def _parse_readme_analysis(readme_path):
    """Parse the README analysis table into {name: {description, language, type, size, rating}}."""
    result = {}
    if not os.path.isfile(readme_path):
        return result
    with open(readme_path, encoding="utf-8") as f:
        content = f.read()
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("| [**"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 10:
            continue
        m = re.match(r"\[\*\*([^*]+)\*\*\]\(([^)]+)\)", cells[1])
        if not m:
            continue
        name = m.group(1)
        result[name] = {
            "description": cells[2],
            "language": cells[3],
            "type": cells[4],
            "size": cells[5],
            "idea": cells[6],
            "idea_score": cells[7],
            "impl_score": cells[8],
            "rating": cells[9],
        }
    return result


def _read_branch_file(repo_root, branch, path):
    """Read a file from a git branch via `git show`, falling back to the working tree."""
    import subprocess
    try:
        out = subprocess.run(
            ["git", "-C", repo_root, "show", f"origin/{branch}:{path}"],
            capture_output=True, check=True,
        )
        return out.stdout.decode("utf-8", errors="replace")
    except (subprocess.CalledProcessError, FileNotFoundError):
        full = os.path.join(repo_root, path)
        if os.path.isfile(full):
            with open(full, encoding="utf-8", errors="replace") as f:
                return f.read()
        return None


def _parse_readme_analysis_from_text(content):
    """Parse the README analysis table from raw text."""
    result = {}
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("| [**"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 10:
            continue
        m = re.match(r"\[\*\*([^*]+)\*\*\]\(([^)]+)\)", cells[1])
        if not m:
            continue
        name = m.group(1)
        result[name] = {
            "description": cells[2],
            "language": cells[3],
            "type": cells[4],
            "size": cells[5],
            "idea": cells[6],
            "idea_score": cells[7],
            "impl_score": cells[8],
            "rating": cells[9],
        }
    return result


def _parse_repos_json(path):
    """Parse repos-archive-guneysus.json into {name: {isFork, isArchived, updatedAt, pushedAt, createdAt}}."""
    result = {}
    if not os.path.isfile(path):
        return result
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for p in data:
        result[p["name"]] = {
            "isFork": p.get("isFork", False),
            "isArchived": p.get("isArchived", False),
            "updatedAt": p.get("updatedAt", ""),
            "pushedAt": p.get("pushedAt", ""),
            "createdAt": p.get("createdAt", ""),
            "description": p.get("description", ""),
        }
    return result


def _parse_scores_csv(path):
    """Parse archive-scores.csv into {name: {score, last_commit, hasArchived}}."""
    result = {}
    if not os.path.isfile(path):
        return result
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            repo = row.get("repo", "")
            name = repo.split("/")[-1] if "/" in repo else repo
            result[name] = {
                "score": row.get("score", ""),
                "last_commit": row.get("last_commit", ""),
                "hasArchived": row.get("hasArchived", ""),
            }
    return result


def enrich_projects(projects, archive_local_path, branch="develop"):
    """Enrich project entries with metadata from the archive repo's data files.

    Only fills in missing/placeholder values; existing curated metadata is kept.
    """
    readme_content = _read_branch_file(archive_local_path, branch, "README.md")
    repos_json = os.path.join(archive_local_path, "data", "repos-archive-guneysus.json")
    scores_csv = os.path.join(archive_local_path, "data", "archive-scores.csv")

    analysis = _parse_readme_analysis_from_text(readme_content) if readme_content else {}
    repos = _parse_repos_json(repos_json)
    scores = _parse_scores_csv(scores_csv)

    enriched = 0
    for p in projects:
        name = p["name"]
        changed = False

        # Description from README analysis (most descriptive)
        if name in analysis and not p.get("description"):
            p["description"] = analysis[name]["description"]
            p["language"] = analysis[name]["language"]
            p["project_type"] = analysis[name]["type"]
            p["size"] = analysis[name]["size"]
            p["rating"] = analysis[name]["rating"]
            changed = True
        elif name in repos and not p.get("description") and repos[name].get("description"):
            p["description"] = repos[name]["description"]
            changed = True

        # Fork flag
        if name in repos and not p.get("fork"):
            p["fork"] = repos[name]["isFork"]
            changed = True

        # Archived status
        if name in repos and repos[name]["isArchived"]:
            p["archived"] = True
            changed = True

        # Last activity from updatedAt
        if name in repos and not p.get("last_activity") and repos[name]["updatedAt"]:
            p["last_activity"] = repos[name]["updatedAt"][:10]
            changed = True

        # Score
        if name in scores and scores[name]["score"]:
            p["score"] = scores[name]["score"]
            changed = True

        if changed:
            enriched += 1

    return enriched