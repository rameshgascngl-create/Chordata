#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMPDIR_KOTLIN="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_KOTLIN"' EXIT
kotlinc "$ROOT/app/src/main/java/in/gasc/zoology/chordata/domain/Models.kt" \
  "$ROOT/tests/CoreSmoke.kt" -include-runtime -d "$TMPDIR_KOTLIN/core.jar"
java -jar "$TMPDIR_KOTLIN/core.jar"
