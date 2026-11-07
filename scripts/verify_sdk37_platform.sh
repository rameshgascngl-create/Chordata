#!/usr/bin/env bash
# Android SDK Platform 37 is distributed as android-37.0. Some tooling
# resolves compileSdk=37 as android-37. Provide a safe alias when needed.
set -euo pipefail
SDK_ROOT="${ANDROID_SDK_ROOT:-${ANDROID_HOME:-}}"
if [[ -z "$SDK_ROOT" ]]; then
  echo "ERROR: ANDROID_SDK_ROOT or ANDROID_HOME is not configured" >&2
  exit 2
fi
platform="$SDK_ROOT/platforms/android-37.0"
legacy="$SDK_ROOT/platforms/android-37"
if [[ ! -f "$platform/android.jar" ]]; then
  echo "ERROR: Android SDK 37.0 not installed at $platform" >&2
  exit 3
fi
if [[ ! -e "$legacy" && ! -L "$legacy" ]]; then
  ln -s android-37.0 "$legacy"
fi
if [[ ! -f "$legacy/android.jar" ]]; then
  echo "ERROR: Android SDK 37 compatibility path unavailable at $legacy" >&2
  exit 4
fi
echo 'PASS: Android SDK 37.0 installed; android-37 lookup resolves to the same platform'
