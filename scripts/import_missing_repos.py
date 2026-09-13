# -*- coding: utf-8 -*-
"""
Import missing GitHub repos into the guneysus/archive monorepo with full history.

These repos exist on GitHub (owned by guneysus) but were never imported into
the archive. This script imports each one into repos/github.com/guneysus/<name>/
using git-filter-repo, preserving full commit history.

Strategy: work directly in the local archive clone. For each repo:
  1. Clone the repo (full history) to a temp dir
  2. Rewrite its history into repos/github.com/guneysus/<name>/
  3. Fetch that rewritten history into the archive clone
  4. Merge it into the archive's local develop branch (unrelated histories)
  5. At the end, push local develop to GitHub

This avoids re-fetching the entire archive history for every repo.

Usage:
  python scripts/import_missing_repos.py          # dry-run (shows what would happen)
  python scripts/import_missing_repos.py --run     # actually import

Prerequisites:
  - gh CLI authenticated
  - git-filter-repo installed (pip install git-filter-repo)
  - A local clone of guneysus/archive at the path below
"""
import os
import shutil
import subprocess
import sys
import tempfile

# The repos that exist on GitHub and need importing.
# blog-v2 and boilerplate were already imported successfully in earlier runs.
REPOS = [
    "learn-prometheus",
]

# Repos whose GitHub remote is deleted but a local clone with full history exists.
# Maps repo name -> local path. These are copied (not cloned) into the archive.
LOCAL_REPOS = {
    "learn-prometheus": r"X:\git\github.com\guneysus\learn-prometheus",
}

ARCHIVE_PATH = r"X:\git\github.com\guneysus\github-archive"
TARGET_BRANCH = "develop"  # the archive's working branch
DEST_PREFIX = "repos/github.com/guneysus"  # where repos go in the archive


def run(cmd, cwd=None, check=True):
    print(f"  $ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        print(f"    ERROR: {r.stderr.strip()}")
        sys.exit(1)
    return r


def import_repo(name, dry_run):
    print(f"\n=== Importing {name} ===")
    tmp = tempfile.mkdtemp(prefix=f"import_{name}_")
    try:
        # 1. Get the source repo (clone from GitHub, or copy from local path)
        local_src = LOCAL_REPOS.get(name)
        if local_src:
            print(f"  [1/4] Copying local repo from {local_src}...")
            run(["git", "clone", "--no-hardlinks", local_src, tmp])
        else:
            print("  [1/4] Cloning repo with full history...")
            run(["gh", "repo", "clone", f"guneysus/{name}", tmp])

        # 2. Rewrite history to move everything into a subdirectory
        print("  [2/4] Rewriting history into subdirectory...")
        run(["git", "filter-repo", "--force", "--to-subdirectory-filter", f"{DEST_PREFIX}/{name}/"], cwd=tmp)

        if dry_run:
            print("  [DRY-RUN] Skipping fetch/merge (would merge into archive)")
            return

        # 3. Fetch the rewritten history into the archive clone under a temp ref
        print("  [3/4] Fetching rewritten history into archive...")
        run(["git", "fetch", tmp, f"HEAD:refs/import/{name}"], cwd=ARCHIVE_PATH)

        # 4. Merge into the archive's local develop branch (unrelated histories)
        print("  [4/4] Merging into archive develop...")
        run(["git", "checkout", TARGET_BRANCH], cwd=ARCHIVE_PATH)
        run(["git", "merge", "--allow-unrelated-histories", "--no-edit", f"refs/import/{name}"], cwd=ARCHIVE_PATH)
        run(["git", "branch", "-D", f"import/{name}"], cwd=ARCHIVE_PATH, check=False)
        print(f"  ✓ {name} imported successfully")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    dry_run = "--run" not in sys.argv
    if dry_run:
        print("DRY-RUN MODE: showing what would happen (use --run to execute)\n")
    else:
        print("EXECUTE MODE: importing repos\n")

    if not os.path.isdir(ARCHIVE_PATH):
        print(f"ERROR: Archive path not found: {ARCHIVE_PATH}")
        sys.exit(1)

    for name in REPOS:
        import_repo(name, dry_run)

    if not dry_run:
        # Push the accumulated local develop branch to GitHub (the archive's origin).
        print("\n=== Pushing local develop to GitHub ===")
        run(["git", "push", "origin", f"{TARGET_BRANCH}:{TARGET_BRANCH}"], cwd=ARCHIVE_PATH)
        print("  ✓ Pushed to GitHub")

    print("\nDone.")


if __name__ == "__main__":
    main()