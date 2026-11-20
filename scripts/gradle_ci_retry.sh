#!/usr/bin/env bash
# Retry only recognised transient Gradle repository/dependency failures.
# Do not mask Kotlin compiler errors, failing tests, or missing source files.
set -euo pipefail

if (( $# < 1 )); then
  echo "Usage: bash scripts/gradle_ci_retry.sh <gradle-task> [more-tasks...]" >&2
  exit 2
fi
attempts="${GRADLE_CI_MAX_ATTEMPTS:-3}"
base_delay="${GRADLE_CI_RETRY_DELAY_SECONDS:-12}"
if [[ ! "$attempts" =~ ^[1-4]$ || ! "$base_delay" =~ ^[0-9]+$ ]]; then
  echo "Invalid CI retry configuration (attempts 1..4, delay nonnegative integer)" >&2
  exit 2
fi
log="$(mktemp)"
trap 'rm -f "$log"' EXIT

for (( attempt=1; attempt<=attempts; attempt++ )); do
  echo "Gradle CI invocation $attempt/$attempts"
  args=(gradle --no-daemon)
  if (( attempt > 1 )); then
    # Re-check remote metadata: Gradle may have cached a transiently missing POM.
    args+=(--refresh-dependencies)
  fi
  args+=("$@")
  set +e
  "${args[@]}" 2>&1 | tee "$log"
  status=${PIPESTATUS[0]}
  set -e
  if (( status == 0 )); then
    echo "PASS: Gradle finished successfully on attempt $attempt"
    exit 0
  fi
  # Restrict retries to dependency transport or metadata failures. A missing
  # Kotlin standard-library / AGP transitive POM was the observed CI incident.
  if ! grep -Eiq "Could not resolve all artifacts for configuration 'classpath'|Could not find (org\.jetbrains\.kotlin:(kotlin-stdlib|kotlin-gradle-plugins-bom)|com\.google\.code\.gson:gson)|Could not (GET|HEAD)|Received status code (429|5[0-9][0-9])|Read timed out|Connect timed out|Connection reset|Temporary failure in name resolution|Remote host terminated the handshake" "$log"; then
    echo "FAIL: non-retryable Gradle failure; preserving original exit code $status" >&2
    exit "$status"
  fi
  if (( attempt >= attempts )); then
    echo "FAIL: dependency resolution still failing after $attempts attempts" >&2
    exit "$status"
  fi
  delay=$((base_delay * attempt))
  echo "WARN: transient dependency retrieval failure; retrying in ${delay}s with refreshed Gradle metadata" >&2
  sleep "$delay"
done
exit 1
