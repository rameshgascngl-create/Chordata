#!/usr/bin/env python3
"""Check staged-source Git whitespace rules required for QA-branch synchronisation.

Markdown's two-space hard breaks and review CSV CRLF rows are intentional;
trailing spaces in Kotlin source must still fail `git diff --cached --check`.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
assert shutil.which("git"), "git is required for the QA-branch synchronisation preflight"

def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)

with TemporaryDirectory(prefix="chordata-git-whitespace-") as tmp:
    repo = Path(tmp)
    init = run(repo, "init", "-q")
    assert init.returncode == 0, init.stderr
    shutil.copy2(ROOT / ".gitattributes", repo / ".gitattributes")
    (repo / "QA.md").write_text("Markdown hard break:  \nNext sentence.\n", encoding="utf-8")
    (repo / "review.csv").write_bytes(b"name,decision\r\na,PROVISIONAL\r\n")
    (repo / "Valid.kt").write_text("fun main() = Unit\n", encoding="utf-8")
    staged = run(repo, "add", "-A")
    assert staged.returncode == 0, staged.stderr
    clean = run(repo, "diff", "--cached", "--check")
    assert clean.returncode == 0, clean.stdout + clean.stderr

    (repo / "Unsafe.kt").write_text("val scientificSignoff = false   \n", encoding="utf-8")
    staged = run(repo, "add", "Unsafe.kt")
    assert staged.returncode == 0, staged.stderr
    bad = run(repo, "diff", "--cached", "--check")
    assert bad.returncode != 0 and "Unsafe.kt" in bad.stdout, "trailing Kotlin spaces must fail"

print("PASS: Git QA sync tolerates Markdown/CSV formatting, rejects trailing Kotlin whitespace")
