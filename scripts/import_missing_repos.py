# -*- coding: utf-8 -*-
"""
Import missing GitHub repos into the guneysus/archive monorepo with full history.

These 15 repos exist on GitHub (owned by guneysus) but were never imported into
the archive. This script imports each one into repos/github.com/guneysus/<name>/
using git-filter-repo, preserving full commit history.

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

# The 15 repos that exist on GitHub and need importing
REPOS = [
    "blog-v2", "boilerplate", "calcx", "cv", "galeri.nakizeyn.guneysu.dev",
    "gohugo-hacker", "goreplay", "mevlana-takvimi", "NanoDbProfiler", "ndig",
    "pake", "ramblings", "Typr", "Typr.Source", "whatismybrowser",
]

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
        # 1. Clone the repo with full history (no blob filter - filter-repo needs blobs)
        print("  [1/5] Cloning repo with full history...")
        run(["gh", "repo", "clone", f"guneysus/{name}", tmp])

        # 2. Rewrite history to move everything into a subdirectory
        print("  [2/5] Rewriting history into subdirectory...")
        run(["git", "filter-repo", "--force", "--to-subdirectory-filter", f"{DEST_PREFIX}/{name}/"], cwd=tmp)

        # 3. Add the archive as a remote and fetch
        print("  [3/5] Adding archive remote...")
        run(["git", "remote", "add", "archive", ARCHIVE_PATH], cwd=tmp)

        if dry_run:
            print("  [DRY-RUN] Skipping fetch/merge (would merge into archive)")
            return

        # 4. Fetch the archive's target branch
        print("  [4/5] Fetching archive branch...")
        run(["git", "fetch", "archive", TARGET_BRANCH], cwd=tmp)

        # 5. Merge into the archive branch with unrelated histories
        print("  [5/5] Merging into archive...")
        run(["git", "merge", "--allow-unrelated-histories", f"archive/{TARGET_BRANCH}"], cwd=tmp)

        # Push back to the archive
        print("  Pushing to archive...")
        run(["git", "push", "archive", f"HEAD:{TARGET_BRANCH}"], cwd=tmp)
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

    print("\nDone.")


if __name__ == "__main__":
    main()