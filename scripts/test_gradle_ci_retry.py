#!/usr/bin/env python3
"""Offline contract tests: retry dependency transport failures, never compilation errors."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/gradle_ci_retry.sh"

def scenario(kind):
    with tempfile.TemporaryDirectory(prefix="chordata-gradle-retry-") as tmp:
        home = Path(tmp)
        bin_dir = home / "bin"
        bin_dir.mkdir()
        mock = bin_dir / "gradle"
        mock.write_text("""#!/usr/bin/env bash
set -euo pipefail
counter="$GRADLE_RETRY_COUNT_FILE"
n=0
[[ -f "$counter" ]] && n="$(cat "$counter")"
n=$((n+1))
echo "$n" > "$counter"
if [[ "$GRADLE_SCENARIO" == "fatal" ]]; then
  echo 'e: App.kt:25: Unresolved reference: nonexistentSymbol' >&2
  exit 1
fi
if [[ "$GRADLE_SCENARIO" == "persistent" || "$n" == "1" ]]; then
  echo "Could not resolve all artifacts for configuration 'classpath'." >&2
  echo "Could not find org.jetbrains.kotlin:kotlin-stdlib:2.2.21." >&2
  exit 1
fi
case " $* " in
  *" --refresh-dependencies "*) echo 'PASS: refreshed dependency metadata' ;;
  *) echo 'ERROR: retry omitted --refresh-dependencies' >&2; exit 9 ;;
esac
exit 0
""", encoding="utf-8")
        mock.chmod(0o755)
        count = home / "count.txt"
        env = os.environ.copy()
        env.update({
            "PATH": str(bin_dir) + os.pathsep + env["PATH"],
            "GRADLE_RETRY_COUNT_FILE": str(count),
            "GRADLE_SCENARIO": kind,
            "GRADLE_CI_MAX_ATTEMPTS": "3",
            "GRADLE_CI_RETRY_DELAY_SECONDS": "0",
        })
        completed = subprocess.run(
            ["bash", str(SCRIPT), ":app:compileDebugKotlin"],
            capture_output=True, text=True, env=env, timeout=30
        )
        return completed.returncode, int(count.read_text()), completed.stdout + completed.stderr

code, tries, output = scenario("transient")
assert code == 0 and tries == 2 and "refreshed dependency metadata" in output, output
code, tries, output = scenario("fatal")
assert code == 1 and tries == 1 and "non-retryable" in output, output
code, tries, output = scenario("persistent")
assert code == 1 and tries == 3 and "after 3 attempts" in output, output
print("PASS: retry one transient Maven failure, reject compiler errors, bound persistent failures")
