#!/usr/bin/env bash
# Synchronise the *complete* 64/64 source, including large PNG/SVG assets,
# to the dedicated QA branch. Requires a GitHub-authenticated Git client and
# network connectivity. It never changes main or force-pushes.
set -euo pipefail

MODE="${1:---dry-run}"
if [[ "$#" -gt 1 || ( "$MODE" != "--dry-run" && "$MODE" != "--push" ) ]]; then
  echo 'Usage: bash scripts/sync_qa_branch.sh [--dry-run|--push]' >&2
  exit 2
fi
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO='https://github.com/rameshgascngl-create/Chordata.git'
BRANCH='native/qa-chordata-illustration-coverage'
EXPECTED_HEAD='5371d7ecfc8a03955ba86100578dad6538c5fd26'
command -v git >/dev/null || { echo 'git is required' >&2; exit 2; }
command -v rsync >/dev/null || { echo 'rsync is required' >&2; exit 2; }

# Validate the source before accessing/changing the remote.
bash "$ROOT/scripts/qa_all.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
GIT_TERMINAL_PROMPT=0 git clone --quiet --depth 1 --single-branch --branch "$BRANCH" "$REPO" "$TMP/repo"
ACTUAL="$(git -C "$TMP/repo" rev-parse HEAD)"
if [[ "$ACTUAL" != "$EXPECTED_HEAD" ]]; then
  echo "STOP: remote QA head changed; expected $EXPECTED_HEAD, saw $ACTUAL" >&2
  exit 3
fi
rsync -a --delete --exclude='.git/' --exclude='__pycache__/' --exclude='*.pyc' "$ROOT/" "$TMP/repo/"
git -C "$TMP/repo" add -A
git -C "$TMP/repo" diff --cached --check
if git -C "$TMP/repo" diff --cached --quiet; then
  echo 'No changes to synchronise.'
  exit 0
fi
printf '\nReview of the QA-only changes:\n'
git -C "$TMP/repo" diff --cached --stat
if [[ "$MODE" == '--dry-run' ]]; then
  echo 'DRY RUN: no commit or push. Re-run with --push only after reviewing changes.'
  exit 0
fi
git -C "$TMP/repo" commit -m 'qa(chordata): stage 64 provisional figures and low-memory native gallery'
# No force. A concurrent update must cause a non-fast-forward rejection.
git -C "$TMP/repo" push origin "HEAD:refs/heads/$BRANCH"
NEW_HEAD="$(git -C "$TMP/repo" rev-parse HEAD)"
echo "QA source pushed: $NEW_HEAD"
echo "Branch: $BRANCH"
echo 'Observe the Chordata Native QA Debug APK GitHub Actions run before downloading an APK.'
